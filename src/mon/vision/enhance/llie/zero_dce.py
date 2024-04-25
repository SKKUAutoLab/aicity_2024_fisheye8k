#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements Zero-DCE models."""

from __future__ import annotations

__all__ = [
    "ZeroDCE",
]

from typing import Any, Literal

import torch

from mon import core, nn
from mon.core import _callable
from mon.globals import MODELS, Scheme
from mon.vision.enhance.llie import base

console = core.console


# region Loss

class TotalVariationLoss(nn.Loss):
    """Total Variation Loss on the Illumination (Illumination Smoothness Loss)
    :math:`\mathcal{L}_{tvA}` preserve the monotonicity relations between
    neighboring pixels. It is used to avoid aggressive and sharp changes between
    neighboring pixels.
    
    References:
        `<https://github.com/Li-Chongyi/Zero-DCE/blob/master/Zero-DCE_code/Myloss.py>`__
    """
    
    def __init__(
        self,
        loss_weight: float = 1.0,
        reduction  : Literal["none", "mean", "sum"] = "mean",
    ):
        super().__init__(loss_weight=loss_weight, reduction=reduction)
    
    def forward(
        self,
        input : torch.Tensor,
        target: torch.Tensor | None = None
    ) -> torch.Tensor:
        x       = input
        b       = x.size()[0]
        h_x     = x.size()[2]
        w_x     = x.size()[3]
        count_h =  (x.size()[2]-1) * x.size()[3]
        count_w = x.size()[2] * (x.size()[3] - 1)
        h_tv    = torch.pow((x[:, :, 1:, :] - x[:, :, :h_x - 1, :]), 2).sum()
        w_tv    = torch.pow((x[:, :, :, 1:] - x[:, :, :, :w_x - 1]), 2).sum()
        loss    = self.loss_weight * 2 * (h_tv / count_h + w_tv / count_w) / b
        # loss    = base.reduce_loss(loss=loss, reduction=self.reduction)
        return loss
    
    
class Loss(nn.Loss):

    def __init__(
        self,
        spa_weight    : float = 1.0,
        exp_patch_size: int   = 16,
        exp_mean_val  : float = 0.6,
        exp_weight    : float = 10.0,
        col_weight    : float = 5.0,
        tva_weight    : float = 200.0,
        reduction     : Literal["none", "mean", "sum"] = "mean",
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.spa_weight = spa_weight
        self.exp_weight = exp_weight
        self.col_weight = col_weight
        self.tva_weight = tva_weight
        
        self.loss_spa = nn.SpatialConsistencyLoss(reduction=reduction)
        self.loss_exp = nn.ExposureControlLoss(
            reduction  = reduction,
            patch_size = exp_patch_size,
            mean_val   = exp_mean_val,
        )
        self.loss_col = nn.ColorConstancyLoss(reduction=reduction)
        self.loss_tva = TotalVariationLoss(reduction=reduction)
    
    def forward(
        self,
        input  : torch.Tensor,
        adjust : torch.Tensor,
        enhance: torch.Tensor,
        **_
    ) -> torch.Tensor:
        loss_spa = self.loss_spa(input=enhance, target=input)
        loss_exp = self.loss_exp(input=enhance)
        loss_col = self.loss_col(input=enhance)
        loss_tva = self.loss_tva(input=adjust)
        loss     = (
              self.spa_weight * loss_spa
            + self.exp_weight * loss_exp
            + self.col_weight * loss_col
            + self.tva_weight * loss_tva
        )
        return loss

# endregion


# region Model

@MODELS.register(name="zero_dce")
class ZeroDCE(base.LowLightImageEnhancementModel):
    """Zero-DCE (Zero-Reference Deep Curve Estimation) model.
    
    Args:
        in_channels: The first layer's input channel. Default: ``3`` for RGB image.
        num_channels: The number of input and output channels for subsequent
            layers. Default: ``32``.
        num_iters: The number of progressive loop. Default: ``8``.
        
    References:
        `<https://github.com/Li-Chongyi/Zero-DCE>`__

    See Also: :class:`base.LowLightImageEnhancementModel`
    """
    
    _scheme: list[Scheme] = [Scheme.UNSUPERVISED, Scheme.ZEROSHOT]
    _zoo   : dict = {}

    def __init__(
        self,
        in_channels : int = 3,
        num_channels: int = 32,
        num_iters   : int = 8,
        weights     : Any = None,
        *args, **kwargs
    ):
        super().__init__(
            name        = "zero_dce",
            in_channels = in_channels,
            weights     = weights,
            *args, **kwargs
        )
        assert num_iters <= 8
        
        # Populate hyperparameter values from pretrained weights
        if isinstance(self.weights, dict):
            in_channels  = self.weights.get("in_channels" , in_channels)
            num_channels = self.weights.get("num_channels", num_channels)
            num_iters    = self.weights.get("num_iters"   , num_iters)
        self.in_channels  = in_channels
        self.num_channels = num_channels
        self.num_iters    = num_iters
        self.out_channels = self.in_channels * self.num_iters
        
        # Construct model
        self.relu     = nn.ReLU(inplace=True)
        self.e_conv1  = nn.Conv2d(self.in_channels,      self.num_channels, 3, 1, 1, bias=True)
        self.e_conv2  = nn.Conv2d(self.num_channels,     self.num_channels, 3, 1, 1, bias=True)
        self.e_conv3  = nn.Conv2d(self.num_channels,     self.num_channels, 3, 1, 1, bias=True)
        self.e_conv4  = nn.Conv2d(self.num_channels,     self.num_channels, 3, 1, 1, bias=True)
        self.e_conv5  = nn.Conv2d(self.num_channels * 2, self.num_channels, 3, 1, 1, bias=True)
        self.e_conv6  = nn.Conv2d(self.num_channels * 2, self.num_channels, 3, 1, 1, bias=True)
        self.e_conv7  = nn.Conv2d(self.num_channels * 2, self.out_channels, 3, 1, 1, bias=True)
        self.maxpool  = nn.MaxPool2d(2, stride=2, return_indices=False, ceil_mode=False)
        self.upsample = nn.UpsamplingBilinear2d(scale_factor=2)
        
        # Loss
        self._loss = Loss()
        
        # Load weights
        if self.weights:
            self.load_weights()
        else:
            self.apply(self._init_weights)

    def _init_weights(self, m: nn.Module):
        classname = m.__class__.__name__
        if classname.find("Conv") != -1:
            m.weight.data.normal_(0.0, 0.02)
        elif classname.find("BatchNorm") != -1:
            m.weight.data.normal_(1.0, 0.02)
            m.bias.data.fill_(0)

    def forward_loss(
        self,
        input : torch.Tensor,
        target: torch.Tensor | None,
        *args, **kwargs
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        pred = self.forward(input=input, *args, **kwargs)
        adjust, enhance = pred
        loss = self.loss(input, adjust, enhance)
        return enhance, loss

    def forward(
        self,
        input    : torch.Tensor,
        augment  : _callable = None,
        profile  : bool      = False,
        out_index: int       = -1,
        *args, **kwargs
    ) -> tuple[torch.Tensor, torch.Tensor]:
        x   = input
        x1  =  self.relu(self.e_conv1(x))
        x2  =  self.relu(self.e_conv2(x1))
        x3  =  self.relu(self.e_conv3(x2))
        x4  =  self.relu(self.e_conv4(x3))
        x5  =  self.relu(self.e_conv5(torch.cat([x3, x4], 1)))
        x6  =  self.relu(self.e_conv6(torch.cat([x2, x5], 1)))
        x_r = torch.tanh(self.e_conv7(torch.cat([x1, x6], 1)))
        
        x_rs = torch.split(x_r, 3, dim=1)
        y    = x
        for i in range(0, self.num_iters):
            y = y + x_rs[i] * (torch.pow(y, 2) - y)

        return x_r, y
    
# endregion

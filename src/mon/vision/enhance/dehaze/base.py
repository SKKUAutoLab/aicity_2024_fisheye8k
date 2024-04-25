#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements the base class for de-hazing models."""

from __future__ import annotations

__all__ = [
    "DehazingModel",
]

from abc import ABC

from mon import core
from mon.globals import ZOO_DIR, Task
from mon.vision.enhance import base

console = core.console


# region Model

class DehazingModel(base.ImageEnhancementModel, ABC):
    """The base class for all de-hazing models.
    
    See Also: :class:`base.ImageEnhancementModel`.
    """
    
    _tasks: list[Task] = [Task.DEHAZE]
    
    @property
    def zoo_dir(self) -> core.Path:
        return ZOO_DIR / "mon" / "vision" / "enhance" / "dehaze"
    
# endregion

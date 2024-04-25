#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module implements YAML file handler by extending the :mod:`yaml` module.
"""

from __future__ import annotations

from typing import Any, TextIO

from yaml import *

from mon.core import pathlib
from mon.core.file import base
from mon.globals import FILE_HANDLERS


# region YAML File Handler

@FILE_HANDLERS.register(name=".yaml")
@FILE_HANDLERS.register(name=".yml")
class YAMLHandler(base.FileHandler):
    """YAML file handler."""
    
    def read_from_fileobj(self, path: pathlib.Path | str | TextIO, **kwargs) -> Any:
        kwargs.setdefault("Loader", FullLoader)
        return load(stream=path, **kwargs)
    
    def write_to_fileobj(self, obj: Any, path: pathlib.Path | str | TextIO, **kwargs):
        path = pathlib.Path(path)
        kwargs.setdefault("Dumper", Dumper)
        dump(data=obj, stream=path, **kwargs)
    
    def write_to_string(self, obj: Any, **kwargs) -> str:
        kwargs.setdefault("Dumper", Dumper)
        return dump(data=obj, **kwargs)

# endregion

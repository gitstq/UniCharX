#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniCharX - Lightweight Unicode Character Intelligent Search CLI Engine
轻量级Unicode字符智能搜索CLI引擎

A zero-dependency, cross-platform CLI tool for searching and exploring
Unicode characters with fuzzy matching and TUI dashboard.
"""

__version__ = "1.0.0"
__author__ = "UniCharX Team"
__license__ = "MIT"

from unicharx.core import UniCharX, search_unicode, get_char_info
from unicharx.cli import main

__all__ = [
    "UniCharX",
    "search_unicode", 
    "get_char_info",
    "main",
    "__version__",
]

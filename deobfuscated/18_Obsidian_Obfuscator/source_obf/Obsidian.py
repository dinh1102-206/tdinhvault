#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Obfuscator v2.5 - Python 3.14 Edition
Launcher script for interactive Obsidian menu
"""
import sys
import os

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from output.tools_sach.Obsidian_py314 import main

if __name__ == '__main__':
    main()

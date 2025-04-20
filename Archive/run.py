#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для запуска системы индексации документов
"""

import os
import sys

# Добавляем корневую директорию проекта в путь для импортов
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.main import main

if __name__ == "__main__":
    main() 
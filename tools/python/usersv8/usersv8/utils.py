import argparse
import os
import platform
import sys
import urllib.parse as urlparse

import requests
from lxml import html


def is_deb_based_linux():

    """
    Определяет принадлежность операционной системы
    к типу пакетов
    """

    return platform.system() == "Linux"


def is_rpm_based_linux():

    """
    Определяет принадлежность операционной системы
    к типу пакетов
    """

    return False


def is_osx():

    """
    Определяет принадлежность к операционной системе
    """

    return False


def is_amd64_sys():

    """
    Определяет принадлежность операционной системы
    к архитектуре
    """

    return platform.machine() == "x86_64" or platform.machine() == "AMD64"

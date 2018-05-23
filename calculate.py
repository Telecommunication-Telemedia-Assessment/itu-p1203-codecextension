#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/itu-p1203/')

from p1203Pv_extended import P1203Pv_codec_extended
from itu_p1203.__main__ import main

# disable the codec warning
# P1203Pv_codec_extended._show_warning = False

if __name__ == "__main__":
    sys.exit(main({"Pv": P1203Pv_codec_extended}))

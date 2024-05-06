#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import re
import yaml
import logging
import ctrl
import shutil
import pkg


logging.basicConfig(level=logging.INFO)

basedir = os.path.dirname(os.path.realpath(__file__))

if sys.argv[-1] != "create":
    print("Usage: videb <config.yml> create")
    sys.exit(1)

try:
    config = yaml.safe_load(open(sys.argv[-2]))
except Exception as e:
    print(e)
    sys.exit(1)

pkg = pkg.Pkg(config, ctrl.Ctrl(config))
pkg.create_fs()
pkg.create_control()
pkg.create_package(move=False)

pkg.set_size(os.path.getsize(basedir + "/packdir.deb") // 1000)  # kBs, not kiBs

os.remove(basedir + "/packdir.deb")

pkg.create_fs()
pkg.create_control()
pkg.create_package()

logging.info("Cleaning up")
shutil.rmtree(basedir + "/packdir")

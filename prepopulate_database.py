#!/usr/bin/env python
"""Refresh a work's OPDS feeds."""
import os
import sys
bin_dir = os.path.split(__file__)[0]
package_dir = os.path.join(bin_dir, "..", "..")
sys.path.append(os.path.abspath(package_dir))
from scripts import Script
Script().run()
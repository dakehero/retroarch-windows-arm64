"""Normalize inherited Windows environment key casing for MSBuild/.NET Framework."""
import os
import subprocess
import sys

env = {key.upper(): value for key, value in os.environ.items()}
raise SystemExit(subprocess.call(sys.argv[1:], env=env))

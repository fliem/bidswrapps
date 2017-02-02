#! /usr/bin/env python
# some portions are borrowed from https://github.com/poldracklab/pydeface/blob/master/setup.py
# which borrowed some portions from https://github.com/mwaskom/lyman/blob/master/setup.py


descr = """bidswrapps: a wrapper to run BIDS-Apps on cloud systems"""

import os
from setuptools import setup, find_packages
import glob
from bidswrapps import __version__

DISTNAME = "bidswrapps"
DESCRIPTION = descr
MAINTAINER = 'Franz Liem'
MAINTAINER_EMAIL = 'franziskus.liem@uzh.ch'
LICENSE = 'Apache2.0'
DOWNLOAD_URL = 'https://github.com/fliem/bidswrapps'
VERSION = __version__

PACKAGES = find_packages()

def check_dependencies():
    # Just make sure dependencies exist, I haven't rigorously
    # tested what the minimal versions that will work are
    needed_deps = []
    missing_deps = []
    for dep in needed_deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)

    if missing_deps:
        raise ImportError("Missing dependencies: %s" % missing_deps)


if __name__ == "__main__":

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    import sys

    if not (len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                            sys.argv[1] in ('--help-commands',
                                                            '--version',
                                                            'egg_info',
                                                            'clean'))):
        check_dependencies()

    # datafiles = {'pydeface': ['data/facemask.nii.gz', 'data/mean_reg2mean.nii.gz']}

    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          version=VERSION,
          url=DOWNLOAD_URL,
          download_url=DOWNLOAD_URL,
          packages=PACKAGES,
          scripts=["scripts/bidswrapps_start.py",
                   "scripts/bidswrapps_check_logfiles.py"],
          classifiers=['Intended Audience :: Science/Research',
                       'Programming Language :: Python :: 2.7',
                       'License :: OSI Approved :: BSD License',
                       'Operating System :: POSIX',
                       'Operating System :: Unix',
                       'Operating System :: MacOS']
          )

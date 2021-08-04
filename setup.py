#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages, Extension
import os
import sys
import numpy
import platform

from Cython.Build import cythonize


requirements = [
    "numpy>=1.16.3",
    "scipy>=1.2.0",
    "Cython>=0.28.5",
    "ephem>=3.7.6.0",
    "healpy>=1.14.0",
    "scikit-sparse>=0.4.5",
    "pint-pulsar>=0.8.2",
    "libstempo>=2.4.0",
    "enterprise-pulsar>=3.1.0",
    "emcee",
    "ptmcmcsampler",
]

test_requirements = [
    "pytest",
]


if platform.system() == "Darwin":
    extra_compile_args = ["-O2", "-Xpreprocessor", "-fopenmp", "-fno-wrapv"]
    extra_link_args = ["-liomp5"] if os.getenv("NO_MKL", 0) == 0 else ["-lomp"]
else:
    extra_compile_args = ["-O2", "-fopenmp", "-fno-wrapv"]
    extra_link_args = ["-liomp5"] if os.getenv("NO_MKL", 0) == 0 else []


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Cython extensions
ext_modules=[
    Extension('jitterext',
             ['jitterext.pyx'],
             include_dirs = [numpy.get_include()],
             extra_compile_args=["-O2"]),
    Extension('choleskyext_omp',
             ['choleskyext_omp.pyx'],
             include_dirs = [numpy.get_include()],
             extra_link_args=["-liomp5"],
             extra_compile_args=["-O2", "-fopenmp", "-fno-wrapv"])
]


setup(
    name="enterprise_outliers",
    description="Single pulsar outlier analysis framework",
    ext_modules=cythonize(ext_modules),
    install_requires=requirements,
    zip_safe=False,
)

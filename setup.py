#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os
import numpy
import platform

requirements = [
    "numpy>=1.16.3",
    "scipy>=1.2.0",
    "Cython>=0.28.5",
    "scikit-sparse>=0.4.5",
    "enterprise-pulsar>=3.1.0",
    "pint-pulsar>=0.8.3",
    "matplotlib>=3.2.0",
    "numdifftools>=0.9.0"
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


ext_modules = [
    Extension(
        "enterprise_outliers.jitterext",
        ["./enterprise_outliers/jitterext.pyx"],
        include_dirs=[numpy.get_include()],
        extra_compile_args=["-O2"],
    ),
    Extension(
        "enterprise_outliers.choleskyext_omp",
        ["./enterprise_outliers/choleskyext_omp.pyx"],
        include_dirs=[numpy.get_include()],
        extra_link_args=extra_link_args,
        extra_compile_args=extra_compile_args,
    ),
]

# Extract version
def get_version():
    with open("enterprise_outliers/__init__.py") as f:
        for line in f.readlines():
            if "__version__" in line:
                return line.split('"')[1]


setup(
    name="enterprise_outliers",
    version=get_version(),
    description="Outlier analysis",
    classifiers=[
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="gravitational-wave, black-hole binary, pulsar-timing arrays",
    url="https://github.com/nanograv/enterprise_outliers",
    author="Stephen R. Taylor, Paul T. Baker, Jeffrey S. Hazboun, Sarah Vigeland",
    author_email="srtaylor@caltech.edu",
    license="MIT",
    packages=[
        "enterprise_outliers",
    ],

    ext_modules=cythonize(ext_modules),
    test_suite="tests",
    tests_require=test_requirements,
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)

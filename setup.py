"""Setup script for PhotoPy Pro."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="photopy-pro",
    version="2.0.0",
    author="PhotoPy Pro Team",
    author_email="contact@photopy-pro.com",
    description="Advanced Image Editor built with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/photopy-pro/photopy-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Editors",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python>=4.5.0",
        "Pillow>=8.0.0",
        "PyQt6>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "photopy-pro=photopy_pro.main:main",
        ],
    },
    include_package_data=True,
)
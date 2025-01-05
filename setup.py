from setuptools import setup, find_packages

setup(
    name="tracksep",
    version="1.0.0",
    description="A PyQt5-based video and audio separator using FFmpeg",
    author="OutlawRGB",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5>=5.15",
    ],
    entry_points={
        "console_scripts": [
            "tracksep=src.main:main",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

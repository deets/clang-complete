import os
import sys
from setuptools import setup, find_packages

setup(
    name="ClangComplete",
    version="0.1",
    description="clang-complete implementation for autocomplete-clang-async for Emacs",
    author="Diez B. Roggisch",
    author_email="deets@web.de",
    license="MIT",
    packages=find_packages(exclude=['ez_setup', 'tests']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "abl.robot",
        ],
    classifiers = [
    ],
    entry_points={
        'console_scripts': [
            'clang-complete=clangcomplete:ClangCompleteRobot.main',
            ]
        },
)

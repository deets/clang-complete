import sys
from setuptools import setup, find_packages

version = "%i.%i" % sys.version_info[:2]
setup(
    name = "clang-complete",
    version = "0.1",
    author = "Diez B. Roggisch",
    author_email = "deets@web.de",
    description = "A package to allow clang completion in emacs.",
    packages = find_packages(),
    install_requires = [
        "abl.util",
        ],
    license = "PSF",
    keywords = "python clang autocomplete",
    entry_points = {
        'console_scripts': [
            'clang-complete = clangcomplete:main',
        ],
    }
)

from setuptools import setup


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Console :: Curses",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3",
    "Topic :: Utilities",
]

# Get the long description from the README file
with open("README.md", encoding="utf-8") as f:
    read_file = f.read()

setup(
    name="kadoo",
    description="The priorities management CLI you never knew you needed",
    url="https://github.com/TechWiz-3/kadoo-cli",
    author="Zac the Wise aka TechWiz-3",
    version="0.0.1",
    packages=["kadoo"],
    long_description=read_file,
    long_description_content_type="text/markdown",
    entry_points="""
    [console_scripts]
    unfollow=unfollow.cli:main
    """,
    classifiers=classifiers,
    install_requires=["rich"],
    )

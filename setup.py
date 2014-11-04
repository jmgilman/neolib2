from distutils.core import setup

setup(
    name="neolib2",
    packages=["neolib", "neolib.http", "neolib.user"],
    version="0.1.1",
    description="Neopets automation library for Python",
    author="Joshua Gilman",
    author_email="joshuagilman@gmail.com",
    url="https://github.com/jmgilman/neolib2",
    download_url="https://github.com/jmgilman/neolib2/archive/master.zip",
    keywords=["Neopets", "automation", "library"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description="",
    )

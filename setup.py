from distutils.core import setup

setup(
    name="neolib2",
    packages=["neolib",
              "neolib.http",
              "neolib.inventory",
              "neolib.item",
              "neolib.registration",
              "neolib.shop",
              "neolib.user",
              "neolib.user.hooks"
              ],
    version="0.1.8",
    description="Neopets automation library for Python",
    author="Joshua Gilman",
    author_email="joshuagilman@gmail.com",
    url="https://github.com/jmgilman/neolib2",
    download_url="https://github.com/jmgilman/neolib2/tarball/0.1",
    install_requires=[
        "requests==2.4",
        "lxml==3.4.1",
        "pillow==2.6",
        ],
    package_data={'neolib2': ['tests/*', 'examples/*']},
    keywords=["Neopets", "automation", "library"],
    classifiers=[],
    long_description="",
    )

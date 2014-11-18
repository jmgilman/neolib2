Neolib 2
=======
Neolib is a python library which aims to automate the cult classic web based
game, Neopets. Neolib automates the game from the ground up by centralizing
actions around the Neopets user account. The library includes strong
functionality for performing complex tasks as well as built-in querying of a
user's assets.

Neolib is built upon python's famous [requests](http://docs.python-requests.org/en/latest/)
library for handling HTTP communications and the powerful [lxml](http://lxml.de/)
library for parsing HTML content. These two libraries combine to give Neolib a
powerful and fast framework for automation.

Neolib is aimed for being deployed on a server or cloud environment. The
library does not assume that there will be a graphical interface for interacting
with the library. Rather, it assumes the code will either be ran in a script on
a server or as part of a grander program with a web interface.

Neolib is still in a very early stage of development. As such, things are
expected to change, up to and including the base classes. If you intend on using
the library in this state please ensure you check back frequently with the master
branch for changes.

Neolib is also looking for developers interested in contributing to the project.
A very detailed and useful primer can be found in the links below. Please read
it and understand it fully before making contributions to the project.

**Documentation**: http://neolib2.readthedocs.org/en/latest/

**Contribution Primer**: http://neolib2.readthedocs.org/en/latest/development/primer.html

Installation
============
* Run the following

```
$ pip install neolib2
```

Alternatively:

* Clone the repository
* Install the dependancies

```
$ cd neolib2
$ pip install -r requirements.txt
```

* Use it!

Usage
=====
```python
>>> from neolib.user.User import User
>>> usr = User('username', 'password')
>>> usr.login()
True
>>> usr.inventory
Inventory <32 items>
```

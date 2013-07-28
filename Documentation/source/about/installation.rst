============
Installation
============

-------------------
Installing from zip
-------------------

**1. Download zip**

Download the latest version of :py:mod:`hTools2` from the project’s repository on `github <https://github.com/gferreira/hTools2>`_.

**2. Unzip and choose a location**

Unzip the package, and move the files to a folder on your hard disk. For example::

    /code/

Avoid using spaces or non-ASCII characters in folder names above the :py:mod:`hTools2` folder, since it may cause a problems.

---------------------------
Adding the module to Python
---------------------------

Create a simple text file, containing the path to the ``Lib`` folder inside :py:mod:`hTools2`::

	/code/hTools2/Lib/

Save this file as ``hTools2.pth`` in the ``site-packages`` folder for the desired Python(s)::

	/Library/Python/2.5/site-packages/hTools2.pth
	/Library/Python/2.6/site-packages/hTools2.pth

And that’s it.

------------------------
Testing the installation
------------------------

To check if `hTools2` has been installed successfully, try to run this line in the RoboFont scripting window or in Terminal::

    import hTools2

If no error message is returned, the installation was successful.

**Configuring the Extensions menu**

To have the dialogs in the :py:mod:`hTools2` ``Scripts`` folder appear in RoboFont’s ``Extensions`` menu, select it as the root path for Python scripts in the ``Preferences`` window.

------------------------------
Configuring keyboard shortcuts
------------------------------

As an optional last step, it is also possible to configure keyboard shortcuts for :py:mod:`hTools2` scripts in RoboFont.

As a reference, my current keyboard shortcuts are collected here.

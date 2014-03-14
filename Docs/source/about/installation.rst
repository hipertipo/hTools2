===========================
Installing hTools2 manually
===========================

.. .. contents:: Table of Contents
..    :depth: 3

--------------------
0. choose a location
--------------------

Choose a location on your hard disk to store the code libraries. For example::

    /_code/

Avoid using spaces or non-ASCII characters in folder names above the :py:mod:`hTools2` folder.

--------------------------
1. getting the source-code
--------------------------

^^^^^^^^^^^^^^^^^^^^
1a. download the zip
^^^^^^^^^^^^^^^^^^^^

Download the latest version of :py:mod:`hTools2` from the project’s repository on `github <https://github.com/gferreira/hTools2>`_.

Unzip and save it into the newly created code folder::

    /_code/hTools2/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1b. check-out the code with git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are used to git, you can clone the code directly from the project's repository on github::

    git clone https://github.com/gferreira/hTools2.git

------------------------------
2. adding the module to Python
------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2a. manually with a .pth file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a simple text file, containing the path to the ``Lib`` folder inside :py:mod:`hTools2`::

    /code/hTools2/Lib/

.. note:: The easiest way to get the correct path is by dragging the ``Lib`` folder from Finder into a code editor or Terminal -- so you'll get the path without having to type it.

Save this file as ``hTools2.pth`` in the ``site-packages`` folder for the desired Python(s)::

    /Library/Python/2.5/site-packages/hTools2.pth
    /Library/Python/2.6/site-packages/hTools2.pth
    /Library/Python/2.7/site-packages/hTools2.pth

And that’s it.

.. note:: This method will create a **reference** to the current ``Lib`` folder, in this case ``/code/hTools2/Lib/``.

^^^^^^^^^^^^^^^^^^^^^^^
2b. with a setup script
^^^^^^^^^^^^^^^^^^^^^^^

As an alternative to the manual installation (2a), it is also possible to install :py:mod:`hTools2` by running a setup script. 

In the Terminal, go the ``hTools2`` folder, and simply run the script ``setup.py`` with Python::

    cd /_code/hTools2/
    python setup.py install

If you get an error message regarding user permissions, try running the script with ``sudo``::

    sudo python setup.py install

This will prompt you to input your user name and password to allow access to system folders.

.. note:: This method will **copy** the ``Lib`` folder to the Python ``site-packages`` folder.

---------------------------
3. testing the installation
---------------------------

To check if ``hTools2`` has been installed successfully, try to run this line in the RoboFont scripting window or in Terminal::

    import hTools2

If no error message is returned, the installation was successful.

=====================
Installing (manually)
=====================

--------------------
0. Choose a location
--------------------

Choose a location on your hard disk to store the code libraries. For example::

    /_code/

Avoid using spaces or non-ASCII characters in folder names above the :py:mod:`hTools2` folder, since it may cause a problems.

----------------------
1. Get the source-code
----------------------

^^^^^^^^^^^^^^^^^^^^
1a. Download the zip
^^^^^^^^^^^^^^^^^^^^

Download the latest version of :py:mod:`hTools2` from the project’s repository on `github <https://github.com/gferreira/hTools2>`_.

Unzip it into the newly created ``_code`` folder.

^^^^^^^^^^^^^^^^^^^^^^
1b. Check-out with git
^^^^^^^^^^^^^^^^^^^^^^

If you are used to git, you can grab the code directly from the project's repository on github::

    git clone https://github.com/gferreira/hTools2.git

------------------------------
2. Adding the module to Python
------------------------------

Create a simple text file, containing the path to the ``Lib`` folder inside :py:mod:`hTools2`::

    /code/hTools2/Lib/

Save this file as ``hTools2.pth`` in the ``site-packages`` folder for the desired Python(s)::

    /Library/Python/2.5/site-packages/hTools2.pth
    /Library/Python/2.6/site-packages/hTools2.pth
    /Library/Python/2.7/site-packages/hTools2.pth

And that’s it.

---------------------------
3. Testing the installation
---------------------------

To check if ``hTools2`` has been installed successfully, try to run this line in the RoboFont scripting window or in Terminal::

    import hTools2

If no error message is returned, the installation was successful.

------------------------------
4. Configuring hTools2 Scripts
------------------------------

``hTools2`` comes with many scripts and dialogs which need to me made available to the user via RoboFont’s inteface.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4a. Scripts under a custom menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add a ``hTools2`` entry to main menu in RoboFont, go to RoboFont's ``Preferences/Extensions`` Window. In the section ``start-up scripts``, select the file ``hTools2/add-RF-menu.py``.

Use this option if you already have many Scripts under your ``Extensions`` menu.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
4b. Scripts under the Extensions menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another option is to have the scripts appear under RoboFont’s ``Extensions`` menu. To configure this option, go to RoboFont's ``Preferences/Python`` Window, and select the folder ``hTools2/Scripts`` as the scripts folder.

---------------------------------
5. Configuring keyboard shortcuts
---------------------------------

As an optional last step, it is also possible to configure keyboard shortcuts for ``hTools2`` scripts in RoboFont.

As a reference, my current keyboard shortcuts are collected here.

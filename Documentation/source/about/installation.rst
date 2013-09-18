=====================
Installing (manually)
=====================

.. contents:: Table of Contents
   :depth: 3

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

^^^^^^^^^^^^
2a. manually
^^^^^^^^^^^^

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

As an optional last step, it is also possible to configure keyboard shortcuts for ``hTools2`` scripts in RoboFont's ``Preferences/Extensions`` Window. In the section ``start-up scripts``, add the file ``add-RF-shortcuts.py``.

Here is an overview of all current keyboard schortcuts:

======= ==========================================================
key     dialog
======= ==========================================================
``a``   selected glyphs > actions > actions
``c``   selected glyphs > color > paint select
``f``   selected glyphs > transform > gridfit
``h``   selected glyphs > metrics > set width
``i``   selected glyphs > interpol > interpolate
``k``   selected glyphs > layers > mask
``l``   selected glyphs > layers > copy to layer
``m``   selected glyphs > transform > move
``o``   selected glyphs > layers > copy to mask
``p``   selected glyphs > actions > copy paste
``r``   selected glyphs > transform > mirror
``s``   selected glyphs > transform > scale
``t``   selected glyphs > transform > shift
``w``   selected glyphs > transform  > skew
``v``   current font > vmetrics > adjust
======= ==========================================================

.. warning:: These shortcuts might clash with existing ones defined by other extensions or by the user.

.. note:: To customize the shortcuts used by ``hTools2``, simply edit the contents of the file ``add-RF-shortcuts.py``. It is recommended to save your custom shortcuts under a different file name, to avoid them from being overwritten in future ``hTools2`` code updates. Also, in the ``Preferences/Extensions`` Window, make sure that the correct (customized) script is set as a start-up script.

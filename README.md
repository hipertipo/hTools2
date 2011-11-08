hTools2
=======

hTools2 is a rewrite of hTools for RoboFont.

hTools is a collection of tools and high-level objects to help with common font-production tasks. It is written in Python on top of existing free/open libraries (RoboFab, dialogKit, NodeBox), and was originally developed around FontLab Studio. 

*Work is still in early days, there’s not much to see/use at the moment.*


Installation
------------

To install hTools2, first download and unzip the [latest package](https://github.com/gferreira/hTools2/zipball/master) from the [repository on github](https://github.com/gferreira/hTools2).

Then:

1. Move the folder to the desired location on your hard disk (for example `/code/`)
2. Create a simple text file named `hTools2.pth` with the path to the `Lib` folder in hTools2: `/code/hTools2/Lib/`.
3. Save this file in the `site-packages` folder for the current Python, for example `/Library/Python/2.6/site-packages`.

That's it.

To test if hTools2 is installed, try to run this in the RoboFont scripting window:

    import hTools2
    
If no error message is returned, we're good to go.


Feedback
--------

For feedback and questions, simply [drop me a message](mailto:gustavo@hipertipo.com).

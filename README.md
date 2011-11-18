hTools2
=======

hTools2 is a rewrite of hTools for RoboFont.

(hTools1 is an unpublished collection of Python tools and objects for type-design & font-production work in FontLab.)

*...work has just started, so there is not much to see yet...*

A couple of useful/usable scripts can already be found inside the `Scripts` folder:

- batch generate fonts from folder
- batch generate all open fonts
- transform selected glyphs in font (remove overlaps, auto contour directions etc.)
- copy glyphs to mask and between fonts
- move layer interactively with slider
- etc.

*...more code and documentation soon...*

Looking forward to [RoboThon 2012](http://twitter.com/#!/robothonconf)!


Credits
-------

Code written by Gustavo Ferreira with help from collaborators. Special thanks to Frederik for the many tips, comments and corrections.

* [hipertipo.com](http://hipertipo.com)

Work on hTools is supported/sponsored by Nikola Djurek / Typonine — thanks!

* [typonine.com](http://typonine.com)

RoboFont is developed by Frederik Berlaen / TypeMyType.

* [typemytype.com](http://typemytype.com)
* [robofont.com](http://robofont.com)

Both RoboFont and hTools are built on top of foundation work and Python libraries by LettError and TypeSupply (RoboFab, vanilla etc).

* [letterror.com](http://letterror.com)
* [typesupply.com](http://typesupply.com)
* [robofab.org](http://robofag.org)
* [vanilla](http://code.typesupply.com/wiki/Vanilla)


Installation
------------

*...for the curious and the brave...*

### Installing from the zip package

To install hTools2, first download and unzip the [latest package](https://github.com/gferreira/hTools2/zipball/master) from the [repository on github](https://github.com/gferreira/hTools2).

Then:

1. Move the folder to the desired location on your hard disk (for example `/code/`)
2. Create a simple text file named `hTools2.pth` with the path to the `Lib` folder in hTools2: `/code/hTools2/Lib/`.
3. Save this file in the `site-packages` folder for the current Python, for example `/Library/Python/2.6/site-packages`.

That’s it.

To test if hTools2 is installed, try to run this in the RoboFont scripting window:

    import hTools2
    
If no error message is returned, we’re good to go.

### Installing via git

Make sure you have Git up and running (see the [official documentation](http://help.github.com/mac-set-up-git/) for instructions).

Then, add hTools2 on github.com as a remote repository:

    git remote add hTools2 git://github.com/gferreira/hTools2.git
  
Finally, fetch the lastest “master” branch, and merge it with your local version:

    git pull hTools2 master

...I hope this works, if not please let me know and I'll do my best to improve the intructions...


Feedback
--------

For feedback and questions, simply [drop me a message](mailto:gustavo@hipertipo.com).


Support
-------

If you would like to support hTools development, consider [comissioning more work](mailto:gustavo@hipertipo.com?subject=custom-scripts-and-tools) on custom or additional tools and functionality.


License
-------

[BSD License](http://www.opensource.org/licenses/bsd-license.php)


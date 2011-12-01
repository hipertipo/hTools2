hTools2
=======

hTools2 is a collection of Python scripts, tools and objects for type-design & font-production work with [RoboFont](http://robofont.com).

It is built on top of [RoboFab](http://robofag.org), [vanilla](http://code.typesupply.com/wiki/Vanilla) and the [UFO font format](http://unifiedfontobject.org/).


Useful scripts
--------------

- batch generate fonts for all .ufos in folder
- batch generate all open fonts
- transform selected glyphs (remove overlaps, auto contour directions etc.)
- copy glyphs to mask and between fonts
- move layer interactively with slider
- adjust vertical metrics interactively with slider
- scale glyphs up/down by percentage increments

Have a look inside the `Scripts` folder for more.


Credits
-------

hTools2 is developed by [Gustavo Ferreira (Hipertipo)](http://hipertipo.com) and [Nikola Djurek (Typonine)](http://typonine.com), with help from collaborators.

Special thanks to Frederik Berlaen for the many tips, comments and corrections.

RoboFont is developed by [Frederik Berlaen (TypeMyType)](http://typemytype.com).

RoboFont and hTools are built on fundamental work and libraries by Erik van Blokland & Just van Rossum [LettError](http://letterror.com) and [Tal Leming (TypeSupply)](http://typesupply.com).


Installation
------------

1. Get the latest version of hTools2 from the [.zip package](https://github.com/gferreira/hTools2/zipball/master) or directly from the [git repository](https://github.com/gferreira/hTools2).

2. Move the folder to the desired location on your hard disk, for example `~/code/`.

3. Create a simple text file named `hTools2.pth`, containing the path to the `Lib` folder in hTools2: 

```
~/code/hTools2/Lib/
```

4. Save this file in the `site-packages` folder for the current Python, for example `/Library/Python/2.6/site-packages`.

5. To test if `hTools2` is installed, try to run this in the RoboFont scripting window:

```
import hTools2
```
    
6. If no error message is returned, the library has been installed sucessfully.


Feedback
--------

For feedback and questions, simply [drop me a message](mailto:gustavo@hipertipo.com).


Support
-------

If you would like to support hTools development, consider [comissioning more work](mailto:gustavo@hipertipo.com?subject=custom-scripts-and-tools) on custom or additional tools and functionality.


License
-------

[BSD License](http://www.opensource.org/licenses/bsd-license.php)


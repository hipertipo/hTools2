### 1. Get the code

Download the latest version of hTools2 from the project’s repository on [github](https://github.com/gferreira/hTools2). Or checkout the code with `git`, if you know how to use it.

### 2. Unzip and choose a location

Unzip the package, and move the files to a folder on your hard disk. For example:

    /code/

Avoid using spaces or non-ASCII characters in folder names above hTools, since it may cause a few problems.

### 3. Add the module to Python

Create a simple text file, containing the path to the `Lib` folder inside `hTools2`:

	/code/hTools2/Lib/

Save this file as `hTools2.pth` in the `site-packages` folder for the desired Python(s):

	/Library/Python/2.5/site-packages/hTools2.pth
	/Library/Python/2.6/site-packages/hTools2.pth

And that’s it.

### 4. Test the installation

To check if `hTools2` has been installed successfully, try to run this line in the RoboFont scripting window or in Terminal:

	import hTools2
    
If no error message is returned, the installation was successful.

### 5. Configure the Extensions menu

To have the dialogs in the hTools2 `Scripts` folder appear in RoboFont’s `Extensions` menu, select it as the root path for Python scripts in the `Preferences` window.

### 6. Configure keyboard shortcuts

As an optional last step, it is also possible to configure keyboard shortcuts for hTools scripts in RoboFont.

As a reference, my current keyboard shortcuts are collected [here](http://hipertipo.com/content/htools2/dialogs/shortcuts/).

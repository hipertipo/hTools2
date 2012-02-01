Installation
============

### 1. Get the code

Download the latest version of hTools2 from the [zip package](https://github.com/gferreira/hTools2/zipball/master), or pull it directly from the [git repository](https://github.com/gferreira/hTools2).

Move the folder to the desired location on your hard disk, for example `/code/`.

### 2. Add the module to Python

Create a simple text file named `hTools2.pth`, containing the path to the `Lib` folder in hTools2: 

```
/code/hTools2/Lib/
```

Save this file in the `site-packages` folder for the desired Python, for example:

```
/Library/Python/2.X/site-packages
```

### 3. Test installation

To test if `hTools2` is installed, try to run this in the RoboFont scripting window:

```
import hTools2
```
    
If no error message is returned, the library has been installed sucessfully.

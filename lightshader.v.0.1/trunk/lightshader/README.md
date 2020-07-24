# README #

LightShaders is a toolbox for artists working in Lookdev/Lighting in Maya. It consists of several convenience tools to make an artist life easier. 

### How do I get set up? ###

To install the toolbox follow the steps below: 

1. First download the latest version from the download section, or follow this link:
*https://bitbucket.org/arvidurs/lightshader/downloads/*

2. Locate your Maya.env file which is in the following directories depending on your os:


```
#!python

Windows XP
\Documents and Settings\<username>\My Documents\maya

Windows Vista and Windows 7 and newer
\Users\<username>\Documents\maya

Mac OS X
~<username>/Library/Preferences/Autodesk/maya

Linux (64-bit)
~<username>/maya
```



and **add** this lines to the **Maya.env** file.


```
#!python
MAYA_MODULE_PATH=/YOUR_PATH/trunk/lightshader/maya;
PYTHONPATH=/YOUR_PATH/trunk;
```
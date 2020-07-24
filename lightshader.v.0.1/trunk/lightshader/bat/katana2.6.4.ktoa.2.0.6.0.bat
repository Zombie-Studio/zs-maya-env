::@ECHO OFF

rem
rem Set the following env vars according to your licensing setup and
rem installation paths. Note the maya/mtoa paths for the ArnoldXGen node to
rem run properly.
rem


:: CHANGE THESE PATHS HERE ::
set "TRUNK=D:\WORK\Development\Dev\trunk"
set "KATANA_HOME=C:\Program Files\Katana2.6v4"
set "ARNOLDTREE=C:\solidangle\mtoadeploy\2018"
set "KTOA_HOME=C:\solidangle\KtoA-2.0.6.0-kat2.6-windows"
set "MAYA_PATH=C:\Program Files\Autodesk\Maya2018"

:: SETTING USER PATHS
set "LIGHTSHADER_ROOT=%TRUNK%\lightshader"
set "LIGHTSHADER_RESOURCES=%LIGHTSHADER_ROOT%\katana\Resources"
set "LIGHTSHADER_MATLIB=%LIGHTSHADER_ROOT%\katana\Library"

:: ARNOLD PATHS
set "ARNOLD_PLUGIN_PATH=%ARNOLDTREE%\bin;%LIGHTSHADER_ROOT%\osl"
set "MTOA_PATH=%ARNOLDTREE%"

set DEFAULT_RENDERER=arnold
set "KATANA_TAGLINE=With KtoA 2.0.6.0 and Arnold 5.0.2.0"
set "PATH=$ARNOLDTREE\bin:$KATANA_HOME:$PATH"
set "path=%KTOA_HOME%\bin;%path%"
set "KATANA_RESOURCES=%KTOA_HOME%;%LIGHTSHADER_RESOURCES%;"
"%KATANA_HOME%\bin\katanaBin.exe"
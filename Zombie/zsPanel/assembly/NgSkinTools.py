"""
SCRIPT NgSkinTools
AUTHOR: Isaac Buzzola/isaac.buzzola@zombiestudio.com.br
DATE: Friday 11 December 2020 15:53

SCRIPT FOR ZOMBIE STUDIO
"""

try:
    from maya import cmds

    from ngSkinTools.ui.mainwindow import MainWindow
    MainWindow.open()
except Exception as error:
    print(error)
"""
SCRIPT StudioLibrary
AUTHOR: Thiago Silva/thiago.silva@zombiestudio.com.br
DATE: Friday 05 March 2021 08:41

SCRIPT FOR ZOMBIE STUDIO
"""

import os
import sys

try:
    zombieEnv = os.path.join(os.environ['APPDATA'], 'zombieEnv')

    path = os.path.join(zombieEnv, 'Zombie', 'zsPanel', 'animation', 'studiolibrary', 'src')
    path = os.path.normpath(path)

    path_zombie = os.path.join(zombieEnv, 'Zombie', 'zsPanel', 'animation', 'studiolibrary')
    path_zombie = os.path.normpath(path_zombie)

    if not os.path.exists(path):
        print(r'The source path "{}" does not exist!'.format(path))

    if path not in sys.path:
        sys.path.insert(0, path)

    if not os.path.exists(path_zombie):
        print(r'The source path "{}" does not exist!'.format(path))

    if path_zombie not in sys.path:
        sys.path.insert(0, path_zombie)

    import zombie
    reload(zombie)
    zombie.zombieSettings()

    import studiolibrary
    reload(studiolibrary)
    studiolibrary.reload()
    studiolibrary.main()
except Exception as error:
    print(error)
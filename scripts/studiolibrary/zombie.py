import json
import os
import sgtk
from maya import cmds

APP = sgtk.platform.current_engine()
PROJECT_PATH = APP.tank.project_path
TK = sgtk.sgtk_from_path(PROJECT_PATH)
CTX = TK.context_from_path(PROJECT_PATH)
CONFIG = APP.context.tank.pipeline_configuration

class zombieSettings:
    def __init__(self):
        self.project_library = os.path.join(PROJECT_PATH, self.getPipe(), 'data', 'StudioLibrary')
        self.types = []
        self.projectId = CTX.project['id']

        self.createDataBase()
        self.setPathSettings()

        self.assets = APP.shotgun.find('Asset', [['project.Project.id', 'is', self.projectId]], ['code', 'sg_asset_type'])
        self.sequence = APP.shotgun.find('Sequence', [['project.Project.id', 'is', self.projectId]], ['code'])
        self.shots = APP.shotgun.find('Shot', [['project.Project.id', 'is', self.projectId]], ['code', 'sg_sequence'])

        self.getTypes()
        self.createAssets()
        self.createShots()

    def getTypes(self):
        for asset in self.assets:
            self.types.append(asset['sg_asset_type'])
        self.types = list(dict.fromkeys(self.types))

    def createAssets(self):
        if not os.path.exists(os.path.join(self.project_library, 'Assets')):
            os.mkdir(os.path.join(self.project_library, 'Assets'))

        for type in self.types:
            if not os.path.exists(os.path.join(self.project_library, 'Assets', type)):
                os.mkdir(os.path.join(self.project_library, 'Assets', type))

            for asset in self.assets:
                if asset['sg_asset_type'] == type:
                    if not os.path.exists(os.path.join(self.project_library, 'Assets', type, asset['code'])):
                        os.mkdir(os.path.join(self.project_library, 'Assets', type, asset['code']))

    def createShots(self):
        if not os.path.exists(os.path.join(self.project_library, 'Shots')):
            os.mkdir(os.path.join(self.project_library, 'Shots'))

        for seq in self.sequence:
            if not os.path.exists(os.path.join(self.project_library, 'Shots', seq['code'])):
                os.mkdir(os.path.join(self.project_library, 'Shots', seq['code']))

            for shot in self.shots:
                if seq['code'] == shot['sg_sequence']['name']:
                    if not os.path.exists(os.path.join(self.project_library, 'Shots', seq['code'], shot['code'])):
                        os.mkdir(os.path.join(self.project_library, 'Shots', seq['code'], shot['code']))

    def createDataBase(self):
        if not os.path.exists(self.project_library):
            os.makedirs(self.project_library)
            os.mkdir('{}\\.studiolibrary'.format(self.project_library))
            databse = '{}\\.studiolibrary\\database.json'.format(self.project_library)
            with open(databse, 'w') as outfile:
                json.dump({}, outfile)

    def setPathSettings(self):
        pathStudiLibrarySettings = os.path.join(os.environ['appdata'], 'StudioLibrary', 'LibraryWidget.json')
        with open(pathStudiLibrarySettings) as data:
            settings = json.load(data)
        settings['Default']['path'] = self.project_library
        with open(pathStudiLibrarySettings, 'w') as outSettings:
            json.dump(settings, outSettings)

    def getPipe(self):
        if 'Anim' not in CONFIG.get_name():
            return '02_prod'
        else:
            return '06_prod_anim'

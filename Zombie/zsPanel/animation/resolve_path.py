from glob import glob
import json
path = "R:\\Zombie Dropbox\\PROJETOS\\2021\\2153_AREA_23_LITTLE_SUGAR\\06_prod_anim\\data\\StudioLibrary\\Assets\\Character\\LilSugar\\Bocas\**"


folders = glob(path)
# print(folders[0])
# with open(folders[0]) as json_file:
#     data = json.load(json_file)
#     print(data)

for file in folders:
    f = open(file, "r")
    print(f.read())
#     with open(file,) as json_file:
#         data = json.load(json_file)
#         print(data)

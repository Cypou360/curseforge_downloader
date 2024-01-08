#A script to automatically download and install a forge server with mods from a manifest.json file

import requests
import json
import os

def read_manifest(path):
    with open(path, 'r') as f:
        return json.load(f)

def download_forge(file, directory):
    MCversion = file["minecraft"]["version"]
    forgeVersion = file["minecraft"]["modLoaders"][0]["id"][6:]
    forgeURL = f'https://maven.minecraftforge.net/net/minecraftforge/forge/{MCversion}-{forgeVersion}/forge-{MCversion}-{forgeVersion}-installer.jar'
    print(f'Downloading forge {forgeVersion}')
    open(directory + 'forge.jar', 'wb').write(requests.get(forgeURL).content)
    os.chdir(directory)
    os.system(f'java -jar {directory}forge.jar --installServer')
    os.remove(f'{directory}forge.jar')
    open(f'{directory}eula.txt', 'w').write('eula=true')

def get_mod_info(modId, fileId):
    header = {
        'Accept': 'application/json',
        'x-api-key': token
    }
    url = f'https://api.curseforge.com/v1/mods/{modId}/files/{fileId}'
    r = requests.get(url, headers=header)
    return r.json()["data"]["downloadUrl"], r.json()["data"]["fileName"]


def download_mods(file,directory):
    print('Starting mod download')
    if not os.path.exists(directory+'/mods'):
        os.mkdir(directory+'/mods')
    directory = directory+'/mods/'
    for i in file["files"]:
        modId = i["projectID"]
        fileId = i["fileID"]
        modURL, modName = get_mod_info(modId, fileId)
        print(f'Downloading {modName}')
        open(directory + modName, 'wb').write(requests.get(modURL).content)
        print(f'Downloaded {modName}')

def load_config():
    if not os.path.exists('config.json'):
        open('config.json', 'w').write('{"installDirectory": "", "token": ""}')
        print('Please fill out the config.json file')
        exit()
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config["Modpack directory"], config["API key"]

def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print(f'Created {path}')
    else:
        print(f'{path} already exists')

def get_modpack_name(file):
    out = file["name"]
    for i in out:
        if i in [' ']:
            out = out.replace(i, '_')
    return out

    return out
if __name__ == '__main__':
    manifestLocation = input('Enter the absolute path to your manifeste.json: ')
    installDirectory, token = load_config()
    manifest = read_manifest(manifestLocation)
    installDirectory = installDirectory +"/" + get_modpack_name(manifest) + '/'
    create_directory(installDirectory)
    download_forge(manifest, installDirectory)
    download_mods(manifest, installDirectory)
    print("Done")
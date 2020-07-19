
import re
import os
import sys
import shlex
import shutil
import subprocess
from os import listdir
from os.path import isfile, join

class NodeConfig:
    version = '0.9.0-d'
    system = 'x86_64-unknown-linux-gnu'
    network = 'testnet'


class WitnetConfig(object):
    NODE_COUNT = 1
    PATH = "/home/witnet"
    VERSION = "latest"
    # network options: testnet, mainnet, testnet_local
    NETWORK = "testnet"
    SYSTEM = "x86_64-unknown-linux-gnu"



conf = WitnetConfig()

VERSION = 'latest'
COMPONENT = 'node'
MODE = 'server'

def get_latest_version():
    command = ['curl',
               'https://github.com/witnet/witnet-rust/releases/latest',
               '--cacert',
               '/etc/ssl/certs/ca-certificates.crt']

    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    output = process.stdout.readline()
    if output:
        print(output.strip())
    rc = process.poll()
    return re.findall(r'"([^"]*)"', output.strip().decode("utf-8"))[0].split('/')[-1]


#print(get_latest_version())
conf.VERSION = get_latest_version()
system = 'x86_64-unknown-linux-gnu'
filename = f'witnet-{conf.VERSION}-{conf.SYSTEM}.tar.gz'

url = f'https://github.com/witnet/witnet-rust/releases/download/{conf.VERSION}/{filename}'
print(f'Version: {conf.VERSION}')
print(filename)


def download_witnet_github():
    command = ['curl', '-L', url, '-o', f'tmp/{filename}', '--cacert', '/etc/ssl/certs/ca-certificates.crt']
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    print(f'Downloading {url}')
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    output = process.stdout.readline()
    if output:
        print(output.strip())
    rc = process.poll()


download_witnet_github()
num_nodes = 3
folder_name = f'node_0'


def extract_node_targz_to(path=None):

    command = ['tar', '-zxf', f'tmp/{filename}', '--directory', path]
    # os.mkdir('tmp')
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    output = process.stdout.readline()
    if output:
        print(output.strip())
    rc = process.poll()
    print(f'Extracted {filename} to {path} : ')


def create_nodes(config=None):
    node_dirs = []
    node_path = os.path.join(f'{config.PATH}/{config.NETWORK}/{config.VERSION}')
    print(f'node path: {node_path}')
    if not os.path.exists(f'{config.PATH}/{config.NETWORK}'):
        os.mkdir(f'{config.PATH}/{config.NETWORK}')
    if not os.path.exists(f'{config.PATH}/{config.NETWORK}/{config.VERSION}'):
        os.mkdir(f'{config.PATH}/{config.NETWORK}/{config.VERSION}')
    print(f'Created directory: {config.PATH}/{config.NETWORK}/{config.VERSION}')
    if isinstance(config, WitnetConfig):
        node_dirs.append(f'{config.PATH}/{config.NETWORK}/{config.VERSION}')


    print(node_dirs)
    for i, node_dir in enumerate(node_dirs):
        print(i, node_dir)
        if not os.path.exists(node_dir):
            os.mkdir(node_dir)
        extract_node_targz_to(path=node_dir)
        db_path = os.path.join(node_path, '.witnet')
        print(db_path)
        if not os.path.exists(db_path):
            os.mkdir(db_path)

        node_config_path = os.path.join(db_path, 'config')
        print(node_config_path)

        if not os.path.exists(node_config_path):
            os.mkdir(node_config_path)

        only_files = [f for f in listdir(node_path)]
        genesis_file = 'genesis_block.json'
        toml_file = 'witnet.toml'
        shutil.copy(os.path.join(node_path, genesis_file), os.path.join(node_config_path, genesis_file))
        print(f'Created {os.path.join(node_config_path, genesis_file)}')
        shutil.copy(os.path.join(node_path, toml_file), os.path.join(node_config_path, f'node-{i}.toml'))
        print(f'Created {os.path.join(node_config_path, f"node-{i}.toml")}')
        print(only_files)


def cleanup(folder=None):
    if isinstance(folder, str):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                print(f'Deleting file: {file_path}')
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

print(os.getcwd())
# cleanup('tmp/')


# download_witnet_github()

create_nodes(config=conf)

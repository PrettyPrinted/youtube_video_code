import hashlib
import os 
import sys

from datetime import datetime

PROJECT_DIR = 'project'

def hash_object(data):
    oid = hashlib.sha1(data).hexdigest()
    with open(f'objects/{oid}', 'wb') as f:
        f.write(data)
    return oid

def get_object(oid):
    with open(f'objects/{oid}', 'rb') as f:
        return f.read()

def save_directory():
    tree_objs = []
    with os.scandir(PROJECT_DIR) as it:
        for entry in it:
            if entry.is_file():
                with open(f'{PROJECT_DIR}/{entry.name}', 'rb') as f:
                    oid = hash_object(f.read())
                    tree_objs.append((oid, entry.name))
    
    tree = ''.join(f'{oid} {name}\n' for oid, name in tree_objs)
    tree_oid = hash_object(tree.encode())

    with open('.history', 'a') as f:
        f.write(f'{datetime.now().isoformat()} {tree_oid}\n')

    return tree_oid

def restore_directory(tree_oid):
    tree = get_object(tree_oid)
    for entry in tree.decode().splitlines():
        oid, name = entry.split()
        with open(f'{PROJECT_DIR}/{name}', 'wb') as f:
            f.write(get_object(oid))

if __name__ == '__main__':
    if sys.argv[1] == '--save':
        save_directory()
    elif sys.argv[1] == '--restore':
        restore_directory(sys.argv[2])
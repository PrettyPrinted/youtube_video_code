from time import time

with open('db.sqlite3', 'rb') as fi, open(f'db.sqlite3.backup.{time()}', 'wb') as fo:
    chunk_size = 4096

    while True:
        data = fi.read(chunk_size)
        if not data:
            break
        fo.write(data)
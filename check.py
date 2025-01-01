#!/usr/bin/env python3

import os

def get_directory_listing(root):
    files = [os.path.join(dirpath[2:], f) for (dirpath, dirnames, filenames) in
             os.walk(root) if not '.git' in dirpath for f in filenames]
    with open(os.path.join(root, 'ignorelist'), 'r') as f:
        ignored = [line for line in f.read().splitlines()]
        for f in ignored:
            print(f'Ignoring {f}')
        filtered = [f for f in files if f not in ignored]
    length = len(files)
    print(f'Read {length} files from {root}')
    return filtered

def read_index(root):
    files = []
    with open(os.path.join(root, 'index'), 'r') as f:
        for line in f.read().splitlines():
            if line.startswith('#') or not line:
                continue

            (fname, *link) = line.split(',')
            if len(link) == 0 or not link[0]:
                files.append((fname, None))
            elif len(link) > 1:
                files.append((fname, -1))
            else:
                files.append((fname, link[0]))

    return files

if __name__ == '__main__':
    files = get_directory_listing('.')
    index = read_index('.')

    for f in files:
        err = 0
        found = [item for item in index if item[0] == f]
        found_len = len(found)
        if found_len == 0:
            print(f'File `{f}` not found in index!')
            err = 1
            continue
        elif found_len > 1:
            print(f'File `{f}` is duplicated in index!')
            err = 2
            continue
        (fname, link) = found[0]
        if link is None:
            print(f'File `{f}` has no links!')
            err = 3
        elif link == -1:
            print(f'File `{f}` has too many links!')
            err = 4
    if err != 0:
        exit(err)

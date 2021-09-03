#! /usr/bin/env python3

import common, os, pathlib, sys, zipfile
from os.path import *


def parents(path):
    res = []
    parent = path.parent
    while '.' != str(parent):
        res.insert(0, parent)
        parent = parent.parent
    return res


def main():
    skia_path = os.path.join(os.path.dirname(__file__), os.pardir, 'skia');
    print("archiving...", skia_path)
    os.chdir(skia_path)

    build_type = common.build_type()
    version = common.version()
    machine = common.machine()
    system = common.system()
    classifier = common.classifier()

    globs = [
        '[!.git]*/*'
    ]

    target = 'Skia-' + version + '-' + system + '-' + build_type + '-' + machine + classifier + '.zip'
    print('> Writing', target)

    rootdir = os.path.abspath(os.getcwd())
    list_ = [rootdir]
    zip = zipfile.ZipFile(os.path.join(os.pardir, target), 'w', compression=zipfile.ZIP_DEFLATED)
    while len(list_) > 0:
        dir_ = list_.pop()
        files_ = os.listdir(dir_)
        for i in range(0, len(files_)):
            path = os.path.join(dir_, files_[i])
            if os.path.isdir(path):
                if not files_[i] == ".git":
                    list_.append(path)
            else:
                #print(path[len(rootdir) + 1:])
                zip.write(path, path[len(rootdir) + 1:])

    return 0


if __name__ == '__main__':
    sys.exit(main())

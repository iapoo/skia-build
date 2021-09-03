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
        'out/' + build_type + '-' + machine + '/*.a',
        'out/' + build_type + '-' + machine + '/*.lib',
        'out/' + build_type + '-' + machine + '/icudtl.dat',
        'include/**/*',
        'modules/particles/include/*.h',
        'modules/skottie/include/*.h',
        'modules/skottie/src/*.h',
        'modules/skottie/src/animator/*.h',
        'modules/skottie/src/effects/*.h',
        'modules/skottie/src/layers/*.h',
        'modules/skottie/src/layers/shapelayer/*.h',
        'modules/skottie/src/text/*.h',
        'modules/skparagraph/include/*.h',
        'modules/skplaintexteditor/include/*.h',
        'modules/skresources/include/*.h',
        'modules/sksg/include/*.h',
        'modules/skshaper/include/*.h',
        'modules/skshaper/src/*.h',
        'modules/svg/include/*.h',
        'src/core/*.h',
        'src/gpu/gl/*.h',
        'src/utils/*.h',
        'third_party/externals/angle2/LICENSE',
        'third_party/externals/angle2/include/**/*',
        'third_party/externals/freetype/docs/FTL.TXT',
        'third_party/externals/freetype/docs/GPLv2.TXT',
        'third_party/externals/freetype/docs/LICENSE.TXT',
        'third_party/externals/freetype/include/**/*',
        'third_party/externals/icu/source/common/**/*.h',
        'third_party/externals/libpng/LICENSE',
        'third_party/externals/libpng/*.h',
        'third_party/externals/libwebp/COPYING',
        'third_party/externals/libwebp/PATENTS',
        'third_party/externals/libwebp/src/dec/*.h',
        'third_party/externals/libwebp/src/dsp/*.h',
        'third_party/externals/libwebp/src/enc/*.h',
        'third_party/externals/libwebp/src/mux/*.h',
        'third_party/externals/libwebp/src/utils/*.h',
        'third_party/externals/libwebp/src/webp/*.h',
        'third_party/externals/harfbuzz/COPYING',
        'third_party/externals/harfbuzz/src/*.h',
        'third_party/externals/swiftshader/LICENSE.txt',
        'third_party/externals/swiftshader/include/**/*',
        'third_party/externals/zlib/LICENSE',
        'third_party/externals/zlib/*.h',
        "third_party/icu/*.h"
    ]

    target = 'Skia-' + version + '-' + system + '-' + build_type + '-' + machine + classifier + '.zip'
    print('> Writing', target)

    rootdir = os.path.abspath(os.getcwd())
    zip = zipfile.ZipFile(os.path.join(os.pardir, target), 'w', compression=zipfile.ZIP_DEFLATED)
    if True:
        dirs = set()
        for glob in globs:
            for path in pathlib.Path().glob(glob):
                if not path.is_dir():
                    for dir in parents(path):
                        if not dir in dirs:
                            zip.write(str(dir))
                            dirs.add(dir)
                    zip.write(str(path))
    else:
        list_ = [rootdir]
        while len(list_) > 0:
            dir_ = list_.pop()
            files_ = os.listdir(dir_)
            for i in range(0, len(files_)):
                path = os.path.join(dir_, files_[i])
                if os.path.isdir(path):
                    if not files_[i] == ".git":
                        list_.append(path)
                else:
                    # print(path[len(rootdir) + 1:])
                    zip.write(path, path[len(rootdir) + 1:])

    return 0


if __name__ == '__main__':
    sys.exit(main())

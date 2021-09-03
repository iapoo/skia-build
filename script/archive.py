#! /usr/bin/env python3

import common, os, pathlib, sys, zipfile

def parents(path):
  res = []
  parent = path.parent
  while '.' != str(parent):
    res.insert(0, parent)
    parent = parent.parent
  return res

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))
  
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
  
  with zipfile.ZipFile(os.path.join(os.pardir, target), 'w', compression=zipfile.ZIP_DEFLATED) as zip:
    dirs = set()
    for glob in globs:
      for path in pathlib.Path().glob(glob):
        if not path.is_dir():
          for dir in parents(path):
            if not dir in dirs :
              zip.write(str(dir))
              dirs.add(dir)
          zip.write(str(path))

  return 0

if __name__ == '__main__':
  sys.exit(main())

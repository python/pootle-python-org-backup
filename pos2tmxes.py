#!/usr/bin/env python
from os import walk
from pathlib import Path
from subprocess import call


def convert():
    for dirpath, dirnames, filenames in walk('pos/locale/python'):
        for filename in filenames:
            if filename.endswith('.po'):
                directory = Path(dirpath)
                language = directory.name
                source = directory / filename
                target_directory = Path('tmxes') / language
                target = target_directory / f'{source.stem}.tmx'
                target_directory.mkdir(parents=True, exist_ok=True)
                call(
                    f'po2tmx --language {language} {source} {target}',
                    shell=True
                )


if __name__ == '__main__':
    convert()

#!/usr/bin/env python
"""Adds matching translations in place of missing ones."""
from argparse import ArgumentParser
from os import walk
from pathlib import Path
from subprocess import call


def merge(translationdirectory: str) -> None:
    for dirpath, dirnames, filenames in walk(Path(translationdirectory)):
        for filename in filenames:
            if filename.endswith(".po"):
                directory = Path(dirpath)
                set = directory.name
                source = directory / filename
                potential_target = Path("pos/locale/python/pl") / source.name
                if potential_target.exists():
                    merge_po(potential_target, source)
                else:
                    potential_target = Path("pos/locale/python/pl") / f"{set}.po"
                    if potential_target.exists():
                        merge_po(potential_target, source)
                    else:
                        print(f"no match in 3.1 translations for {source}")


def merge_po(potential_target, source):
    call(
        f"msgcat --use-first {source} {potential_target} -o tmpsum.po",
        shell=True,
    )
    call(
        f"msgmerge tmpsum.po {source} --output tmpmerged.po",
        shell=True,
    )
    call(
        "msgattrib tmpmerged.po --no-obsolete -o tmpcleaned.po",
        shell=True,
    )
    with open("tmpcleaned.po") as cleaned, open(source, "w") as output:
        cleanedlines = cleaned.readlines()
        l = cleanedlines.index('"Language: pl\\n"\n')
        outputlines = (
            cleanedlines[:l]
            + cleanedlines[l + 1 : l + 4]
            + cleanedlines[l : l + 1]
            + cleanedlines[l + 4 :]
        )
        output.writelines(outputlines)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('translationdirectory')
    args = parser.parse_args()

    merge(args.translationdirectory)

#!/usr/bin/env python
"""Adds matching translations in place of missing ones."""
from argparse import ArgumentParser
from os import walk
from pathlib import Path
from subprocess import call


def merge(translationdirectory: str, language: str) -> None:
    for dirpath, dirnames, filenames in walk(Path(translationdirectory)):
        for filename in filenames:
            if filename.endswith(".po"):
                directory = Path(dirpath)
                parent = directory.name
                source = directory / filename
                old_translations_directory = Path("pos/locale/python") / language
                potential_target = old_translations_directory / source.name
                if potential_target.exists():
                    merge_po(potential_target, source)
                elif (
                    potential_target := old_translations_directory / f"{parent}.po"
                ).exists():
                    merge_po(potential_target, source)
                else:
                    print(f"no match in 3.1 translations for {source}")


def merge_po(potential_target: Path, source: Path) -> None:
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
    parser.add_argument('language')
    args = parser.parse_args()

    merge(args.translationdirectory, args.language)

#!/usr/bin/env -S ${HOME}/bin/.venv3/bin/python

from os.path import exists, join
import sys
import re
import json
import massedit

with open("wasis.json", 'r') as fp:
    wasis = json.load(fp)

def updateLine(line):
    """ Check the line and update if needed """
    changed = False
    m = selpat.search(line)
    if m:
        sel = m.group(3)
        if sel in wasis:
            changed = True
            sel2 = wasis.get(sel)
            line = selpat.sub(r"\1\2: selectors['" + sel2 + r"']\4", line)
            print(line)

    return changed, line


selpat = re.compile(r"(^.*)(\w+)\:\s+selectors\['(.*)'\](.*$)")


for file in sys.argv[1:]:
    if exists(file):
        print(f"File exists {file}")
        lines = []
        wasChanged = False
        with open(file, 'r') as fp:
            for line in fp:
                changed, line = updateLine(line)
                lines.append(line)
                wasChanged = wasChanged or changed

        if wasChanged:
            with open(file, 'w') as fp:
                for line in lines:
                    fp.write(line)
            print(f"File {file} was updated")
    else:
        print(f"File {file} does not exist")


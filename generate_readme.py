#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

from logseq2md import get_markdown_files

TAG_MAP = {
    "#hráčskápostava" : "Hráčské Postavy",
    "#město": "Města",
    "#místo": "Místa",
    "#postava": "Postavy",
    "#loď": "Lodě",
    "#organizace": "Organizace",
    "#pašeráci": "Pašerácké Záležitosti",
    "#předmět": "Předměty"
}

FILE_START = [
    "# D&D - Duchové Slaniska\n",
    "Poznámky ze schůzek Dungeons and Dragons z dobrodružství Duchové Slaniska vyprávěného Ambrym. v letech 2023-Nyní\n",
    "## Linky na poznámky:\n"
]

tag_files = {}
file_headers = {}

def generate_readme(markdown_dir: str = "./pure_markdown/"):
    populate_tag_files_dictionary(markdown_dir)
    
    file = codecs.open("README.md", "w+", "utf-8")
    file.writelines(FILE_START)
    for tag in TAG_MAP.keys():
        if not tag in tag_files:
            continue
        lines = [f"### {TAG_MAP[tag]}\n"]
        for file_name in tag_files[tag]:
            lines.append(f"- [{file_headers[file_name]}]({markdown_dir + file_name})\n")
        file.writelines(lines)
    file.close()


def populate_tag_files_dictionary(markdown_dir: str):
    files = get_markdown_files(markdown_dir)
    for file_name in files:
        file = codecs.open(markdown_dir + file_name, "r", "utf-8")
        header = file.readline()
        if header[:2] != "# ":
            continue
        file_headers[file_name] = header[2:].strip()
        line = file.readline()
        if line[:3] != "- #" or line[:4] == "- # " or line[:4] == "- ##":
            continue
        tags = line[2:].strip().split(' ')
        for tag in tags:
            if tag in tag_files:
                tag_files[tag].append(file_name)
            else:
                tag_files[tag] = [file_name]


generate_readme()

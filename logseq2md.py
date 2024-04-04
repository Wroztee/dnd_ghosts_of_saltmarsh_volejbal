#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs

IMAGE_FILE_EXTENSIONS = [".png", ".jpg", ".svg", ".pdf"]

section_links = {}

def get_markdown_files(path: str = "./pages/"):
    md_files = []
    files = os.listdir(path)
    for file in files:
        if file[-3:] == ".md":
            md_files.append(file)
    return md_files


def reformat_markdown_file(file_name : str, in_dir: str, out_dir: str):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    adjusted_file_name = file_name.replace(' ', '_')
    in_file = codecs.open(in_dir + file_name, "r", "utf-8")
    out_file = codecs.open(out_dir + adjusted_file_name, "w+", "utf-8")

    lines = in_file.readlines()
    
    i = 0
    while (i < len(lines)):
        if register_section_link(lines, i, adjusted_file_name) or remove_timestamps(lines[i]):
            lines.pop(i)
            continue
        lines[i] = lines[i].replace("- ![", "![")
        lines[i] = reformat_double_bracket_links(lines[i])
        lines[i] = remove_empty_line_point(lines[i])
        lines[i] = reformat_checkboxes(lines[i])
        lines[i] = remove_image_sizes(lines[i])
        lines[i] = add_file_extension_to_links(lines[i])
        i += 1

    # Add Page Title
    if lines[0][0:1] != "# ":  # Check if first line is a header
        lines.insert(0, f"# {file_name.replace('.md', '')}\n")

    out_file.writelines(lines)

    in_file.close()
    out_file.close()


def reformat_double_bracket_links(line: str):
    new_line = line
    start_index = new_line.find("[[")
    while start_index != -1:
        end_index = new_line.find("]]")
        content = new_line[start_index + 2 : end_index]
        new_line = new_line.replace("[[", "[", 1).replace("]]", f"]({content})", 1)
        start_index = new_line.find("[[")
    return new_line


def remove_empty_line_point(line: str):
    if line.strip() == "-":
        return "\n"
    return line


def remove_timestamps(line: str):
    strip_line = line.strip()
    if strip_line == ":LOGBOOK:" or strip_line == ":END:" or strip_line[:6] == "CLOCK:":
        return True
    return False


def reformat_checkboxes(line: str):
    indent = line.find('-')
    strip_line = line.strip()
    if strip_line[:7] == "- DONE ":
        return ' ' * indent + f"- [x] ~~{strip_line[7:]}~~\n"   # Keep indentation, add checked box, remove DONE text, add strikethrough (with ~~)
    if strip_line[:8] == "- DOING ":
        return ' ' * indent + f"- [ ] **DOING** {strip_line[8:]}\n" # Keep indentation, add unchecked box, make DOING bold
    if strip_line[:7] == "- TODO ":
        return ' ' * indent + f"- [ ] **TODO** {strip_line[8:]}\n"  # Keep indentation, add unchecked box, make TO DO bold
    return line


def remove_image_sizes(line: str):
    new_line = line
    start_index = new_line.find("){:height ")
    while start_index != -1:
        end_index = new_line.find("}")
        new_line = new_line[:start_index + 1] + new_line[end_index + 1:]
        start_index = new_line.find("){:height ")
    return new_line


def add_file_extension_to_links(line: str):
    new_line = line
    start_find = 0
    while start_find != -1:
        start_find = new_line.find("](", start_find)
        if start_find == -1:
            break
        content_start = start_find
        start_find = new_line.find(")", start_find)
        if start_find != -1 and not new_line[start_find - 4 : start_find] in IMAGE_FILE_EXTENSIONS and new_line[start_find - 3 : start_find] != ".md":
            new_line = new_line[:content_start] + new_line[content_start:start_find].replace(' ', '_') + new_line[start_find:].replace(")", ".md)", 1)
    return new_line


def register_section_link(lines: list, index: int, file_name: str):
    if index == 0:
        return False
    strip_line = lines[index].strip()
    if strip_line[:5] == "id:: ":
        link_name = f"{file_name}#{lines[index - 1].strip().replace('#', '').replace(' ', '-').lower().strip('-')}"
        link_id = strip_line[5:]
        section_links[link_id] = link_name
        return True
    return False


def reformat_file_section_links(file_name : str, dir: str):
    adjusted_file_name = file_name.replace(' ', '-')
    lines = []

    file = codecs.open(dir + adjusted_file_name, "r", "utf-8")
    lines = file.readlines()
    file.close()

    for i in range(len(lines)):
        for id in section_links.keys():
            lines[i] = lines[i].replace(f"{id}.md", section_links[id])
        lines[i] = lines[i].replace(adjusted_file_name, '')
    
    file = codecs.open(dir + adjusted_file_name, "w+", "utf-8")
    file.writelines(lines)
    file.close()
        

def reformat_logseq_pages(old_dir: str = "./pages/", new_dir: str = "./pure_markdown/"):
    for file_name in get_markdown_files(old_dir):
        reformat_markdown_file(file_name, old_dir, new_dir)

    for file_name in get_markdown_files(new_dir):
        reformat_file_section_links(file_name, new_dir)


reformat_logseq_pages()
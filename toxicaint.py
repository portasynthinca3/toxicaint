#!/usr/bin/env python
from os import path
import os
from sys import argv
import shutil
from pathlib import Path

import markovify
import lxml.html

ELEMENT_SELECTOR = "h1, h2, h3, h4, h5, h6, p, a, div, span, figcaption, li, td, abbr, footer"

if len(argv) != 3:
    print("Usage: toxicaint.py [source] [destination]")
    exit(1)
_, SOURCE, DESTINATION = argv

CONTAINING_DIR = path.dirname(path.realpath(__file__))
TEXTS_DIR = path.join(CONTAINING_DIR, "texts")
TEXT_FILES = os.listdir(TEXTS_DIR)

print("Loading texts.")
MODELS = []

for text_name in TEXT_FILES:
    text_path = path.join(TEXTS_DIR, text_name)
    with open(text_path, "r") as file:
        text = file.read()

    model = markovify.Text(text)
    MODELS.append(model)
    print(f"  Loaded {path.basename(text_path)}")

MODEL = markovify.combine(MODELS)
MODEL.compile(inplace=True)
print(f"  Done. Loaded {len(TEXT_FILES)} text(s).")

print("Copying source to destination.")
shutil.rmtree(DESTINATION, ignore_errors=True)
shutil.copytree(SOURCE, DESTINATION)
print("  Done.")

print("Processing HTML files.")
HTML_FILES = list(Path(DESTINATION).rglob("*.html"))

def generate_slop(target_length):
    slop = ""
    while len(slop) < target_length:
        slop_len = max(target_length, 100)
        slop += (MODEL.make_short_sentence(slop_len) or "") + " "
    slop = slop[:target_length]
    return slop

for html_path in HTML_FILES:
    readable_path = str(html_path)[len(DESTINATION):]
    with open(html_path, "r") as file:
        html_text = file.read()

    try:
        html = lxml.html.fromstring(html_text)
        elements = html.cssselect(ELEMENT_SELECTOR)
        element_cnt, char_cnt, skip_cnt, fail_cnt = 0, 0, 0, 0

        for element in elements:
            if not element.text:
                skip_cnt += 1
                continue

            slop = generate_slop(len(element.text))
            if not slop:
                element.text = ""
                fail_cnt += 1
                continue
            element.text = slop            
            char_cnt += len(slop)
            element_cnt += 1

            if element.tail and len(element.tail.strip("\r\n ")):
                slop = generate_slop(len(element.tail))
                if not slop:
                    element.tail = ""
                    fail_cnt += 1
                    continue
                element.tail = slop

        html_text = lxml.html.tostring(html)
        with open(html_path, "wb") as file:
            file.write(html_text)
        print(f"  Processed {readable_path}: {element_cnt} element(s) ({skip_cnt} skipped), {char_cnt} character(s), {fail_cnt} failure(s).")
    except Exception as ex:
        print(f"  Failed to process {readable_path}: {ex}")

print(f"  Done. Processed {len(HTML_FILES)} file(s).")
print("Done.")

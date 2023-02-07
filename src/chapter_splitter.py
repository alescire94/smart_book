import json
import os
import re

from tqdm import tqdm

from src.constants import (
    TRANSCRIPTIONS_PATH,
    SPLITTER_OUTPUT_PATH,
    CHAPTER_PAGE_MAPPING,
)
from src.patterns import SUBCHAPTER_PATTERN


def split():
    if os.path.exists(SPLITTER_OUTPUT_PATH):
        return
    book2chapter2page = {}
    dumps = []
    with open(CHAPTER_PAGE_MAPPING) as f:
        for line in f.readlines():
            book, chapter, page = line.strip().split("\t")
            book2chapter2page.setdefault(book, {})[chapter] = int(page)
    for book_filename in tqdm(
        os.listdir(TRANSCRIPTIONS_PATH), desc="splitting texts in chapters"
    ):
        book_title = book_filename.replace(".txt", "").strip()
        text_path = os.path.join(TRANSCRIPTIONS_PATH, book_filename)
        with open(text_path) as f:
            raw_text = f.read()
            subchapter_texts = re.split(SUBCHAPTER_PATTERN, raw_text)
            for i, subchapter in enumerate(SUBCHAPTER_PATTERN.finditer(raw_text)):
                start_index, end_index = subchapter.start(), subchapter.end()
                subchapter_text = subchapter_texts[i + 1].strip()
                title = (
                    raw_text[start_index:end_index]
                    + subchapter_text.split("\n")[0].strip()
                ).lstrip()
                if subchapter_text == "":
                    continue
                subchapter_text = '\n'.join(subchapter_text.split("\n")[1:])
                subchapter_number = re.findall("^\d+\.\d{1,2}", title)[0]
                chapter_title = title.replace(subchapter_number, '').lstrip()
                chapter_title = re.sub('^\|\s+', '', chapter_title).lstrip()
                if subchapter_number in book2chapter2page[book_title]:
                    chapter_dump = {
                        "book_title": book_title,
                        "title": f"{book_title}\n{title}",
                        "chapter_title": chapter_title,
                        "text": subchapter_text,
                        "section_number": subchapter_number,
                        "page_number": book2chapter2page[book_title][subchapter_number],
                    }
                    dumps.append(chapter_dump)
    os.makedirs(os.path.dirname(SPLITTER_OUTPUT_PATH), exist_ok=True)
    with open(SPLITTER_OUTPUT_PATH, "w") as w:
        for dump in dumps:
            w.write(json.dumps(dump) + "\n")

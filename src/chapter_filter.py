import json
import os.path
import re
import spacy
from tqdm import tqdm

from src.constants import (
    CHAPTER_FILTER_OUTPUT_PATH,
    SPLITTER_OUTPUT_PATH,
)
from src.page_skipper import parse_annotations
from src.patterns import SENTENCE_PATTERNS, IN_SENTENCE_PATTERNS


def filter_chapters():
    tokenizer = spacy.load("en_core_web_sm")
    if os.path.exists(CHAPTER_FILTER_OUTPUT_PATH):
        return
    os.makedirs(os.path.dirname(CHAPTER_FILTER_OUTPUT_PATH), exist_ok=True)
    with open(SPLITTER_OUTPUT_PATH) as f:
        chapters = [json.loads(l.strip()) for l in f.readlines()]
    _, title2section_num, title2pattern = parse_annotations()
    chapters = [
        c
        for c in chapters
        if c["section_number"] not in title2section_num.get(c["book_title"], [])
    ]
    chapters = [
        c
        for c in chapters
        if c["chapter_title"].lower()
        not in [pat.lower() for pat in title2pattern.get(c["book_title"], [])]
    ]
    filtered_chapters = []
    for c in tqdm(chapters, desc="filtering chapters"):
        c_text = c["text"]
        c_sentences = list([s.text for s in tokenizer(c_text).sents])
        # if any(['openstax' in s.text for s in c_sentences]):
        #     found_sentence = [s for s in c_sentences if 'openstax' in s.text]
        #     print()
        # c_sentences = c_text.split(".")
        filtered_sentences = [
            s
            for s in c_sentences
            if not any(re.search(p, s) for p in SENTENCE_PATTERNS)
        ]
        if filtered_sentences:
            c["text"] = ".".join(filtered_sentences)
            for pat in IN_SENTENCE_PATTERNS:
                c["text"] = re.sub(pat, "", c["text"])
            c["text"] = re.sub(r"\n_+\n", "\n", c["text"])
            if len(c["text"].strip()) > 15:
                filtered_chapters.append(c)
    with open(CHAPTER_FILTER_OUTPUT_PATH, "w") as w:
        for c in filtered_chapters:
            w.write(json.dumps(c) + "\n")

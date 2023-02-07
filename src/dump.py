import json
import os.path

from tqdm import tqdm

from src.constants import OUTPUT_PATH, TITLE_URL_PATH, CHAPTER_FILTER_OUTPUT_PATH


def dump():
    if os.path.exists(OUTPUT_PATH):
        return
    title2url = {}
    with open(TITLE_URL_PATH) as f:
        for line in f.readlines():
            title, url = line.strip().split("\t")
            title2url[title] = url
    with open(CHAPTER_FILTER_OUTPUT_PATH) as f:
        chapters = [json.loads(l.strip()) for l in f.readlines()]
    for c in chapters:
        c["url"] = f'{title2url[c["book_title"]]}#page={c["page_number"]}'
    with open(OUTPUT_PATH, "w") as w:
        for c in tqdm(chapters, desc="dumping chapters"):
            w.write(json.dumps(c) + "\n")

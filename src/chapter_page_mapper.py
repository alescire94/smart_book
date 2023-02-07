import os
import re

from PyPDF2 import PdfReader
from tqdm import tqdm

from src.constants import CHAPTER_PAGE_MAPPING, RAW_BOOKS_PATH
from src.page_skipper import parse_annotations
from src.patterns import SUBCHAPTER_PATTERN


def map():
    if os.path.exists(CHAPTER_PAGE_MAPPING):
        return
    os.makedirs(os.path.dirname(CHAPTER_PAGE_MAPPING), exist_ok=True)
    title2range, _, _ = parse_annotations()
    with open(CHAPTER_PAGE_MAPPING, "w") as w:
        for filename in tqdm(
            os.listdir(RAW_BOOKS_PATH), desc="mapping chapters to pages"
        ):
            book_title = filename.replace(".pdf", "")
            pdf_file = PdfReader(os.path.join(RAW_BOOKS_PATH, filename))
            for i, p in enumerate(pdf_file.pages):
                if i + 1 not in title2range.get(book_title, []):
                    page_text = p.extract_text()
                    page_subchapter_texts = re.split(SUBCHAPTER_PATTERN, page_text)
                    # found subchapter
                    if len(page_subchapter_texts) > 1:
                        for y, subchapter in enumerate(
                            SUBCHAPTER_PATTERN.finditer(page_text)
                        ):
                            start_index, end_index = subchapter.start(), subchapter.end()
                            subchapter_text = page_subchapter_texts[y + 1].strip()
                            title = (
                                page_text[start_index:end_index]
                                + subchapter_text.split("\n")[0].strip()
                            ).lstrip()
                            subchapter_number = re.findall("\d+\.\d{1,2}", title)[0]
                            w.write(
                                book_title
                                + "\t"
                                + subchapter_number
                                + "\t"
                                + str(i + 1)
                                + "\n"
                            )

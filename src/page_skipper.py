import os
import re

from tqdm import tqdm

from src.constants import SKIP_PAGES_PATH, RAW_BOOKS_PATH, PROCESSED_BOOKS_PATH
import PyPDF2


def skip():
    title2range, _, _ = parse_annotations()
    for pdf_file_name in tqdm(os.listdir(RAW_BOOKS_PATH), desc="skipping pages"):
        title = pdf_file_name.replace(".pdf", "")
        pdf_file_path = os.path.join(RAW_BOOKS_PATH, pdf_file_name)
        pdf_file = PyPDF2.PdfReader(open(pdf_file_path, "rb"))
        output_pdf_path = os.path.join(PROCESSED_BOOKS_PATH, pdf_file_name)
        os.makedirs(PROCESSED_BOOKS_PATH, exist_ok=True)
        if os.path.exists(output_pdf_path):
            continue
        output_pdf = PyPDF2.PdfWriter(output_pdf_path)
        for page_num in range(len(pdf_file.pages)):
            pdf_page_num = page_num + 1
            page_blacklist = title2range.get(title, [])
            if pdf_page_num not in page_blacklist:  # pages to remove
                output_pdf.add_page(pdf_file.pages[page_num])
        with open(output_pdf_path, "wb") as f:
            output_pdf.write(f)


def parse_annotations():
    title2range = {}
    title2section_num = {}
    title2pattern = {}
    with open(SKIP_PAGES_PATH) as f:
        for line in f.readlines():
            chunks = line.strip().split("\t")
            title = chunks[0]
            for chunk in chunks[1:]:
                chunk = chunk.strip()
                if ";" in chunk:
                    start, end = [int(c) for c in chunk.split(";")]
                    title2range.setdefault(title, []).extend(list(range(start, end)))
                elif re.search("\d+\..*", chunk):
                    title2section_num.setdefault(title, []).append(chunk)
                else:
                    title2pattern.setdefault(title, []).append(chunk)
    return title2range, title2section_num, title2pattern

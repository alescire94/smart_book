import os
import re

from tqdm import tqdm

from src.constants import PROCESSED_BOOKS_PATH, TRANSCRIPTIONS_PATH

def transcribe():
    os.makedirs(TRANSCRIPTIONS_PATH, exist_ok=True)
    for pdf_filename in tqdm(os.listdir(PROCESSED_BOOKS_PATH), 'transcribing'):
        pdf_filepath = os.path.join(PROCESSED_BOOKS_PATH, pdf_filename)
        output_path = os.path.join(
            TRANSCRIPTIONS_PATH, pdf_filename.replace(".pdf", ".txt")
        )
        if os.path.exists(output_path):
            continue
        command_input_path = os.path.abspath(re.escape(pdf_filepath))
        command_output_path = os.path.abspath(re.escape(output_path))
        os.system(f"pdftotext -enc ASCII7 {command_input_path} {command_output_path}")
        with open(output_path) as f:
            text = f.read()
            text = re.sub(r"", "", text)
        with open(output_path, "w") as w:
            w.write(text)


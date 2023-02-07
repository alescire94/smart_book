import os
import re

from tqdm import tqdm

from src.constants import TITLE_URL_PATH, RAW_BOOKS_PATH


def download():
    with open(TITLE_URL_PATH) as f:
        for line in tqdm(f.readlines(), 'downloading'):
            title, url = line.strip().split('\t')
            out_path = os.path.join(RAW_BOOKS_PATH, f'{title}.pdf')
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            if os.path.exists(out_path):
                continue
            out_path = re.escape(out_path)
            os.system(f'wget {url} -O {out_path}')

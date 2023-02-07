from src import (
    downloader,
    page_skipper,
    chapter_page_mapper,
    transcriber,
    chapter_splitter,
    chapter_filter,
)
from src import dump

if __name__ == "__main__":
    # downloader.download()
    page_skipper.skip()
    chapter_page_mapper.map()
    transcriber.transcribe()
    chapter_splitter.split()
    chapter_filter.filter_chapters()
    dump.dump()

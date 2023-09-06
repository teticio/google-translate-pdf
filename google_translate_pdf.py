import argparse
import io
import logging
import time
from typing import List

from PyPDF2 import PdfReader, PdfWriter

from utils import translate_pdf, translate_pdf_proxy

handler = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class GoogleTranslatePDF:
    """
    Class to handle splitting, translating, and joining PDFs.
    """

    def __init__(self, pdf: bytearray, split_size: float = 10) -> None:
        """
        Initialize the GoogleTranslatePDF object.

        Args:
            pdf (bytearray): The PDF file to be translated.
            split_size (int, optional): The maximum size of each split PDF (in MB). Defaults to 10.
        """
        self.pdfs = self.split_pdf(pdf=pdf, max_size=int(split_size * 1024 * 1024))

    @staticmethod
    def split_pdf(pdf: bytearray, max_size: int) -> List[bytearray]:
        """
        Split a PDF into multiple smaller PDFs.

        Args:
            pdf (bytearray): The PDF file to be split.
            max_size (int): The maximum size of each split PDF.

        Returns:
            List[bytearray]: A list of split PDFs.
        """

        def split_pdf_by_pages(
            pdf_reader: PdfReader, max_pages: int
        ) -> List[bytearray]:
            """
            Split a PDF into multiple smaller PDFs by pages.

            Args:
                pdf_reader (PdfReader): The PDF reader object.
                max_pages (int): The maximum number of pages in each split PDF.

            Returns:
                List[bytearray]: A list of split PDFs.
            """
            pdfs = []

            for start_page in range(0, len(pdf_reader.pages), max_pages):
                pdf_writer = PdfWriter()

                for offset in range(max_pages):
                    page = start_page + offset
                    if page >= len(pdf_reader.pages):
                        break
                    pdf_writer.add_page(pdf_reader.pages[page])

                pdf_stream = io.BytesIO()
                pdf_writer.write(pdf_stream)
                pdfs.append(pdf_stream.getvalue())

            return pdfs

        pdfs = [pdf]
        while True:
            if max([len(x) for x in pdfs]) < max_size:
                return pdfs

            new_pdfs = []
            for pdf in pdfs:
                size = len(pdf)
                if size >= max_size:
                    pdf_reader = PdfReader(io.BytesIO(pdf))
                    max_pages = len(pdf_reader.pages) // (int(size / max_size) + 1)
                    assert max_pages > 0
                    new_pdfs.extend(
                        split_pdf_by_pages(pdf_reader=pdf_reader, max_pages=max_pages)
                    )
                else:
                    new_pdfs.append(pdf)
            assert len(new_pdfs) > len(pdfs)
            pdfs = new_pdfs

    @staticmethod
    def join_pdfs(pdfs: List[bytearray]) -> bytearray:
        """
        Join multiple PDFs into a single PDF.

        Args:
            pdfs (List[bytearray]): A list of PDFs to be joined.

        Returns:
            bytearray: The joined PDF.
        """
        pdf_writer = PdfWriter()

        for pdf in pdfs:
            if len(pdf) == 0:
                logger.error("Empty PDF")
                continue
            pdf_reader = PdfReader(io.BytesIO(pdf))
            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

        pdf_stream = io.BytesIO()
        pdf_writer.write(pdf_stream)

        return pdf_stream.getvalue()

    def translate(self, proxy: bool = False, sleep: int = 0) -> bytearray:
        """
        Translate a PDF file.

        Args:
            proxy (bool, optional): Whether to use a proxy for translation. Defaults to False.
            sleep (int, optional): Seconds to sleep between requests. Defaults to 0.

        Returns:
            bytearray: The translated PDF.
        """
        pdfs = []
        _translate_pdf = translate_pdf_proxy if proxy else translate_pdf
        for idx, pdf in enumerate(self.pdfs):
            pdfs.append(_translate_pdf(pdf=pdf))
            if idx < len(self.pdfs) - 1:
                time.sleep(sleep)
        return self.join_pdfs(pdfs=pdfs)


if __name__ == "__main__":
    """
    Main function to handle command line arguments and execute the translation.
    """
    parser = argparse.ArgumentParser(
        description="Split PDF file into multiple PDF files."
    )
    parser.add_argument("--input_pdf", type=str, help="input PDF file")
    parser.add_argument("--output_pdf", type=str, help="output PDF file")
    parser.add_argument("--proxy", action="store_true", help="use proxy")
    parser.add_argument(
        "--sleep", type=int, help="seconds to sleep between requests", default=0
    )
    parser.add_argument(
        "--split_size",
        type=float,
        help="split PDF into multiple PDFs of this size (in MB)",
        default=10,
    )
    args = parser.parse_args()

    with open(args.input_pdf, "rb") as file:
        pdf = file.read()
    pdf = GoogleTranslatePDF(pdf=pdf, split_size=args.split_size).translate(
        proxy=args.proxy, sleep=args.sleep
    )
    with open(args.output_pdf, "wb") as file:
        file.write(pdf)

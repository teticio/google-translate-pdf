import argparse
import io
from typing import List

from PyPDF2 import PdfReader, PdfWriter

from utils import translate_pdf, translate_pdf_proxy


class GoogleTranslatePDF:
    def __init__(self, pdf: bytearray) -> None:
        self.pdfs = self.split_pdf(pdf=pdf, max_size=10 * 1024 * 1024)

    @staticmethod
    def split_pdf(pdf: bytearray, max_size: int) -> List[bytearray]:
        def split_pdf_by_pages(
            pdf_reader: PdfReader, max_pages: int
        ) -> List[bytearray]:
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
        pdf_writer = PdfWriter()

        for pdf in pdfs:
            pdf_reader = PdfReader(io.BytesIO(pdf))
            for page in range(len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page])

        pdf_stream = io.BytesIO()
        pdf_writer.write(pdf_stream)

        return pdf_stream.getvalue()

    def translate(self, proxy: bool = False) -> bytearray:
        if proxy:
            pdfs = [translate_pdf_proxy(pdf=pdf) for pdf in self.pdfs]
        else:
            pdfs = [translate_pdf(pdf=pdf) for pdf in self.pdfs]
        return self.join_pdfs(pdfs=pdfs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split PDF file into multiple PDF files."
    )
    parser.add_argument("--input_pdf", type=str, help="input PDF file")
    parser.add_argument("--output_pdf", type=str, help="output PDF file")
    parser.add_argument("--proxy", action="store_true", help="use proxy")
    args = parser.parse_args()

    with open(args.input_pdf, "rb") as file:
        pdf = file.read()
    pdf = GoogleTranslatePDF(pdf=pdf).translate(proxy=args.proxy)
    with open(args.output_pdf, "wb") as file:
        file.write(pdf)

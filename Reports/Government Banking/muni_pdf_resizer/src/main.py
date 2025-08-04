"""
Main Entry Point
"""
import os
import fitz # PyMuPDF
from pathlib import Path

from src._version import __version__
from src.config import BASE_PATH, INPUT_DIR, OUTPUT_DIR

def add_margins_to_pdf(input_path, output_path, margin_pts=20):
    original = fitz.open(input_path)
    new_pdf = fitz.open()

    for page in original:
        rect = page.rect
        new_rect = fitz.Rect(
            0, 0,
            rect.width + 2 * margin_pts,
            rect.height + 2 * margin_pts
        )
        new_page = new_pdf.new_page(width=new_rect.width, height=new_rect.height)
        # Insert original page on top of margin
        new_page.show_pdf_page(
            fitz.Rect(margin_pts, margin_pts, margin_pts + rect.width, margin_pts + rect.height),
            original,
            page.number
        )
        
    new_pdf.save(output_path)
    new_pdf.close()
    original.close()

def add_margins_to_all_pdfs(directory, margin_pts=20):
    input_dir = Path(directory)
    OUTPUT_DIR.mkdir(exist_ok=True)

    for pdf_file in input_dir.glob("*.pdf"):
        output_path = OUTPUT_DIR / pdf_file.name
        print(f"Adding margins to {pdf_file.name}...")
        add_margins_to_pdf(pdf_file, output_path, margin_pts)
        print(f"Saved to {output_path}")


if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    add_margins_to_all_pdfs(INPUT_DIR, 20)
    print("Complete!")


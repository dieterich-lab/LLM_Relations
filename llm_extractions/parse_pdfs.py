"""
Parse PDF files as markdown.

This script iterates over all PDF files in a directory, converts them to markdown,
and saves the markdown files to an output directory.
"""

import logging
from pathlib import Path
from typing import List, Literal, Optional

import click
import pymupdf4llm
from docling.document_converter import DocumentConverter
from tabulate import tabulate
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("pdf_to_markdown")

DEFAULT_PPI_DIR = "/beegfs/prj/LINDA_LLM/CardioPrior/PPI_Papers/"
DEFAULT_TF_GENES_DIR = "/beegfs/prj/LINDA_LLM/CardioPrior/GRN_Papers/"

DEFAULT_PARSED_PPI_DIR = "/prj/LINDA_LLM/outputs/parsed_papers/CardioPrior/ppi"
DEFAULT_PARSED_TF_GENES_DIR = "/prj/LINDA_LLM/outputs/parsed_papers/CardioPrior/tf"


def ensure_directory_exists(path: str) -> None:
    """Ensure the directory exists, create if it doesn't."""
    directory = Path(path)
    if not directory.exists():
        logger.info(f"Creating directory: {directory}")
        directory.mkdir(parents=True, exist_ok=True)


def get_pdf_files(directory: str) -> List[Path]:
    """Get all PDF files in a directory."""
    pdf_files = list(Path(directory).glob("**/*.pdf"))
    return pdf_files


def format_table_for_markdown(table: List[List[str]]) -> str:
    """
    Format a table for markdown using the tabulate library.

    Args:
        table: A list of lists representing rows and columns

    Returns:
        Markdown formatted table
    """
    if not table or not table[0]:
        return ""

    # Clean up table data
    cleaned_table = []
    for row in table:
        cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
        cleaned_table.append(cleaned_row)

    # Use first row as header
    headers = cleaned_table[0]

    # Generate markdown table
    return tabulate(cleaned_table[1:], headers=headers, tablefmt="pipe")


def convert_with_pymupdf4llm(pdf_path: str) -> str:
    """
    Convert PDF to markdown using PyMuPDF4LLM library.

    This library is optimized for LLM use cases and preserves more formatting,
    especially tables and structure.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Markdown formatted string
    """
    try:
        # Use PyMuPDF4LLM's to_markdown function
        markdown = pymupdf4llm.to_markdown(pdf_path)
        return markdown
    except Exception as e:
        logger.error(f"Error converting with PyMuPDF4LLM: {e}")
        # Return empty string on failure so we can handle errors gracefully
        return ""


def convert_pdf_to_markdown(
    pdf_path: Path,
    output_dir: Path,
    converter: Literal["docling", "pymupdf4llm"] = "docling",
) -> Optional[Path]:
    """
    Convert a PDF file to markdown with enhanced table support.

    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save the markdown file
        converter: Conversion method to use:
                  - "docling": Uses docling for better overall conversion
                  - "pymupdf4llm": Uses PyMuPDF4LLM for LLM-optimized output

    Returns:
        Path to the generated markdown file or None if conversion failed
    """
    output_file = output_dir / f"{pdf_path.name.rsplit('.', 1)[0]}.md"

    try:
        if converter == "docling":
            # Use docling for conversion
            docling_converter = DocumentConverter()
            result = docling_converter.convert(str(pdf_path))
            doc = result.document
            markdown_content = doc.export_to_markdown()
        elif converter == "pymupdf4llm":
            # Use PyMuPDF4LLM for conversion
            markdown_content = convert_with_pymupdf4llm(str(pdf_path))
        # Check if we have any content
        if not markdown_content.strip():
            logger.error(f"No markdown content was generated for {pdf_path}")
            return None

        if output_file.exists():
            logger.warning(f"Overwriting existing file: {output_file}")

        # Write markdown to file (using "w" mode explicitly overwrites any existing content)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return output_file
    except Exception as e:
        logger.error(f"Error converting {pdf_path}: {e}")
        return None


@click.command()
@click.option(
    "--input-dir",
    default=DEFAULT_PPI_DIR,
    help="Directory containing PDF files",
)
@click.option(
    "--output-dir",
    default=DEFAULT_PARSED_PPI_DIR,
    help="Directory to save markdown files",
)
@click.option(
    "--converter",
    type=click.Choice(["docling", "pymupdf4llm"]),
    default="docling",
    help="Conversion method: docling (default) or pymupdf4llm (LLM-optimized)",
)
@click.option(
    "--single-file",
    help="Process only a single file instead of a directory",
)
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
def main(
    input_dir: str,
    output_dir: str,
    converter: str,
    single_file: Optional[str],
    verbose: bool,
) -> None:
    """
    Parse PDF files as markdown with enhanced table support.

    This script converts PDFs to markdown, with special handling for tables
    and document structure. It can process a single file or an entire directory.

    Multiple conversion methods are supported:
    - docling: Better overall conversion but slower
    - pymupdf4llm: LLM-optimized output with good table structure preservation
    """
    if verbose:
        logger.setLevel(logging.DEBUG)

    # Ensure output directory exists
    ensure_directory_exists(output_dir)
    output_dir_path = Path(output_dir)

    if single_file:
        pdf_path = Path(single_file)
        if not pdf_path.exists():
            logger.error(f"File not found: {pdf_path}")
            return

        logger.info(f"Processing single file: {pdf_path}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Using converter: {converter}")

        output_file = convert_pdf_to_markdown(pdf_path, output_dir_path, converter)
        if output_file:
            logger.info(f"Successfully converted {pdf_path} to {output_file}")
        else:
            logger.error(f"Failed to convert {pdf_path}")
    else:
        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Using converter: {converter}")

        # Get all PDF files
        pdf_files = get_pdf_files(input_dir)
        if not pdf_files:
            logger.warning(f"No PDF files found in {input_dir}")
            return

        # Make sure we don't process the same file multiple times
        pdf_files = list(set(pdf_files))

        logger.info(f"Found {len(pdf_files)} unique PDF files")

        # Convert PDFs to markdown
        success_count = 0

        for pdf_file in tqdm(pdf_files, desc="Converting PDFs"):
            output_file = convert_pdf_to_markdown(pdf_file, output_dir_path, converter)
            if output_file:
                success_count += 1
                logger.debug(f"Converted {pdf_file} to {output_file}")

        logger.info(
            f"Conversion complete: {success_count}/{len(pdf_files)} files converted"
        )


if __name__ == "__main__":
    main()

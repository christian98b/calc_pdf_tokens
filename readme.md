# PDF Cost Calculator

## Description

This Python script, `pdf_cost_calculator.py`, calculates the estimated cost of processing a PDF file based on the number of input tokens in the PDF and an estimated number of output tokens.  It allows you to specify different prices per million tokens for both input and output, offering a flexible way to estimate costs for language model applications that process PDFs.

## Features

*   **Separate Input and Output Token Pricing:**  Specify different prices per million tokens for input (reading the PDF content) and output (e.g., generating a summary or answering questions based on the PDF).
*   **Token Counting:** Uses the `tiktoken` library with the `p50k_base` encoding (suitable for models like GPT-4, GPT-3.5-turbo, and text-embedding-ada-002) to accurately count the number of input tokens in the PDF.
*   **PDF Text Extraction:** Employs the `PyPDF2` library to extract text from the PDF file.
*   **Error Handling:** Robust error handling for PDF file processing, including handling file not found errors and other exceptions.  Error messages are printed to `stderr`.
*   **Command-Line Interface:**  Provides a command-line interface using `argparse` for easy configuration.
*   **Optional PDF Path:** If no PDF path is provided as an argument, the script attempts to find and use the first PDF file in the current directory.
*   **Helpful Usage Information:**  Includes a comprehensive help message (accessible via `-h` or `--help`) with argument descriptions and example usage.

## Requirements

*   Python 3.6 or higher
*   `PyPDF2` library
*   `tiktoken` library

To install the necessary libraries, run:

```bash
pip install PyPDF2 tiktoken
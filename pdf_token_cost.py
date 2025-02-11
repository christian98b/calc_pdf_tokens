#!/usr/bin/env python3
"""
Calculate the cost of processing a PDF file, considering separate prices for input
and output tokens.

This script extracts text from a PDF, counts the number of input tokens, and
calculates the total cost based on a user-provided estimate of output tokens
and separate prices per million tokens for input and output.
"""

import PyPDF2
import tiktoken
import argparse
import sys  # For handling standard input
import os  # For finding files in the directory

def num_tokens_from_string(string: str) -> int:
    """
    Returns the number of tokens in a text string using the 'p50k_base' encoding.

    Args:
        string (str): The text string to tokenize.

    Returns:
        int: The number of tokens in the string.
    """
    encoding = tiktoken.get_encoding("p50k_base")  # Suitable for gpt-4, gpt-3.5-turbo, text-embedding-ada-002
    num_tokens = len(encoding.encode(string))
    return num_tokens


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF.  Returns an empty string if the file
             cannot be opened or read.
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}", file=sys.stderr)
        return ""  # Return empty string to avoid errors later
    except Exception as e:  # Catch any other exceptions during PDF processing
        print(f"Error processing PDF: {e}", file=sys.stderr)
        return ""

def calculate_costs(pdf_path: str, price_per_million_input: float, price_per_million_output: float, estimated_output_tokens: int):
    """
    Calculates and prints the cost of processing a PDF, considering separate input
    and output token prices.

    Args:
        pdf_path (str): Path to the PDF file.
        price_per_million_input (float): Price per million input tokens.
        price_per_million_output (float): Price per million output tokens.
        estimated_output_tokens (int): Estimated number of output tokens.
    """

    text_from_pdf = extract_text_from_pdf(pdf_path)
    if not text_from_pdf:
        return  # Exit if PDF processing failed

    input_tokens_count = num_tokens_from_string(text_from_pdf)

    input_cost = (input_tokens_count / 1000000) * price_per_million_input
    output_cost = (estimated_output_tokens / 1000000) * price_per_million_output
    total_cost = input_cost + output_cost

    print(f"Number of input tokens: {input_tokens_count}")
    print(f"Estimated number of output tokens: {estimated_output_tokens}")
    print(f"Total number of tokens: {input_tokens_count + estimated_output_tokens}")
    print(f"Price per million input tokens: ${price_per_million_input:.2f}")
    print(f"Price per million output tokens: ${price_per_million_output:.2f}")
    print(f"Total input cost: ${input_cost:.2f}")
    print(f"Total output cost: ${output_cost:.2f}")
    print(f"Total cost (input + output): ${total_cost:.2f}")


def find_first_pdf(directory: str = ".") -> str:
    """
    Finds the first PDF file in the specified directory.

    Args:
        directory (str): The directory to search in. Defaults to the current directory.

    Returns:
        str: The path to the first PDF file found, or an empty string if no PDF file is found.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            return os.path.join(directory, filename)
    return ""


def main():
    """
    Main function to parse arguments and run the cost calculation.
    """

    parser = argparse.ArgumentParser(
        description="Calculate the cost of processing a PDF with separate input and output token prices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,  # Show defaults in help message
        epilog="Example: pdf_cost_calculator.py [PDF_PATH] -i 1.50 -o 2.00 [-n 5000]"  # Example usage in help
    )

    # Positional argument for PDF path (optional)
    parser.add_argument(
        "pdf_path",
        metavar="PDF_PATH",
        nargs="?",  # Make the argument optional
        help="Path to the PDF file (if not provided, the first PDF in the current directory will be used).",
        type=str,  # Explicitly specify the type
    )

    # Named arguments
    parser.add_argument(
        "-i",
        "--input-price",
        dest="price_per_million_input",
        type=float,
        required=True,
        help="Price per million input tokens in dollars (e.g., 1.40)",
    )
    parser.add_argument(
        "-o",
        "--output-price",
        dest="price_per_million_output",
        type=float,
        default=0,
        help="Price per million output tokens in dollars (e.g., 2.00)",
    )
    parser.add_argument(
        "-n",
        "--num-output-tokens",
        dest="estimated_output_tokens",
        type=int,
        default=0,  # Set the default value to 0
        help="Estimated number of output tokens (default: 0).",
    )
    # Add a version argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0.0",  # Display script name and version
        help="Show program's version number and exit"  # Help message
    )


    args = parser.parse_args()

    # Determine PDF path
    pdf_path = args.pdf_path
    if not pdf_path:
        pdf_path = find_first_pdf()
        if not pdf_path:
            print("Error: No PDF path provided and no PDF files found in the current directory.", file=sys.stderr)
            sys.exit(1)  # Exit with an error code
        else:
            print(f"Using PDF file: {pdf_path}")  # Inform the user which PDF is being used


    # Call the calculation function
    calculate_costs(
        pdf_path,
        args.price_per_million_input,
        args.price_per_million_output,
        args.estimated_output_tokens,
    )

if __name__ == "__main__":
    main()
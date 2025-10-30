#!/usr/bin/env python3
"""
Remove leading and trailing double quotes from input string.
"""
import sys

def remove_quotes(text):
    """Remove one leading and one trailing double quote if both exist."""
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        return text[1:-1]
    return text

if __name__ == "__main__":
    # Read from stdin
    input_text = sys.stdin.read()
    # Remove trailing newline if present
    if input_text.endswith('\n'):
        input_text = input_text[:-1]
    # Process and output
    output_text = remove_quotes(input_text)
    print(output_text, end='', flush=True)

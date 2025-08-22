#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill column 9 (DEPS) in CoNLL-U files using head:deprel.
Uses Yauti to extract and write sentences, preserving metadata and multiword tokens.
"""

import sys
import argparse
from pathlib import Path

# --- Add path to Yauti.py if needed ---
YAUTI_SRC_DIR = "/home/usuario/complin/nheengatu/src"
if YAUTI_SRC_DIR not in sys.path:
    sys.path.append(YAUTI_SRC_DIR)

from Yauti import extractConlluSents, writeSentsConllu

def fill_deps(sentences):
    """
    Fill the DEPS column (9th) with head:deprel for each simple token.
    Multiword tokens and metadata are preserved.
    """
    for sent in sentences:
        for tok in sent:
            if isinstance(tok.get("id"), int):
                head = tok.get("head")
                deprel = tok.get("deprel")
                if head is not None and deprel is not None:
                    tok["deps"] = f"{head}:{deprel}"

def main():
    parser = argparse.ArgumentParser(description="Fill DEPS column with head:deprel using Yauti")
    parser.add_argument("--input", "-i", type=str, default="test_with_xcomp.conllu", help="Input CoNLL-U file")
    parser.add_argument("--output", "-o", type=str, default="test_with_deps.conllu", help="Output CoNLL-U file")
    args = parser.parse_args()

    input_file = Path(args.input)
    output_file = Path(args.output)

    # Extract sentences
    sentences = extractConlluSents(str(input_file))

    # Fill DEPS
    fill_deps(sentences)

    # Write back, preserving format
    writeSentsConllu(sentences, str(output_file))
    print(f"DEPS column filled and written to {output_file}")

if __name__ == "__main__":
    main()

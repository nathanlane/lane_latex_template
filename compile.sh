#!/bin/bash
# Simple compilation script for Lane LaTeX Template
# This ensures proper TEXINPUTS setting for the new package structure

# Set TEXINPUTS to find the llt* packages
export TEXINPUTS=".:./paper:./paper/modules:$TEXINPUTS"

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found. Please install a LaTeX distribution."
    exit 1
fi

# Compile the document
echo "Compiling main.tex with TEXINPUTS set for llt packages..."
pdflatex -interaction=nonstopmode -halt-on-error main.tex

# Check if compilation was successful
if [ $? -eq 0 ]; then
    echo "Compilation successful! Output: main.pdf"
else
    echo "Compilation failed. Check the error messages above."
    exit 1
fi
#!/bin/bash

# Install ghostscript if not already installed
# es per macOS: brew install ghostscript

# Directory containing the EPS files
EPS_DIR="/eos/user/s/sgiappic/diagrams/llnunu"

# Change to the directory containing EPS files
cd "$EPS_DIR"

# Convert each EPS file to PDF
for file in *.eps; do
    ps2pdf "$file" "${file%.eps}.pdf"
    rm "$file"
done

echo "Conversione completa"
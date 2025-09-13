#!/bin/bash

# Batch processing script for ScanNet .sens files
# This script processes .sens files from eval_list.txt and exports all data types

# Configuration
DATASET_ROOT="../OpenDataLab___ScanNet_v2/"  # Change this to your dataset path
OUTPUT_DIR="../processed_scannet"  # Change this to your desired output directory
EVAL_LIST="eval_list.txt"  # Path to eval_list.txt file

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if eval_list.txt exists
if [ ! -f "$EVAL_LIST" ]; then
    echo "Error: $EVAL_LIST not found!"
    echo "Please make sure eval_list.txt exists in the current directory."
    exit 1
fi

# Run batch processing
echo "Starting batch processing..."
echo "Dataset root: $DATASET_ROOT"
echo "Output directory: $OUTPUT_DIR"
echo "Eval list: $EVAL_LIST"

python3 batch_process.py \
    --dataset_root "$DATASET_ROOT" \
    --output_dir "$OUTPUT_DIR" \
    --reader_script "reader.py" \
    --eval_list "$EVAL_LIST"

echo "Batch processing completed!"

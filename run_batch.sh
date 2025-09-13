#!/bin/bash

# Batch processing script for ScanNet .sens files
# This script processes all .sens files and exports all data types

# Configuration
DATASET_ROOT="/path/to/your/scannet/dataset"  # Change this to your dataset path
OUTPUT_DIR="./processed_data"  # Change this to your desired output directory

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run batch processing
echo "Starting batch processing..."
echo "Dataset root: $DATASET_ROOT"
echo "Output directory: $OUTPUT_DIR"

python3 batch_process.py \
    --dataset_root "$DATASET_ROOT" \
    --output_dir "$OUTPUT_DIR" \
    --reader_script "reader.py"

echo "Batch processing completed!"

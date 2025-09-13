# Batch Processing Guide

This guide explains how to use the batch processing script to extract all data from your ScanNet dataset.

## Quick Start

### Method 1: Using the shell script (Recommended)

1. Edit the `run_batch.sh` file and update the paths:
   ```bash
   DATASET_ROOT="/path/to/your/scannet/dataset"  # Your dataset path
   OUTPUT_DIR="./processed_data"  # Your output directory
   ```

2. Make the script executable and run it:
   ```bash
   chmod +x run_batch.sh
   ./run_batch.sh
   ```

### Method 2: Using Python script directly

```bash
python3 batch_process.py \
    --dataset_root "/path/to/your/scannet/dataset" \
    --output_dir "./processed_data" \
    --reader_script "reader.py"
```

## Advanced Usage

### Process only a subset of files (for testing)

```bash
python3 batch_process.py \
    --dataset_root "/path/to/your/scannet/dataset" \
    --output_dir "./processed_data" \
    --max_files 10  # Process only first 10 files
```

### Resume from a specific file

```bash
python3 batch_process.py \
    --dataset_root "/path/to/your/scannet/dataset" \
    --output_dir "./processed_data" \
    --start_from 50  # Skip first 50 files
```

### Process specific range

```bash
python3 batch_process.py \
    --dataset_root "/path/to/your/scannet/dataset" \
    --output_dir "./processed_data" \
    --start_from 10 \
    --max_files 20  # Process files 10-29
```

## Output Structure

The script will create the following structure in your output directory:

```
processed_data/
├── scene0000_00/
│   ├── depth/           # 16-bit PNG depth images
│   ├── color/           # 8-bit RGB JPEG images
│   ├── pose/            # Camera poses (4x4 matrices)
│   └── intrinsic/       # Camera intrinsics
├── scene0000_01/
│   ├── depth/
│   ├── color/
│   ├── pose/
│   └── intrinsic/
└── batch_process_YYYYMMDD_HHMMSS.log  # Processing log
```

## What Gets Exported

For each .sens file, the script exports:

- **Depth Images**: 16-bit PNG files (depth shift 1000)
- **Color Images**: 8-bit RGB JPEG files
- **Camera Poses**: 4x4 transformation matrices (camera to world)
- **Camera Intrinsics**: 4x4 intrinsic and extrinsic matrices

## Monitoring Progress

The script provides:
- Real-time progress updates
- Detailed logging to both console and log file
- Error reporting for failed files
- Final summary with success/failure counts

## Troubleshooting

### Common Issues

1. **Permission denied**: Make sure you have write permissions to the output directory
2. **File not found**: Verify the dataset path is correct
3. **Memory issues**: Process files in smaller batches using `--max_files`
4. **Timeout errors**: Some large files may take longer; the script has a 1-hour timeout per file

### Log Files

Check the log file for detailed error information:
```bash
tail -f processed_data/batch_process_YYYYMMDD_HHMMSS.log
```

## Performance Tips

1. **SSD Storage**: Use SSD storage for both input and output for better performance
2. **Batch Size**: For large datasets, process in smaller batches to avoid memory issues
3. **Parallel Processing**: The script processes files sequentially; for parallel processing, you can run multiple instances with different `--start_from` values

## Example Commands

```bash
# Process all files
python3 batch_process.py --dataset_root "/data/scannet" --output_dir "./output"

# Test with first 5 files
python3 batch_process.py --dataset_root "/data/scannet" --output_dir "./test_output" --max_files 5

# Resume from file 100
python3 batch_process.py --dataset_root "/data/scannet" --output_dir "./output" --start_from 100
```

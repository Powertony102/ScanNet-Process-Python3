# ScanNet Data Processing Tool (Python 3)

A Python 3 compatible tool for processing ScanNet sensor data files (.sens format). This tool allows you to extract depth images, color images, camera poses, and camera intrinsics from ScanNet .sens files.

## Features

- **Depth Image Export**: Extract and export depth images from .sens files
- **Color Image Export**: Extract and export RGB color images from .sens files  
- **Camera Pose Export**: Export camera poses (camera-to-world transformations) for each frame
- **Camera Intrinsics Export**: Export camera intrinsic and extrinsic parameters
- **Batch Processing**: Process multiple .sens files in batch with progress tracking
- **Eval List Support**: Process only scenes specified in an eval_list.txt file
- **Random Scene Sampling**: Generate random scene lists for evaluation
- **Python 3 Compatible**: Fully updated to work with Python 3.x

## Requirements

- Python 3.6+
- numpy
- imageio
- opencv-python (cv2)
- pypng

## Installation

Install the required dependencies:

```bash
pip install numpy imageio opencv-python pypng
```

## Usage

The main script is `reader.py`. Use it with the following command-line arguments:

```bash
python reader.py --filename <path_to_sens_file> --output_path <output_directory> [options]
```

### Command Line Arguments

- `--filename`: Path to the .sens file to process (required)
- `--output_path`: Path to the output directory (required)
- `--export_depth_images`: Export depth images (optional flag)
- `--export_color_images`: Export color images (optional flag)
- `--export_poses`: Export camera poses (optional flag)
- `--export_intrinsics`: Export camera intrinsics (optional flag)

### Examples

Export all data types:
```bash
python reader.py --filename scene0000_00.sens --output_path ./output --export_depth_images --export_color_images --export_poses --export_intrinsics
```

Export only depth images:
```bash
python reader.py --filename scene0000_00.sens --output_path ./output --export_depth_images
```

Export color images and poses:
```bash
python reader.py --filename scene0000_00.sens --output_path ./output --export_color_images --export_poses
```

## Batch Processing

For processing multiple .sens files, use the batch processing script:

### Process All Scenes
```bash
python batch_process.py --dataset_root /path/to/scannet --output_dir ./processed_data
```

### Process Scenes from Eval List
```bash
python batch_process.py --dataset_root /path/to/scannet --output_dir ./processed_data --eval_list eval_list.txt
```

### Batch Processing Arguments
- `--dataset_root`: Root directory of the ScanNet dataset (required)
- `--output_dir`: Output directory for processed data (required)
- `--reader_script`: Path to the reader.py script (default: reader.py)
- `--eval_list`: Path to eval_list.txt file (default: eval_list.txt)
- `--start_from`: Start processing from this file index (for resuming)
- `--max_files`: Maximum number of files to process (for testing)

### Using the Shell Script
You can also use the provided shell script for convenience:

```bash
# Edit run_batch.sh to set your dataset path
# Then run:
./run_batch.sh
```

## Random Scene Sampling

Generate a random list of scenes for evaluation:

```bash
python random_sample.py
```

This will:
1. Extract all scene names from structure.txt
2. Randomly sample 50 scenes
3. Save the list to eval_list.txt

## Complete Workflow Example

Here's a complete example of how to use the tools:

1. **Generate a random scene list for evaluation:**
   ```bash
   python random_sample.py
   ```

2. **Process the scenes from the eval list:**
   ```bash
   python batch_process.py --dataset_root /path/to/scannet --output_dir ./processed_data --eval_list eval_list.txt
   ```

3. **Or use the shell script:**
   ```bash
   # Edit run_batch.sh to set your dataset path
   ./run_batch.sh
   ```

The processed data will be saved in the output directory with the following structure:
```
processed_data/
├── scene0126_00/
│   ├── depth/
│   ├── color/
│   ├── pose/
│   └── intrinsic/
├── scene0030_01/
│   └── ...
└── ...
```

## Output Structure

When you run the tool, it will create the following directory structure in your output path:

```
output/
├── depth/           # Depth images (if --export_depth_images is used)
│   ├── 0.png
│   ├── 1.png
│   └── ...
├── color/           # Color images (if --export_color_images is used)
│   ├── 0.jpg
│   ├── 1.jpg
│   └── ...
├── pose/            # Camera poses (if --export_poses is used)
│   ├── 0.txt
│   ├── 1.txt
│   └── ...
└── intrinsic/       # Camera intrinsics (if --export_intrinsics is used)
    ├── intrinsic_color.txt
    ├── extrinsic_color.txt
    ├── intrinsic_depth.txt
    └── extrinsic_depth.txt
```

## File Formats

- **Depth Images**: 16-bit PNG files
- **Color Images**: JPEG files
- **Camera Poses**: Text files containing 4x4 transformation matrices
- **Camera Intrinsics**: Text files containing 4x4 intrinsic and extrinsic matrices

## Classes

### SensorData
Main class for loading and processing .sens files.

**Methods:**
- `export_depth_images(output_path, image_size=None, frame_skip=1)`: Export depth images
- `export_color_images(output_path, image_size=None, frame_skip=1)`: Export color images
- `export_poses(output_path, frame_skip=1)`: Export camera poses
- `export_intrinsics(output_path)`: Export camera intrinsics

### RGBDFrame
Represents a single RGB-D frame from the .sens file.

**Methods:**
- `decompress_depth(compression_type)`: Decompress depth data
- `decompress_color(compression_type)`: Decompress color data

## Notes

- This tool has been updated from Python 2 to Python 3 for better compatibility
- The .sens file format is specific to ScanNet dataset
- Depth images are saved as 16-bit PNG files to preserve precision
- All camera poses are in camera-to-world format

## Files

- `reader.py`: Main script for processing individual .sens files
- `batch_process.py`: Batch processing script for multiple .sens files
- `run_batch.sh`: Shell script wrapper for batch processing
- `random_sample.py`: Script to generate random scene lists for evaluation
- `SensorData.py`: Core classes for reading and processing .sens files
- `eval_list.txt`: List of scenes to process (generated by random_sample.py)
- `structure.txt`: Dataset structure file used for scene discovery

## License

This tool is based on the original ScanNet processing code and has been updated for Python 3 compatibility.

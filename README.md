# ScanNet Data Processing Tool (Python 3)

A Python 3 compatible tool for processing ScanNet sensor data files (.sens format). This tool allows you to extract depth images, color images, camera poses, and camera intrinsics from ScanNet .sens files.

## Features

- **Depth Image Export**: Extract and export depth images from .sens files
- **Color Image Export**: Extract and export RGB color images from .sens files  
- **Camera Pose Export**: Export camera poses (camera-to-world transformations) for each frame
- **Camera Intrinsics Export**: Export camera intrinsic and extrinsic parameters
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

## License

This tool is based on the original ScanNet processing code and has been updated for Python 3 compatibility.

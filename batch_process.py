#!/usr/bin/env python3
"""
Batch processing script for ScanNet .sens files
Processes all .sens files in the dataset and exports all available data types.
"""

import os
import sys
import glob
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime

def setup_logging(log_file):
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def find_sens_files(dataset_root):
    """Find all .sens files in the dataset"""
    sens_files = []
    
    # Look for .sens files in the scans directory
    scans_dir = os.path.join(dataset_root, 'raw', 'scans')
    if os.path.exists(scans_dir):
        pattern = os.path.join(scans_dir, '*', '*.sens')
        sens_files = glob.glob(pattern)
        logging.info(f"Found {len(sens_files)} .sens files in {scans_dir}")
    else:
        logging.warning(f"Scans directory not found: {scans_dir}")
    
    return sorted(sens_files)

def process_sens_file(sens_file, output_base_dir, reader_script):
    """Process a single .sens file"""
    # Extract scene name from file path
    scene_name = os.path.basename(sens_file).replace('.sens', '')
    scene_dir = os.path.dirname(sens_file)
    scene_id = os.path.basename(scene_dir)
    
    # Create output directory for this scene
    scene_output_dir = os.path.join(output_base_dir, scene_id)
    
    # Build command
    cmd = [
        'python3', reader_script,
        '--filename', sens_file,
        '--output_path', scene_output_dir,
        '--export_depth_images',
        '--export_color_images', 
        '--export_poses',
        '--export_intrinsics'
    ]
    
    logging.info(f"Processing {scene_name}...")
    logging.info(f"Command: {' '.join(cmd)}")
    
    try:
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
        
        if result.returncode == 0:
            logging.info(f"Successfully processed {scene_name}")
            return True
        else:
            logging.error(f"Failed to process {scene_name}")
            logging.error(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"Timeout processing {scene_name}")
        return False
    except Exception as e:
        logging.error(f"Exception processing {scene_name}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Batch process ScanNet .sens files')
    parser.add_argument('--dataset_root', required=True, 
                       help='Root directory of the ScanNet dataset')
    parser.add_argument('--output_dir', required=True,
                       help='Output directory for processed data')
    parser.add_argument('--reader_script', default='reader.py',
                       help='Path to the reader.py script (default: reader.py)')
    parser.add_argument('--start_from', type=int, default=0,
                       help='Start processing from this file index (for resuming)')
    parser.add_argument('--max_files', type=int, default=None,
                       help='Maximum number of files to process (for testing)')
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = os.path.join(args.output_dir, f'batch_process_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    os.makedirs(args.output_dir, exist_ok=True)
    setup_logging(log_file)
    
    logging.info("Starting batch processing of ScanNet .sens files")
    logging.info(f"Dataset root: {args.dataset_root}")
    logging.info(f"Output directory: {args.output_dir}")
    logging.info(f"Reader script: {args.reader_script}")
    
    # Find all .sens files
    sens_files = find_sens_files(args.dataset_root)
    
    if not sens_files:
        logging.error("No .sens files found!")
        return 1
    
    # Apply limits
    if args.max_files:
        sens_files = sens_files[:args.max_files]
    
    if args.start_from > 0:
        sens_files = sens_files[args.start_from:]
        logging.info(f"Starting from file index {args.start_from}")
    
    total_files = len(sens_files)
    logging.info(f"Processing {total_files} files")
    
    # Process files
    successful = 0
    failed = 0
    
    for i, sens_file in enumerate(sens_files):
        logging.info(f"Progress: {i+1}/{total_files} ({((i+1)/total_files)*100:.1f}%)")
        
        if process_sens_file(sens_file, args.output_dir, args.reader_script):
            successful += 1
        else:
            failed += 1
    
    # Summary
    logging.info("="*50)
    logging.info("BATCH PROCESSING COMPLETE")
    logging.info(f"Total files: {total_files}")
    logging.info(f"Successful: {successful}")
    logging.info(f"Failed: {failed}")
    logging.info(f"Success rate: {(successful/total_files)*100:.1f}%")
    logging.info(f"Log file: {log_file}")
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())

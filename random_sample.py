#!/usr/bin/env python3
"""
Randomly sample 50 scenes from ScanNet dataset and output to eval_list
"""

import re
import random
import os

def extract_scene_names_from_structure(structure_file):
    """
    Extract all scene names from the structure.txt file
    """
    scene_names = []
    
    with open(structure_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Match lines that contain scene directories
            # The line format is: │   │   ├── scene0000_00
            if '├── scene' in line:
                # Extract the scene name from the line
                match = re.search(r'scene(\d+_\d+)', line)
                if match:
                    scene_name = 'scene' + match.group(1)
                    scene_names.append(scene_name)
    
    return scene_names

def random_sample_scenes(scene_names, num_samples=50):
    """
    Randomly sample specified number of scenes
    """
    if len(scene_names) < num_samples:
        print(f"Warning: Only {len(scene_names)} scenes available, sampling all of them")
        return scene_names
    
    return random.sample(scene_names, num_samples)

def save_to_eval_list(sampled_scenes, output_file='eval_list.txt'):
    """
    Save sampled scene names to eval_list file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for scene in sampled_scenes:
            f.write(f"{scene}\n")
    
    print(f"Successfully saved {len(sampled_scenes)} scenes to {output_file}")

def main():
    # Set random seed for reproducibility
    random.seed(42)
    
    # Path to structure.txt file
    structure_file = 'structure.txt'
    
    if not os.path.exists(structure_file):
        print(f"Error: {structure_file} not found!")
        return
    
    print("Extracting scene names from structure.txt...")
    scene_names = extract_scene_names_from_structure(structure_file)
    print(f"Found {len(scene_names)} total scenes")
    
    print("Randomly sampling 50 scenes...")
    sampled_scenes = random_sample_scenes(scene_names, 50)
    
    print("Sampled scenes:")
    for i, scene in enumerate(sampled_scenes, 1):
        print(f"{i:2d}. {scene}")
    
    print("\nSaving to eval_list.txt...")
    save_to_eval_list(sampled_scenes)
    
    print("\nDone!")

if __name__ == "__main__":
    main()

#!/bin/bash

python3 - "$@" <<'PYTHON'
import os
import sys
import shutil

def print_usage_and_exit():
    print("Usage: collect_files.sh [--max_depth N] <input_dir> <output_dir>")
    sys.exit(1)

args = sys.argv[1:]
max_depth = None
if not args:
    print_usage_and_exit()

if args[0] == "--max_depth":
    if len(args) < 3:
        print_usage_and_exit()
    try:
        max_depth = int(args[1])
    except ValueError:
        print("Error: max_depth must be an integer")
        sys.exit(1)
    input_dir = args[2]
    output_dir = args[3] if len(args) > 3 else None
else:
    input_dir = args[0]
    output_dir = args[1] if len(args) > 1 else None

if not input_dir or not output_dir:
    print_usage_and_exit()

input_dir = os.path.abspath(input_dir)
output_dir = os.path.abspath(output_dir)

if not os.path.isdir(input_dir):
    print(f"Error: Input directory '{input_dir}' does not exist or is not a directory")
    sys.exit(1)

common_path = os.path.commonpath([input_dir, output_dir])
if common_path == input_dir:
    print("Error: Output directory is inside the input directory (this could cause infinite recursion)")
    sys.exit(1)

if os.path.exists(output_dir):
    if not os.path.isdir(output_dir):
        print(f"Error: Output path '{output_dir}' exists but is not a directory")
        sys.exit(1)
else:
    try:
        os.makedirs(output_dir)
    except Exception as e:
        print(f"Error: Failed to create output directory '{output_dir}': {e}")
        sys.exit(1)

used_names = set(os.listdir(output_dir))

for root, dirs, files in os.walk(input_dir, topdown=True):
    if max_depth is not None:
        rel_path = os.path.relpath(root, input_dir)
        depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))
        if depth >= max_depth:
            dirs[:] = []

    for filename in files:
        source_path = os.path.join(root, filename)
        dest_name = filename

        if dest_name in used_names:
            name, ext = os.path.splitext(filename)
            counter = 1
            while True:
                dest_name = f"{name}{counter}{ext}"
                if dest_name not in used_names and not os.path.exists(os.path.join(output_dir, dest_name)):
                    break
                counter += 1

        dest_path = os.path.join(output_dir, dest_name)
        try:
            shutil.copy(source_path, dest_path)
        except Exception as e:
            print(f"Error: Failed to copy '{source_path}' to '{dest_path}': {e}")
            continue

        used_names.add(dest_name)
PYTHON
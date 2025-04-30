#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def collect_files(input_dir: str, output_dir: str, max_depth: int = None) -> None:
    os.makedirs(output_dir, exist_ok=True)
    used_names = set()

    def recurse(current_path: str, current_level: int = 0):
        for entry in os.scandir(current_path):
            if entry.is_file():
                file_name = entry.name
                dest_name = file_name
                if dest_name in used_names:
                    base, ext = os.path.splitext(file_name)
                    counter = 1
                    dest_name = f"{base}{counter}{ext}"
                    while dest_name in used_names:
                        counter += 1
                        dest_name = f"{base}{counter}{ext}"
                used_names.add(dest_name)
                dest_path = os.path.join(output_dir, dest_name)
                shutil.copy2(entry.path, dest_path)
            elif entry.is_dir():
                if max_depth is None or current_level < max_depth - 1:
                    recurse(entry.path, current_level + 1)

    recurse(input_dir, 0)

def main():
    parser = argparse.ArgumentParser(description="Собирает все файлы из папки (с вложенными) в одну выходную папку.")
    parser.add_argument("input_dir", help="Путь к входной директории с файлами")
    parser.add_argument("output_dir", help="Путь к выходной директории, куда будут скопированы файлы")
    parser.add_argument("--max_depth", type=int, help="Максимальная глубина рекурсивного обхода директорий", default=None)
    args = parser.parse_args()

    collect_files(args.input_dir, args.output_dir, args.max_depth)

if __name__ == "__main__":
    main()
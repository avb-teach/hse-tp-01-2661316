#!/usr/bin/env python3
import os
import sys

def collect_files(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for name in os.listdir(src_dir):
        path = os.path.join(src_dir, name)
        if os.path.isfile(path):
            copy_file(path, dst_dir)
        elif os.path.isdir(path):
            collect_files(path, dst_dir)

def copy_file(src_path, dst_dir):
    fname = os.path.basename(src_path)
    dst_path = os.path.join(dst_dir, fname)
    with open(src_path, 'rb') as fin, open(dst_path, 'wb') as fout:
        fout.write(fin.read())

def main():
    if len(sys.argv) != 3:
        print("Использование:\n  python collect_files.py <входная_папка> <выходная_папка>")
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    if not os.path.isdir(src):
        print(f"Ошибка: «{src}» не является директорией.")
        sys.exit(1)
    collect_files(src, dst)

if __name__ == "__main__":
    main()
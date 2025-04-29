#!/usr/bin/env python3
import sys
import os
import shutil

def usage():
    print(f"Использование: {sys.argv[0]} [--max_depth N] <input_dir> <output_dir>")
    sys.exit(1)

def collect_files(input_dir, output_dir, max_depth=None):
    seen = {}
    def helper(current, depth):
        if max_depth is not None and depth > max_depth:
            return
        try:
            entries = os.listdir(current)
        except PermissionError:
            return
        for name in entries:
            path = os.path.join(current, name)
            if os.path.isdir(path):
                helper(path, depth + 1)
            else:
                base, ext = os.path.splitext(name)
                count = seen.get(name, 0)
                seen[name] = count + 1
                if count > 0:
                    name_copy = f"{base}_{count}{ext}"
                else:
                    name_copy = name
                shutil.copy2(path, os.path.join(output_dir, name_copy))

    os.makedirs(output_dir, exist_ok=True)
    helper(input_dir, depth=1)

if __name__ == "__main__":
    args = sys.argv[1:]
    max_depth = None
    if len(args) == 0:
        usage()
    if args[0] == "--max_depth":
        if len(args) < 3:
            usage()
        try:
            max_depth = int(args[1])
        except ValueError:
            print("Ошибка: N должно быть числом")
            sys.exit(1)
        args = args[2:]
    if len(args) != 2:
        usage()
    inp, outp = args
    collect_files(inp, outp, max_depth)
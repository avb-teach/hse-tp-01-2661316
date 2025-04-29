#!/usr/bin/env bash
# collect_files.sh

if [ $# -lt 2 ]; then
  echo "Использование: $0 [--max_depth N] <входная_директория> <выходная_директория>"
  exit 1
fi

collect_files.py "$@"
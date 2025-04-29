#!/bin/bash
if [ $# -ne 2 ]; then
  echo "Использование: $0 папка_входа папка_выхода"
  exit 1
fi
input_dir=$1
output_dir=$2
if [ ! -d "$output_dir" ]; then
  mkdir "$output_dir"
fi
for file in $(find "$input_dir" -type f); do
  cp "$file" "$output_dir/"
done
echo "Готово! Все файлы скопированы в $output_dir"
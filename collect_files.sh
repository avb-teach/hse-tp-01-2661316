#!/usr/bin/env bash

if [ $# -lt 2 ]; then
  printf "Usage: %s INPUT_DIR OUTPUT_DIR [--max_depth N]\n" "$0" >&2
  exit 1
fi

INPUT=$1
OUTPUT=$2
shift 2

DEPTH=-1
while [ $# -gt 0 ]; do
  case "$1" in
    --max_depth) DEPTH=$2; shift 2 ;;
    *)           shift ;;
  esac
done

python3 "$(dirname "$0")/script.py" "$INPUT" "$OUTPUT" "$DEPTH"
#!/usr/bin/env bash

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
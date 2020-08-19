#!/bin/bash

SET=$(seq 1 5)

python3 ./dynamodb_all_remove-aug.py

for idx in $SET; do
  python3 ./req/request.py
  sleep 10
  echo '==================================='$idx'==================================='
done
sh ./dynamodb_export_json.sh aug ./aug-only-one

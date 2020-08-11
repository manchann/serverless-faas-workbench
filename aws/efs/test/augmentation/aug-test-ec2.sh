#!/bin/bash

lambda_memory="512 2048"
count="10 50 100"
for lm in $lambda_memory; do
  python3 ./dynamodb_all_remove-aug.py

  aws lambda update-function-configuration --function-name efs-test-2 --memory-size $lm
  aws lambda update-function-configuration --function-name s3-aug-test --memory-size $lm
  sleep 60
  for cnt in $count; do
    python3 ./request$cnt.py
  done
  sleep 30
  sh ./dynamodb_export_json.sh aug ./aug-$lm
done

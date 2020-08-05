#!/bin/bash

lambda_memory="512 2048"

for lm in $lambda_memory; do
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove-aug.py

  aws lambda update-function-configuration --function-name efs-test-2 --memory-size $lm
  aws lambda update-function-configuration --function-name s3-aug-test --memory-size $lm
  sleep 60

  python3 ./request.py

  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh aug2 /Users/manchan/Desktop/BigDataLab/Papers/aug-$lm
done

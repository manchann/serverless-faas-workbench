#!/bin/bash

lambda_memory="512 2048"

lambda_functions="dd"

bs_set="50 256 1024 2048"

for lm in $lambda_memory; do
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove-local.py

  for lf in $lambda_functions; do
    aws lambda update-function-configuration --function-name efs-test --handler $lf.lambda_handler --memory-size $lm
    aws lambda update-function-configuration --function-name tmp-test --handler $lf.lambda_handler --memory-size $lm
    for bs in $bs_set; do
      sleep 10
      aws lambda update-function-configuration --function-name efs-test --memory-size 256
      aws lambda update-function-configuration --function-name tmp-test --memory-size 256
      sleep 30
      aws lambda update-function-configuration --function-name efs-test --memory-size $lm
      aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
      sleep 30

      python3 ./bs_set/bs_$bs.py
      sleep 10
    done
  done

  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/efs-bw-$lm
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh local /Users/manchan/Desktop/BigDataLab/Papers/loc-bw-$lm
done

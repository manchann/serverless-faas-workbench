#!/bin/bash

lambda_memory="512"

bs_set="50"

for lm in $lambda_memory; do
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove-local.py

  sleep 10

  for bs in $bs_set; do

    SET=$(seq 1 50)
    for i in $SET; do
      python3 ./bs_set/bs_$bs.py
      sleep 3
    done

  done
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/concurrency-efs-test
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh local /Users/manchan/Desktop/BigDataLab/Papers/concurrency-loc-test
done

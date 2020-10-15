#!/bin/bash

lambda_memory="512"

lambda_functions="random-read random-write sequence-read sequence-write dd"
bs_set="1MB" #1MB 1KB
efs_scale="1 10"

for lm in $lambda_memory; do
  #remove dynamodb datas
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
  sleep 10
  #change lambda_function sequence -> random
  for lf in $lambda_functions; do
    for bs in $bs_set; do
      for es in $efs_scale; do
        aws lambda update-function-configuration --function-name efs-test --handler $lf.lambda_handler --memory-size 256
        sleep 10
        aws lambda update-function-configuration --function-name efs-test --handler $lf.lambda_handler --memory-size $lm
        sleep 10
        python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/efs/test/efs_scalablity/$bs/request$es.py
        sleep 20
      done
    done
  done
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/efs-scalability-$lm-1
done

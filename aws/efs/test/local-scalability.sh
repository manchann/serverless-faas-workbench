#!/bin/bash

lambda_memory="512"

lambda_functions="random-write sequence-write"
bs_set="1MB" #1MB 1KB
efs_scale="1 10 20 50 100 200"

for lm in $lambda_memory; do
  #remove dynamodb datas
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove-local.py
  sleep 10

  for lf in $lambda_functions; do
    for bs in $bs_set; do
      for es in $efs_scale; do
        aws lambda update-function-configuration --function-name tmp-test --handler $lf.lambda_handler --memory-size 256
        sleep 40
        aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
        sleep 40
        python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/efs/test/local_scalablity/$bs/request$es.py
        sleep 60
      done
    done
    sleep 60
  done
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh local /Users/manchan/Desktop/BigDataLab/Papers/local-scalability-$lm-$bs
done

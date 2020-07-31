#!/bin/bash

lambda_memory="512 2048"

lambda_functions="random-read sequence-read dd"
bs_set="1MB"
for lm in $lambda_memory; do
  #remove dynamodb datas
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
  sleep 10
  #change lambda_function sequence -> random
  for lf in $lambda_functions; do
    efs_scale="1 10 20 50 100 200"
    for bs in $bs_set; do
      for es in $efs_scale; do
        aws lambda update-function-configuration --function-name efs-test --handler $lf.lambda_handler --memory-size 256
        sleep 40
        aws lambda update-function-configuration --function-name efs-test --memory-size $lm
        sleep 40
        python3 ./efs_scalablity/$bs/request$es.py
        sleep 60
      done
    done
    sleep 60
  done
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/efs-scalablity
done

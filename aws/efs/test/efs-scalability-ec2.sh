#!/bin/bash

lambda_memory="512"

lambda_functions="random-write sequence-write"
bs_set="1MB" #1MB 1KB
efs_scale="200"

for lm in $lambda_memory; do
  #remove dynamodb datas
  python3 ./dynamodb_all_remove.py
  sleep 10
  #change lambda_function sequence -> random
  for lf in $lambda_functions; do
    for bs in $bs_set; do
      for es in $efs_scale; do
        aws lambda update-function-configuration --function-name efs-test --handler $lf.lambda_handler --memory-size 256
        aws lambda update-function-configuration --function-name efs-test --memory-size $lm
        python3 ./request.py
        sleep 400
      done
    done
  done
  sh ./dynamodb_export_json.sh EFS ./
done
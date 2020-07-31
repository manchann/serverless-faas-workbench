#!/bin/bash

lambda_memory="512 2048"

for lm in $lambda_memory; do
  python3 ./dynamodb_all_remove.py

  #  aws lambda update-function-configuration --function-name efs-test --handler random-write.lambda_handler --memory-size $lm
  #  aws lambda update-function-configuration --function-name tmp-test --handler random-write.lambda_handler --memory-size $lm
  #
  #  sleep 70
  #
  #  for ((i = 0; i < 5; i++)); do
  #
  #    python3 ./request.py
  #    sleep 60
  #
  #  done
  #
  #  aws lambda update-function-configuration --function-name efs-test --handler sequence-write.lambda_handler
  #  aws lambda update-function-configuration --function-name tmp-test --handler sequence-write.lambda_handler
  #
  #  sleep 60
  #  for ((i = 0; i < 5; i++)); do
  #
  #    python3 ./request.py
  #    sleep 60
  #
  #  done

  aws lambda update-function-configuration --function-name efs-test --handler random-read.lambda_handler
  aws lambda update-function-configuration --function-name tmp-test --handler random-read.lambda_handler

  for ((i = 0; i < 5; i++)); do

    sleep 10
    aws lambda update-function-configuration --function-name efs-test --memory-size 256
    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
    sleep 5
    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
    sleep 40

    python3 ./request.py
    sleep 60

  done

  aws lambda update-function-configuration --function-name efs-test --handler sequence-read.lambda_handler
  aws lambda update-function-configuration --function-name tmp-test --handler sequence-read.lambda_handler

  for ((i = 0; i < 5; i++)); do

    sleep 10
    aws lambda update-function-configuration --function-name efs-test --memory-size 256
    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
    sleep 5
    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
    sleep 40

    python3 ./request.py
    sleep 60

  done

  sh ./dynamodb_export_json.sh EFS ./file_r_test2-$lm
done

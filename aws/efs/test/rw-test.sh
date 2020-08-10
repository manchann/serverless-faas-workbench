#!/bin/bash

lambda_memory="512 2048"

bs_set="1 50 256 1024 2048"

for lm in $lambda_memory; do
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove.py
  python3 /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_all_remove-local.py

  aws lambda update-function-configuration --function-name efs-test --handler random-write.lambda_handler --memory-size $lm
  aws lambda update-function-configuration --function-name tmp-test --handler random-write.lambda_handler --memory-size $lm

  sleep 70

  for bs in $bs_set; do

    sleep 10
    aws lambda update-function-configuration --function-name efs-test --memory-size 256
    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
    sleep 20
    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
    sleep 40

    python3 ./bs_set/bs_$bs.py
    sleep 60

  done

  aws lambda update-function-configuration --function-name efs-test --handler sequence-write.lambda_handler
  aws lambda update-function-configuration --function-name tmp-test --handler sequence-write.lambda_handler

  sleep 60
  for bs in $bs_set; do

    sleep 10
    aws lambda update-function-configuration --function-name efs-test --memory-size 256
    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
    sleep 5
    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
    sleep 40

    python3 ./bs_set/bs_$bs.py
    sleep 60

  done

  #  aws lambda update-function-configuration --function-name efs-test --handler random-read.lambda_handler --memory-size $lm
  #  aws lambda update-function-configuration --function-name tmp-test --handler random-read.lambda_handler --memory-size $lm
  #
  #  for bs in $bs_set; do
  #
  #    sleep 10
  #    aws lambda update-function-configuration --function-name efs-test --memory-size 256
  #    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
  #    sleep 20
  #    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
  #    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
  #    sleep 40
  #
  #    python3 ./bs_set/bs_$bs.py
  #    sleep 60
  #
  #  done
  #
  #  aws lambda update-function-configuration --function-name efs-test --handler sequence-read.lambda_handler
  #  aws lambda update-function-configuration --function-name tmp-test --handler sequence-read.lambda_handler
  #
  #  for bs in $bs_set; do
  #
  #    sleep 10
  #    aws lambda update-function-configuration --function-name efs-test --memory-size 256
  #    aws lambda update-function-configuration --function-name tmp-test --memory-size 256
  #    sleep 5
  #    aws lambda update-function-configuration --function-name efs-test --memory-size $lm
  #    aws lambda update-function-configuration --function-name tmp-test --memory-size $lm
  #    sleep 40
  #
  #    python3 ./bs_set/bs_$bs.py
  #    sleep 60
  #
  #  done

  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh EFS /Users/manchan/Desktop/BigDataLab/Papers/file_rw_test-efs-$lm
  sh /Users/manchan/Desktop/programming/serverless-faas-workbench/aws/dynamodb/dynamodb_export_json.sh local /Users/manchan/Desktop/BigDataLab/Papers/file_rw_test-loc-$lm
done

#!/bin/bash

lambda_functions="random-read random-write sequence-read sequence-write dd"
bs_set="1MB" #1MB 1KB
efs_scale="20"
newline=$'\n'

for bs in $bs_set; do
  for es in $efs_scale; do
    echo $newline'---------------' $es '개 진행중 -----------------'$newline
    python3 ./$bs/request$es.py
    sleep 30
  done
done

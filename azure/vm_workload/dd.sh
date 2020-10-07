#!/bin/bash

concurrent_1=$(seq 1)
concurrent_10=$(seq 1 10)
concurrent_20=$(seq 1 20)
concurrent_50=$(seq 1 50)
concurrent_100=$(seq 1 100)

out_path="/mnt/jgfileshare2/out"

for cnt in $concurrent_1; do
  dd if=/dev/zero of=$out_path$cnt bs=1024 count=204800 &
done

exit
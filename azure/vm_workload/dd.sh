#!/bin/bash

concurrent=$(seq 0 100)

out_path="/mnt/jgfileshare2/out"

for cnt in $concurrent; do
  dd if=/dev/zero of=$out_path$cnt bs=1024 count=200000 &
done

exit

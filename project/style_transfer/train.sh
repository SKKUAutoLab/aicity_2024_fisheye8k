#!/bin/bash
echo "$HOSTNAME"
clear

# Directories
current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
project_dir=$(dirname "$current_dir")
root_dir=$(dirname "$project_dir")
src_dir="${root_dir}/src/cyclegan_pix2pix"
data="${root_dir}/data"
save_dir="${root_dir}/run/train/cyclegan_pix2pix"

# eval "$(conda shell.bash hook)"
# conda activate cyclegan
python $src_dir/train.py --dataroot $data/cyclegan_pix2pix/A2E --name a2e --model cycle_gan --checkpoints_dir $save_dir --load_size 1080 --crop_size 1080

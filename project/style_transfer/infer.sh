#!/bin/bash
clear
echo "$HOSTNAME"

# Directories
current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
project_dir=$(dirname "$current_dir")
root_dir=$(dirname "$project_dir")
src_dir="${root_dir}/src/cyclegan_pix2pix"
data="${root_dir}/data"
zoo_dir="${root_dir}/zoo"
save_dir="${root_dir}/run/generate/cyclegan_pix2pix"

eval "$(conda shell.bash hook)"
conda activate cyclegan
python $current_dir/data.py

python $src_dir/test.py --dataroot $data/aicity/aicity_2024_fisheye8k/images --name a2e --model test --no_dropout --checkpoints_dir $zoo_dir --results_dir $save_dir
python $src_dir/test.py --dataroot $data/aicity/aicity_2024_fisheye8k/images --name a2n --model test --no_dropout --checkpoints_dir $zoo_dir --results_dir $save_dir

python $src_dir/fake_build.py --name a2e --source_dataset $data/aicity/aicity_2024_fisheye8k --fake_images_path $save_dir
python $src_dir/fake_build.py --name a2n --source_dataset $data/aicity/aicity_2024_fisheye8k --fake_images_path $save_dir

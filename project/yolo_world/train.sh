#!/bin/bash
echo "$HOSTNAME"
clear

current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
project_dir=$(dirname "$current_dir")
root_dir=$(dirname "$project_dir")
src_dir="${root_dir}/src/yolo_world"
save_dir="${root_dir}/run/train/yolo_world"

eval "$(conda shell.bash hook)"
conda activate yolo-world
python $current_dir/data.py
$src_dir/tools/dist_train.sh $src_dir/configs/fisheye8k/yolo_world_x.py 2 --amp --work-dir $save_dir

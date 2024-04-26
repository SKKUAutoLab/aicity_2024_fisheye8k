#!/bin/bash
echo "$HOSTNAME"
clear

# Directories
current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
project_dir=$(dirname "$current_dir")
mon_dir=$(dirname "$project_dir")
runml_dir="${project_dir}/runml"
data_dir="${mon_dir}/data"
yolor_dir="${mon_dir}/src/yolor"
zoo_dir="${mon_dir}/zoo"

# Constants
train_cameras=(
    "train/camera3_a"
    "train/camera3_n"
    "train/camera5_a"
    "train/camera6_a"
    "train/camera8_a"
    "train/camera9_a"
    "train/camera10_a"
    "train/camera11_m"
    "train/camera12_a"
    "train/camera13_a_500"
    "train/camera13_a_779"
    "train/camera14_a"
    "train/camera15_a"
    "train/camera16_a"
    "train/camera17_a"
    "train/camera18_a"
)
val_cameras=(
    "val/camera1_a_test"
    "val/camera2_a_test"
    "val/camera4_a_e_m_n_test"
    "val/camera7_a_test"
    "val_syn/camera1"
    "val_syn/camera2"
    "val_syn/camera7"
)
test_cameras=(
    "test/camera19_a"
    "test/camera20_a"
    "test/camera21_a"
    "test/camera22_a"
    "test/camera23_a"
    "test/camera24_a"
    "test/camera25_a"
    "test/camera26_a"
    "test/camera27_a"
    "test/camera28_a"
    "test/camera29_a_n"
)

# Train
cd "${yolor_dir}" || exit
python -W ignore my_train.py \
    --root "${current_dir}" \
    --config "${current_dir}/config/yolor_d6_aicity_2024_fisheye8k_1920.yaml" \
    --weights "${zoo_dir}/yolor_d6_coco.pt" \
    --model "yolor_d6" \
    --fullname "yolor_d6_aicity_2024_fisheye8k_1920" \
    --save-dir "${current_dir}/run/train" \
    --device "cuda:0" \
    --epochs 300 \
    "$@"

# Done
cd "${current_dir}" || exit

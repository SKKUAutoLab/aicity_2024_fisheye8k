current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
src_dir="${current_dir}/src/yolo_world"
echo $src_dir

echo -e "\nInstall yolo-world library"
eval "$(conda shell.bash hook)"
conda create -y -n yolo-world python=3.8
conda activate yolo-world
pip install torch wheel albumentations tqdm
pip install -e $src_dir

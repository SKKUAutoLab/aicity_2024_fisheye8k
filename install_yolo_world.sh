current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
src_dir="${current_dir}/src/yolo_world"
echo $src_dir

echo -e "\nInstall yolo_world library"
eval "$(conda shell.bash hook)"
conda create -y -n yolo_world python=3.8
conda activate yolo_world
pip install torch wheel albumentations tqdm supervision

git clone --branch v2.1.0 https://github.com/open-mmlab/mmcv.git $src_dir/third_party/mmcv
cd $src_dir/third_party/mmcv
pip install -r requirements.txt
pip install -U .
git clone --branch v3.3.0 https://github.com/open-mmlab/mmdetection.git $src_dir/third_party/mmdet
cd $src_dir/third_party/mmdet
pip install -U .
git clone https://github.com/onuralpszr/mmyolo.git $src_dir/third_party/mmyolo
cd $src_dir/third_party/mmyolo
pip install -U .

cd $src_dir
pip install -e .
current_file=$(readlink -f "$0")
current_dir=$(dirname "$current_file")
project_dir=$(dirname "$current_dir")
main_dir=$(dirname "$project_dir")
src_dir="${main_dir}/src/yolo_world"
data="${main_dir}/data"
save_dir="${main_dir}/run/predict/yolo_world"
#echo $data_dir/aic24_fisheye8k/images


eval "$(conda shell.bash hook)"
conda activate yolo-world
python $current_dir/data.py

python $src_dir/image_demo.py $src_dir/configs/fisheye8k/yolo_world_x.py zoo/yolo_world_epoch_100.pth $data/aic24_fisheye8k/images 'Bus,Bike,Car,Pedestrian,Truck' --topk 100 --threshold 0.2 --output-dir $save_dir

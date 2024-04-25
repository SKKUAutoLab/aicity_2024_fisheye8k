conda create -n yolo-world python=3.8 -y
conda activate yolo-world
pip install torch wheel -q
pip install -e .
pip install -U albumentations

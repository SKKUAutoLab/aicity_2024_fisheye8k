# [CVPRW 2024] Improving Object Detection to Fisheye Cameras with Open-Vocabulary Pseudo-Label Approach

This repository contains the source code for AI City Challenge 2024 Track 4 (Road Object Detection in Fish-Eye Cameras).

- Team Name: SKKU-AutoLab 
- Team ID: 05

___

## Setting up

### Organization
The project directory should look like this:
```
aicity_2024_fisheye8k
    |__ data
    |   |__ aicity
    |       |__ aicity_2024_fisheye8k
    |             |__ test
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels (Pseudo-labels from YOLO-World)
    |             |     ...
    |             |__ train
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels
    |             |     ...
    |             |__ train_syn (Synthesis nighttime images)
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels
    |             |     ...
    |             |__ val
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels
    |             |     ...
    |             |__ val_syn ((Synthesis nighttime images))
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels
    |             |     ...
    |             ...  
    |__ project
    |     |__ aicity_2024_fisheye8k
    |           |__ config
    |           |__ run
    |           |     |__ predict
    |           |     |     |__ aicity_2024_fisheye8k
    |           |     |           |__ submission
    |           |     |                 |__ results.json (Final submission results)
    |           |     |__ train
    |           |__ gen_submission.py
    |           |__ run_predict.sh
    |           |__ run_train.sh
    |__ src
    |     |__ cyclegan_pix2pix
    |     |__ mon
    |     |__ yolo_world
    |     |__ yolor
    |__ zoo (Pretrained weights)            
```

### Installation
The code was implemented and tested on Ubuntu 22.04, Python 3.11 and PyTorch (>=v1.13.0) with conda environment. 

The pretrained weights, data, and running environments are included in a Docker image for ease of distribution.

Installation using Docker (recommended):
```bash
docker run --name aicity_2024_fisheye8k --gpus all -it skkuautolab/aicity_2024_fisheye8:latest
```

---

## Inference
Enter the Docker container and run the following commands:

```bash
conda activate mon
cd aicity_2024_fisheye8k/project/aicity_2024_fisheye8k
./run_predict.sh
```

The final submission results will be saved in: `aicity_2024_fisheye8k/project/aicity_2024_fisheye8k/run/predict/aicity_2024_fisheye8k/submission/results.json`.

---

## Training
Enter the Docker container and run the following commands:

### Style transfer train/test

- To train the model, please run as bellow:
```bash
conda activate cyclegan
cd aicity_2024_fisheye8k/project/style_transfer
./train.sh
```
All training models and training results will be stored in: `run/train/cyclegan_pix2pix`
To view the training results per epoch, please look for the `html` file in: `run/train/cyclegan_pix2pix` directory.

- To generate synthesis dataset, run the `infer.sh` script:
```bash
conda activate cyclegan
cd aicity_2024_fisheye8k/project/style_transfer
./infer.sh
```
Synthesis images and new synthetic dataset will be generated automatically. All generated images and additional datasets will be stored in `run/generate`

### YOLO-World train/test

- Install the environment:
```bash
cd aicity_2024_fisheye8k
./install_yolo_world.sh
```
_It can take a while to install all dependencies._

- To train the model, please run as bellow:
```bash
conda activate yolor_world
cd aicity_2024_fisheye8k/project/yolo_world
./train.sh
```
All training models and training results will be stored in: `run/train/yolo_world`

- For inferencing, run the `predict.sh` script:
```bash
conda activate yolor_world
cd aicity_2024_fisheye8k/project/yolo_world
./predict.sh
```
New annotations and results will be generated and stored in `/run/predict/yolo_world`

### YOLOR-D6

- To train the model, please run as bellow:
```bash
conda activate mopn
cd aicity_2024_fisheye8k/project/aicity_2024_fisheye8k
./run_train_1280.sh
./run_train_1536.sh
./run_train_1920.sh
```
All training models and training results will be stored in: `run/train/...`

---

## Contact
If you have any questions, feel free to contact `Long H. Pham`
([longpham3105@gmail.com](longpham3105@gmail.com) or [phlong@skku.edu](phlong@skku.edu))

# [CVPRW 2024] Improving Object Detection to Fisheye Cameras with Open-Vocabulary Pseudo-Label Approach

This repository contains the source code for 2024 AI City Challenge Track 4 (Road Object Detection in Fish-Eye Cameras).

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
    |             |     |     |__ labels
    |             |     ...
    |             |__ train
    |             |     |__ <camera_id>
    |             |     |     |__ images
    |             |     |     |__ labels
    |             |     ...
    |             |__ val
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
docker run --name aicity_2024_fisheye8k --gpus all -it phlong/aicity_2024_fisheye8k
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

### Train Detectors


---

## Contact
If you have any questions, feel free to contact `Long H. Pham`
([longpham3105@gmail.com](longpham3105@gmail.com) or [phlong@skku.edu](phlong@skku.edu))

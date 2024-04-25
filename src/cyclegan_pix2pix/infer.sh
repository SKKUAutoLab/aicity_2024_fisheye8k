python test.py --dataroot datasets/fisheye8k/ --name a2e --model test --no_dropout
python test.py --dataroot datasets/fisheye8k/ --name a2n --model test --no_dropout
python fake_build.py --name a2e
python fake_build.py --name a2n

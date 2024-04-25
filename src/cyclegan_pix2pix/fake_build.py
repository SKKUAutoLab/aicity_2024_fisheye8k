import os
import argparse
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description='export fake synthesis dataset')
    parser.add_argument('--name', default='a2e', help='a2e, a2n')
    parser.add_argument('--source_dataset', default='./datasets/fisheye8k', help='')
    parser.add_argument('--fake_images_path', default='./results', help='image path')
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    args = parse_args()
    print('Buidling synthesis dataset')
    src = os.path.abspath(args.source_dataset)
    des = f'{args.fake_images_path}/fiskeye8k_{args.name}'
    os.makedirs (des, exist_ok=True)
    for dir in ['train', 'val']:
        os.makedirs(os.path.join(des, dir), exist_ok=True)
        for cam in os.listdir(os.path.join(src, dir)):
            os.makedirs(os.path.join(des, dir, cam), exist_ok=True)
            for folder in os.listdir(os.path.join(src, dir, cam)):
                os.makedirs(os.path.join(des, dir, cam, folder), exist_ok=True)
                if folder == 'images':
                    for img in os.listdir(os.path.join(src, dir, cam, folder)):
                        
                        # copy image
                        fake_img = img.replace('.png', f'_fake.png')
                        shutil.copyfile(os.path.join(args.fake_images_path, args.name, 'test_latest/images', fake_img), os.path.join(des, dir, cam, folder, fake_img))
                if folder == 'annotations':
                    for ann in os.listdir(os.path.join(src, dir, cam, folder)):
                        shutil.copyfile(os.path.join(src, dir, cam, folder, ann), os.path.join(des, dir, cam, folder, ann.replace('.xml', '_fake.xml')))
                if folder == 'labels':
                    for label in os.listdir(os.path.join(src, dir, cam, folder)):
                        shutil.copyfile(os.path.join(src, dir, cam, folder, label), os.path.join(des, dir, cam, folder, label.replace('.txt', '_fake.txt')))
    print(f'done: new data is at {os.path.abspath(des)}')

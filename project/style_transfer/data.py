import os
import argparse
import shutil
import glob
import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description='export fake synthesis dataset')
    parser.add_argument('--name', default='a2e', help='a2e, a2n')
    parser.add_argument('--source_data', default='./data/aic24_fisheye8k', help='')
    parser.add_argument('--fake_images_path', default='./results', help='image path')
    parser.add_argument('-q', action='store_true', help='quiet')
    args = parser.parse_args()
    return args
    
if __name__ == '__main__':
    args = parse_args()
    print('Copying training images...')
    src = os.path.abspath(args.source_data)
    print(src)
    des = os.path.join(args.source_data,'images')
    if not os.path.exists(des):
        os.makedirs(des)
    else:
        img_files = glob.glob(args.source_data + '/images/*.png')
        if len(img_files) == 8000:
            print('Images already copied')
            exit()
    img_files = glob.glob(args.source_data + '/train/*/images/*.png') + glob.glob(args.source_data + '/val/*/images/*.png')
    for img in tqdm.tqdm(img_files):
        shutil.copy(img, des+'/'+os.path.basename(img))
    print('Done')

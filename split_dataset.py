# -*- coding: utf-8 -*-
'''
@Project ：Fruit and vegetables recognition 
@File    ：split_dataset.py
@Author  ：Jackwxiao
@Date    ：2022/5/4 20:52 
'''
import os
import glob
import random
import shutil
from PIL import Image

# 对所有图片进行RGB转化，并且统一调整大小，但不让图片发生变形扭曲，划分训练集和测试集
if __name__ == '__main__':
    # 定义常量
    test_split_ratio = 0.05  # 5% 作为测试集
    desired_size = 128  # 图片缩放后的统一大小 ,由硬件计算能力决定
    raw_path = './raw'

    # 保留路径下的目录和文件
    dirs = glob.glob(os.path.join(raw_path, "*"))
    # 保留目录部分，文件不要了
    dirs = [d for d in dirs if os.path.isdir(d)]
    print(f'Totally {len(dirs)} classes: {dirs}')

    # 对每个类别单独处理
    for path in dirs:
        path = path.split('\\')[-1]  # 只保留类别名称，去掉路径
        # 创建文件夹
        os.makedirs(f'train/{path}', exist_ok=True)
        os.makedirs(f'test/{path}', exist_ok=True)

        files = glob.glob(os.path.join(raw_path, path, '*.jpg'))
        files += glob.glob(os.path.join(raw_path, path, '*.JPG'))
        files += glob.glob(os.path.join(raw_path, path, '*.png'))
        files += glob.glob(os.path.join(raw_path, path, '*.jpeg'))
        files += glob.glob(os.path.join(raw_path, path, '*.PNG'))

        random.shuffle(files)  # 随机打乱
        boundary = int(len(files)*test_split_ratio)  # 计算测试集和训练集的边界

        for i, file in enumerate(files):  # 要拿到索引的话可以使用enumerate
            img = Image.open(file).convert('RGB')
            old_size = img.size
            ratio = float(desired_size / max(old_size))
            new_size = tuple([int(x * ratio) for x in old_size])  # 等比例缩放
            im = img.resize(new_size, Image.ANTIALIAS)  # Image.ANTIALIAS 缩放不会使图片模糊
            new_im = Image.new("RGB", (desired_size, desired_size))
            new_im.paste(im, (
                (desired_size - new_size[0]) // 2,
                (desired_size - new_size[1]) // 2
            ))

            assert new_im.mode == 'RGB'

            if i <= boundary:
                new_im.save(os.path.join(f'test/{path}', file.split('\\')[-1].split('.')[0] + '.jpg'))
            else:
                # print('i:', i)
                new_im.save(os.path.join(f'train/{path}', file.split('\\')[-1].split('.')[0] + '.jpg'))

    test_files = glob.glob(os.path.join('test', '*', '*.jpg'))
    train_files = glob.glob(os.path.join('train', '*', '*.jpg'))

    print(f'Totally {len(train_files)} files for training')
    print(f'Totally {len(test_files)} files for test')

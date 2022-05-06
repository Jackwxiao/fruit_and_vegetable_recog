# -*- coding: utf-8 -*-
'''
@Project ：Fruit and vegetables recognition 
@File    ：statistic_mean_std.py
@Author  ：Jackwxiao
@Date    ：2022/5/6 16:27 
'''
import os
import glob
import random
import shutil
import numpy as np
from PIL import Image

# 统计数苦衷的所有图片的每个通道的均值和 标准差
if __name__ == '__main__':
    train_files = glob.glob(os.path.join('train', '*', '*.jpg'))

    print(f'Totally {len(train_files)} files for trainning')
    result = []
    for file in train_files:
        img = Image.open(file).convert('RGB')
        img = np.array(img).astype(np.uint8)
        img = img/255
        result.append(img)

    print(np.shape(result))  ## [batchsize, h, w, c]
    mean = np.mean(result, axis=(0, 1, 2))
    std = np.std(result, axis=(0, 1, 2))
    print(mean)
    print(std)
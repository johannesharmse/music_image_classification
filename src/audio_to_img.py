from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import re
import random


count = 0

img_folder = "../additional/data"
genres = ["hip_hop", "electro"]

sample_duration = 4*1000 # 4 secs

if not os.path.exists(join(img_folder, "train/")):
    os.makedirs(join(img_folder, "train/"))
    
if not os.path.exists(join(img_folder, "test/")):
    os.makedirs(join(img_folder, "test/"))

    
for genre in genres:
    if not os.path.exists(join(img_folder, "train", genre, "/")):
        os.makedirs(join(img_folder, "train", genre, "/"))
        
    song_folder = join(img_folder, genre, "mp3_files/")

    song_files = [f for f in listdir(song_folder) if isfile(join(song_folder, f))]

    for f in song_files:
        song = AudioSegment.from_mp3(join(song_folder, f))

        for segment in range(0, len(song) - sample_duration, sample_duration):
            sample_start = segment
            sample_end = segment + sample_duration

            sample = song[sample_start:sample_end]
            sample = sample.raw_data
            sample = np.fromstring(sample, 'Int16')

            sample = np.convolve(sample, np.ones((1*1000,))/(1*1000), mode='valid')

            plt.figure()
            plt.plot(sample)
            plt.ylim([0, 17000])

            test_pic = np.random.choice([True, False], p=[0.2, 0.8])

            if test_pic:
                plt.savefig(join(img_folder, "test", re.sub(r'\W+', '', f) + str(segment//1000) + '.jpg'))
            else:
                plt.savefig(join(img_folder, "train", genre, re.sub(r'\W+', '', f) + str(segment//1000) + '.jpg'))


            plt.close()
            
            count += 1

            print(count)
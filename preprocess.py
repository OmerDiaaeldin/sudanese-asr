import os
import shutil
path = "Sudanese_dialect_speech_dataset/SDN Dialect Corpus v1.0/Dataset files/"
#create audio directory
try:
    os.mkdir(path + 'audio')
except FileExistsError:
    print("directory already exists")
#create transcript directory
try:
    os.mkdir(path + 'transcript')
except FileExistsError:
    print("directory already exists")
for dirname, _, filenames in os.walk(path):
    for filename in filenames:
        if(filename.split('.')[-1] == 'txt'):
            shutil.move(path + filename, path + 'transcript/' + filename)
        else:
            shutil.move(path + filename, path + 'audio/' + filename)
            
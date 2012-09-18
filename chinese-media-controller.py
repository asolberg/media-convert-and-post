#!/usr/bin/python
import pickle
import os
from subprocess import call
import glob
import datetime

pickle_path = "/mnt/media-chinese/log/converted-files.p"
media_dir = "/mnt/media-chinese/"
web_dir = media_dir + "web-optimized-raw/"
web_dir_stitched = media_dir + "web-optimized-stitched/"


##Rename files based on date
os.chdir(media_dir)
allfiles = os.listdir(media_dir)
for filename in allfiles:
        #print filename
        if not os.path.isfile(filename):
                continue
        t = os.path.getmtime(filename)
        v= datetime.datetime.fromtimestamp(t)
        x = v.strftime('%Y%m%d')
        loop = 1
        iterator = 1
        temp_name = x + "_" + str(iterator) + '.mp4'
        while temp_name != filename:
                if not os.path.exists(temp_name):
                        os.rename(filename, temp_name)
                        filename=temp_name
                else:
                        iterator+=1
                        temp_name = x + '_' + str(iterator) + '.mp4'



#Load log file
if os.path.exists(pickle_path):
        pickle_file = open(pickle_path, 'rb')
        converted_files = pickle.load(pickle_file)
        pickle_file.close()
else:
        converted_files = {}


#Convert files that have not been converted yet
os.chdir(media_dir)
for filename in os.listdir(media_dir):
        if os.path.isfile(filename):
                if filename not in converted_files:
                        print str(filename) + " not in pickle directory, running compression...."
                        call('HandBrakeCLI -i ' + media_dir + filename + ' -o '
+ web_dir + filename[:-4] + '_small.m4v ' + '-w 640 --preset="sfwhs-moodle"', shell=True)
                        converted_files[filename] = 1
                        continue
                else:
                        continue
        else:
                continue 
pickle_file = open(pickle_path, 'wb')
pickle.dump( converted_files, pickle_file)
pickle_file.close()

## Stitch together multiple files
os.chdir(web_dir)
all_dates = set()
files_to_stitch = list()
for filename in os.listdir(web_dir):
        all_dates.add(filename[:8])
for date_pattern in all_dates:
        files_to_stitch = glob.glob(web_dir + date_pattern + "*")
        stitch_cmd = "MP4Box "
        for file in files_to_stitch:
                stitch_cmd = stitch_cmd + " -cat " + file
#                print file
        stitch_cmd = stitch_cmd + " -new " + web_dir_stitched + date_pattern + "_full.m4v" 
        print "stitch command is " + stitch_cmd

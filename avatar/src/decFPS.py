"""Function decrease the FPS of the video to 25 
   only when FPS is less than 25

   takes
   video path as the argument
"""
import cv2

import os
import subprocess
import logging
import uuid

def dec_fps(vid: str):
    if not os.path.exists("temp_video"):
            os.mkdir("temp_video")
    unique_num = uuid.uuid4()
    output_video_pth = os.path.join("temp_video", str(unique_num)+".mp4")
    video = cv2.VideoCapture(vid)
    fps = fps = video.get(cv2.CAP_PROP_FPS)
    logging.info("INFO: FPS of video is {}".format(fps))
    ## check if fps of video is less then 30 
    if int(fps)<=25:
        return vid
    logging.warning("FPS greater then 25 decreaseing FPS.")
    c = 'ffmpeg -y -i ' + vid + ' -r 25 -c:v libx264 -b:v 3M -strict -2 -movflags faststart '+output_video_pth
    subprocess.call(c, shell=True)
    logging.info("INFO: Decreasing fps completed")
    return output_video_pth

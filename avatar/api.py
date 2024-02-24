'''Function sync the lip of the given audio
'''
##imports 
import uuid
import os
import requests
from datetime import datetime
import logging
import subprocess, platform

import boto3

import cv2

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.decFPS import dec_fps
# from src.decRES import dec_res_video
import main
import new_main

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
session = boto3.Session(
    aws_access_key_id= AWS_ACCESS_KEY_ID,
    aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
)
s3 = session.resource("s3")
BUCKET_NAME = "oi-avatar"
LOGGER = 'logger'

if not os.path.exists(LOGGER):
    os.mkdir(LOGGER)


@app.get("/healthy")
def healthy():
    return "healthy"
    
@app.get("/")
def homepage():
    return "home page"
    
@app.get("/api/v1/avatarGen")
def wav2lip(
    vid_path: str,
    file_name: str,
    output_url: str,
    audio_pth:str
    )->dict:
    try:
        unique_num = uuid.uuid4()
        start_time = datetime.now()
        # vid_path = dec_fps(vid_path)
        dec_res_video_pth = vid_path
        temp_audio_dir = "temp_audio"
        print("INFO: reading the audio file")
        temp_audio_pth = os.path.join(temp_audio_dir, str(unique_num))
        if not os.path.exists(temp_audio_dir):
            os.mkdir(temp_audio_dir)
            os.mkdir(temp_audio_pth)
        with open(temp_audio_pth+".wav", "wb") as f:
            f.write(requests.get(audio_pth).content)
        with open(temp_audio_pth+".mp3", "wb") as f:
            f.write(requests.get(audio_pth).content)

        audio_pth = temp_audio_pth+".wav"
        audio_pth_mp3 = temp_audio_pth+".mp3"
        print("INFO: Decreasing resolution")
        print("INFO: Resolution decreased at {}".format(vid_path))
        ### generating the sync video
        print("INFO: Avartar generation started")
        avatar_file = new_main.main(vid_path, audio_pth, audio_pth_mp3)
        if avatar_file:
            print("INFO: Avartar generation sucessfully completed")
            folder_name = "/".join(output_url.split("/")[-3:-1])
            print("INFO: UPloading to s3")
            my_bucket = s3.Bucket(BUCKET_NAME)
            my_bucket.upload_file(
                avatar_file, 
                os.path.join(folder_name, file_name), 
                ExtraArgs={'ACL':'public-read'}
                )
            total_time = datetime.now()-start_time
            print("INFO: File sucessfully uploaded")
            print("INFO: Total time taken: {}".format(total_time))
            print("INFO: Deleting audio file {}".format(audio_pth))
            if os.path.exists(audio_pth):
                os.remove(audio_pth)
            if os.path.exists(audio_pth_mp3):
                os.remove(audio_pth_mp3)
            print(f"INFO: Deleting video at {vid_path}")
            if os.path.exists(vid_path):
                os.remove(vid_path)
            print(f"Deleting fps lower video {dec_res_video_pth}")
            if os.path.exists(dec_res_video_pth):
                os.remove(dec_res_video_pth)
            if os.path.exists(avatar_file):
                os.remove(avatar_file)
            output_url = "/".join(str(output_url).split("/")[:-1]) + "/"+file_name
            return_responce = {
                "status" : True,
                "time_taken": total_time,
                "saved_at": output_url
            }
            return return_responce
        else:
            print("Rolling back avatar not made")
            print("INFO: Deleting audio file {}".format(audio_pth))
            if os.path.exists(audio_pth):
                os.remove(audio_pth)
            if os.path.exists(audio_pth_mp3):
                os.remove(audio_pth_mp3)
            print(f"INFO: Deleting video at {vid_path}")
            if os.path.exists(vid_path):
                os.remove(vid_path)
            print(f"Deleting fps lower video {dec_res_video_pth}")
            if os.path.exists(dec_res_video_pth):
                os.remove(dec_res_video_pth)
            return {
            "status": False,
            "message": "Failed"
            }

    except Exception as e:
        print("WARNING: Error due to {}".format(e))
        return {
            "status": False,
            "message": "Failed"
        }

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host= "0.0.0.0",
        port= 5000,
        reload= True
    )
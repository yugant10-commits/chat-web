FROM python:3.7
WORKDIR wav2lip
RUN apt-get update && \
    apt-get install -y libsndfile1-dev && \
    apt-get install -y ffmpeg
RUN pip install --upgrade pip
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install opencv-python-headless 
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "api.py"]
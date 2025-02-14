FROM anibali/pytorch:2.0.1-cuda11.8-ubuntu22.04
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install 'accelerate>=0.26.0' -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python","boto.py"]
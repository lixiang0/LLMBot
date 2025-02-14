# 悠然AI助理

悠然AI助理的目标是打造一个智能的机器人助理。

# 主页
<img src='home.png' width=800>

# 部署

## 源码形式
```
conda create -p ./env python=3.12
pip install -r requirements.txt
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install 'accelerate>=0.26.0'
git clone https://github.com/lixiang0/ChatBot
cd ChatBot
python boto.py

```

## docker
```
sudo docker build -t llm:1.0 .
#注意修改路径
sudo docker run -itd  --name llm --network=host --gpus all -v /opt/llm/ChatBot:/app  -p 8181:8181 --restart always llm:1.0 python boto.py
```


可以看到输出：
```
Bottle v0.12.19 server starting up (using PasteServer())...
Listening on http://0.0.0.0:8890/
Hit Ctrl-C to quit.

serving on 0.0.0.0:8890 view at http://127.0.0.1:8890
```
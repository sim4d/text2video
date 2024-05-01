# 纯 Python 实现的文章转视频小工具
用 Python 实现的文章转视频小工具，可以轻松将包含图文的网页文章转为视频。

## 具体步骤
- 用requests获取文章内容
- 用edge-tts生成语音和字幕
- 用BeautifulSoap获取文章图片
- 用moviepy将图片生成视频，并叠加语音和字幕

## 开发环境
Windows WSL + Ubuntu 22.04.4 LTS，Python 3.10
安装依赖
pip install -r requirements.txt

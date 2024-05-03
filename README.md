# 纯粹 Python 构建的文章转视频神器
运用 Python 代码，便能方便地将图文并茂的网页文章转换成视频。

## 具体步骤
- 通过 requests 获取文章内容
- 借 edge-tts 生成语音及字幕
- 利用 BeautifulSoap 抓取文章图像
- 再借助 moviepy 将图像拼接为视频，并匹配语音与字幕

## 项目特点
- 完全基于 Python 及其第三方应用库，无需依赖于stable-diffusion/midjourney等大模型。
- 实现以微信公众号文章为例，函数的具体查询是基于公众号文章的特点 (如 make_audio.py 里的 get_title / get_wechat_article 等函数)。若用于其它类型文章，可能需要调整查询的tag和class信息

## 开发环境
Windows WSL + Ubuntu 24.04 LTS，Python 3.12

安装pip和ImageMagick

```bash
sudo apt install python3-pip
sudo apt install imagemagick
```

安装依赖

```python
python3 -m venv my_venv
source ./my_venv/bin/activate
pip3 install -r requirements.txt
```

设置url，运行text2video.py

```
python3 text2video.py
```

## License: MIT
本项目采用 MIT 许可证授权。

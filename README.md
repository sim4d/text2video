# 纯粹 Python 构建的文章转视频神器
运用 Python 代码，便能方便地将图文并茂的网页文章转换成视频。

## 具体步骤
- 通过 requests 获取文章内容
- 借 edge-tts 生成语音及字幕
- 利用 BeautifulSoap 抓取文章图像
- 再借助 moviepy 将图像拼接为视频，并匹配语音与字幕

## 项目特点
- 纯粹基于 Python 及其第三方应用库，不依赖于stable-diffusion/midjourney等大模型。
- 实现以微信公众号文章为例，好多函数的具体查询都是基于公众号文章。
-- 比如 make_audio.py 里的 get_title / get_wechat_article 等函数
-- 如果用于其它类型文章，可能需要更改查询tag和class信息

## 开发环境
Windows WSL + Ubuntu 24.04 LTS，Python 3.10

安装pip和ImageMagick

```bash
sudo apt install python3-pip
sudo apt-get install imagemagick
```

安装依赖

```python
pip install -r requirements.txt
```

## License: MIT
本项目采用 MIT 许可证授权。

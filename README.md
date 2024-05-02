# 纯粹 Python 构建的文章转视频神器
运用 Python 代码，便能方便地将图文并茂的网页文章转换成视频。

## 具体步骤
- 通过 requests 获取文章内容
- 借 edge-tts 生成语音及字幕
- 利用 BeautifulSoap 抓取文章图像
- 再借助 moviepy 将图像拼接为视频，并匹配语音与字幕

## 开发环境
Windows WSL + Ubuntu 22.04.4 LTS，Python 3.10

安装依赖

```python
pip install -r requirements.txt
```

moviepy 还依赖 ImageMagick
```bash
sudo apt-get install imagemagick
```

## License: MIT
本项目采用 MIT 许可证授权。

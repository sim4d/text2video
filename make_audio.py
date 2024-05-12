import asyncio
import re
import requests
from bs4 import BeautifulSoup
from edge_tts.communicate import Communicate
from edge_tts.submaker import SubMaker

# get title and account
def get_title(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # change Element as needed if {url} is not WeChat Public Account article
    title = soup.find('h1', {'class': 'rich_media_title'}).get_text().strip()
    if not title:
        title = "(缺省标题)"

    # change Element as needed if {url} is not WeChat Public Account article
    pub_account = soup.find('a', {'id': 'js_name'}).get_text().strip()
    if not pub_account:
        pub_account = "(缺省公众号)"

    return title, pub_account

# get article contents
def get_wechat_article(url):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # change Element as needed if {url} is not WeChat Public Account article
    article_content = soup.find('div', {'class': 'rich_media_content'}).get_text().strip()

    return article_content

# speak article
async def speak_article(url, voice="zh-CN-YunjianNeural", output_file="test.mp3", vtt_file="test.vtt"):
    text = get_wechat_article(url)
    # add \r\n for each Chinese sentence
    modified_text = re.sub(r'(，|：|；|。|！|？|…)\s*', r'\1\r\n', text)

    communicate = Communicate(modified_text, voice)
    submaker = SubMaker()
    with open(output_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(vtt_file, "w", encoding="utf-8") as file:
        # one Chinese sentence as one word in edge_tts
        file.write(submaker.generate_subs(words_in_cue=1))


# change voice as needed
# voice = "zh-CN-XiaoyiNeural"
voice = "zh-CN-YunjianNeural"

# main
async def _main() -> None:
    url = 'https://mp.weixin.qq.com/s/t8c07-3gKjKXW4MOIwW5aQ'
    await speak_article(url)

if __name__ == '__main__':
    asyncio.run(_main())


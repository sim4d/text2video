import moviepy.editor as mp
import moviepy.video.tools.subtitles as mps
import webvtt
import os
import asyncio
from datetime import datetime
import argparse

from make_audio import speak_article, get_title
from save_image import save_images

# set url
URL = 'https://mp.weixin.qq.com/s/t8c07-3gKjKXW4MOIwW5aQ'
# use r-string for Windows compatibility
FONT_PATH = r'fonts/NotoSerifSC-Bold.otf'
# default voice
VOICE = 'zh-CN-YunjianNeural'


def generate_video(images_dir, audio_path, vtt_file, font_path, output_path, front_txt, title_txt):
    """
    Generates a video from a directory of images, an audio file, and an SRT subtitle file.
    """

    audio = mp.AudioFileClip(audio_path)
    audio_duration = audio.duration

    # Load the images
    images = [os.path.join(images_dir, image) for image in os.listdir(images_dir) if image.endswith(('.png', '.jpg', '.jpeg'))]
    images.sort(key=lambda x: x.lower())
    print(images)

    # add 1 more for front page: len(images) + 1
    image_duration = int(audio_duration / (len(images) + 1))
    # add 1 second padding
    image_duration = image_duration + 1
    print(f"\naudio_duration: {audio_duration}")
    print(f"\nimage_duration: {image_duration}")

    # specify the size of each frame (width, height)
    frame_size = (640, 480)
    width, height = frame_size
    up_position = int(height * 0.2)

    clips = []

    # add front page
    front_clip = mp.TextClip(front_txt, color='black', bg_color='white', font=font_path, align='West', kerning=5, fontsize=18)
    front_col = front_clip.on_color(size=frame_size, color=(255,255,255), pos=('center', up_position))

    title_clip = mp.TextClip(title_txt, color='darkred', bg_color='white', font=font_path, align='West', kerning=5, fontsize=21)

    # use half of image_duration for both front page and back page
    txt_clip = mp.CompositeVideoClip([front_col, title_clip.set_position('center')], size=frame_size).set_duration(image_duration / 2)
    clips.append(txt_clip)

    # add images into clips
    for image_path in images:
        clip = mp.ImageClip(image_path)
        image_ratio = min(width / clip.w, height / clip.h)
        scaled_clip = clip.resize(height=int(clip.h * image_ratio))
        image_clip = mp.CompositeVideoClip([scaled_clip.set_position('center').set_duration(image_duration)], size=frame_size)
        clips.append(image_clip)

    # add back page
    clips.append(txt_clip)

    video = mp.concatenate_videoclips(clips, method='compose').set_position('center').set_duration(audio_duration)

    # read the WebVTT file
    captions = webvtt.read(vtt_file)

    # convert to SRT and save
    srt_file = vtt_file + '.srt'
    captions.save_as_srt(srt_file)

    # define a lambda function that takes text and returns a TextClip
    generator = lambda txt: mp.TextClip(txt, font=font_path, color='white', bg_color='black', method='caption',
                        size=(min(len(txt) * 17, width * 0.8), 30 * (1 + int(len(txt) / 34)))
                        )

    # calculate the position from the bottom
    bottom_position = int(height * 0.8)

    # load your subtitles from SRT file
    subtitle_clip = mps.SubtitlesClip(srt_file, generator).set_position(('center', bottom_position)).set_duration(audio_duration).set_opacity(0.75)

    final_clip = mp.CompositeVideoClip([video, subtitle_clip], size=frame_size)

    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile(output_path, fps=24, codec='libx264')


def main(url, font_path=FONT_PATH, voice=VOICE):
    # get date str
    date_str = datetime.now().strftime('%Y-%m-%d')

    # set the paths to your media files
    images_dir = "images-" + date_str
    audio_path = "article-" + date_str + ".mp3"
    vtt_path = "article-" + date_str + ".vtt"
    output_path = "article-" + date_str + ".mp4"

    print("\n########## speak_article ##########")
    title, pub_account = get_title(url)
    front_txt = f"文章内容来自微信公众号，版权属于原作者\n如喜欢内容，欢迎关注原公众号"

    title_txt = f"公众号：{pub_account}\n标  题：{title}"

    asyncio.run(speak_article(url, voice=voice, output_file=audio_path, vtt_file=vtt_path))
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"The file '{audio_path}' does not exist.")

    if not os.path.isfile(vtt_path):
        raise FileNotFoundError(f"The file '{vtt_path}' does not exist.")

    print("\n########## save_images ##########")
    saved_images = True
    saved_images = save_images(url, save_dir=images_dir)
    if not saved_images:
        raise FileNotFoundError(f"No image in sub dir: '{images_dir}', please re-try.")

    print("\n########## generate_video ##########")
    generate_video(images_dir, audio_path, vtt_path, font_path, output_path, front_txt, title_txt)


if __name__ == "__main__":
    url = URL
    voice = VOICE

    parser = argparse.ArgumentParser(description="A simple Text to Video conversion tool based on Pyhon libs.")
    parser.add_argument("--url", help="Specify url info", action="store")
    parser.add_argument("--voice", help="Specify voice info", action="store")

    args = parser.parse_args()
    if args.url:
        url = args.url
        print(f"\nCustomized url: {url}\n")

    if args.voice:
        voice = args.voice
        print(f"\nCustomized voice: {voice}\n")


    main(url, voice=voice)



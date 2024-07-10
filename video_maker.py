import ffmpeg
import os
import sys

def video_with_image(input_files, output_video, codec):
    ffmpeg.input(input_files[0], loop=1).output(
        ffmpeg.input(input_files[1]),
        output_video,
        vcodec=codec,
        r=30,
        pix_fmt='yuv420p',
        vf='scale=1920:1080',
        acodec='aac',
        audio_bitrate='192k',
        shortest=None,
    ).run(overwrite_output=True)

def video_with_gif(input_files, output_video, codec):
    ffmpeg.input(input_files[0], stream_loop=-1).output(
        ffmpeg.input(input_files[1]),
        output_video,
        vcodec=codec,
        acodec='aac',
        audio_bitrate='192k',
        shortest=None,
    ).run(overwrite_output=True)

def make_video(input_files, output_video, codec = "libx264"):
    """
    input_files[0] is image
    input_files[1] is audio
    """
    print(input_files)
    for i in range(2):
        unformatted_file = input_files[i]
        input_files[i] = unformatted_file.split("file:///")[-1].strip()

        if sys.platform.startswith('linux'):
            input_files[i] = "/" + input_files[i]

        if not os.path.exists(input_files[i]):
            raise FileNotFoundError("Error: File not Found:", input_files[i])
        
        extension = (input_files[0].split(".")[-1]).strip()
        if (extension == "gif"):
            video_with_gif(input_files, output_video, codec)
        else:
            video_with_image(input_files, output_video, codec)

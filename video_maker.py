import ffmpeg

# Define the input and output files
#input_image = 'in.jpg'
#input_audio = 'in.mp3'
#output_video = 'output.mp4'
def make_video(input_image, input_audio, output_video):
    # Build the FFmpeg command
    ffmpeg.input(input_image, loop=1).output(
        ffmpeg.input(input_audio),
        output_video,
        vcodec='libx264',
        r=30,
        pix_fmt='yuv420p',
        vf='scale=1920:1080',
        acodec='aac',
        audio_bitrate='192k',
        shortest=None
    ).run()
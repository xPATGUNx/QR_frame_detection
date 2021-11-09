import cv2 as cv
import os
import subprocess
from Python.QRCodeTools import generate_qr_codes, delete_generated_qr_codes


def render_test_video(path_to_video: str, *, frame_rate: float, qr_code_offset: int, format_profile: str = None,
                      format_level: str = None):
    """
    Dedicated function to render test videos for Frame Error Detection including a QR Code via a FFMPEG command call.
    :param path_to_video: string of video path.
    :param frame_rate: float value of the playback frame rate of the selected video.
    :param qr_code_offset: An integer value that sets the offset of the qr code position.
    :param format_profile: A string of the specified format profile of H264.
    :param format_level: A string of the specified format level of H264.
    """
    total_amount_of_frames = get_total_amount_of_frames_from_video(path_to_video)
    amount_of_leading_zeros = len(str(total_amount_of_frames))
    base_name = os.path.basename(path_to_video)
    name_of_rendered_video = f'Rendered_Videos/qr_test_vid_{total_amount_of_frames}_frames_{frame_rate}fps_{base_name}'
    if os.path.exists(name_of_rendered_video):
        os.remove(name_of_rendered_video)

    delete_generated_qr_codes()
    generate_qr_codes(total_amount_of_frames)

    if format_profile and format_level is not None:
        ffmpeg_command = f'ffmpeg -r {frame_rate} -i "{path_to_video}" ' \
                         f'-r {frame_rate} -i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png ' \
                         f'-filter_complex "[0:v][1:v] ' \
                         f'overlay={qr_code_offset}:{qr_code_offset}" ' \
                         f'-profile:v {format_profile} -level:v {format_level} ' \
                         f'{name_of_rendered_video} ' \
                         f'-vframes {total_amount_of_frames}'

        print(ffmpeg_command)
        pass_command(ffmpeg_command)

    else:
        ffmpeg_command = f'ffmpeg -r {frame_rate} -i "{path_to_video}" ' \
                         f'-r {frame_rate} -i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png ' \
                         f'-filter_complex "[0:v][1:v] ' \
                         f'overlay={qr_code_offset}:{qr_code_offset}" {name_of_rendered_video} ' \
                         f'-vframes {total_amount_of_frames}'

        print(ffmpeg_command)
        pass_command(ffmpeg_command)

    print('Video render done.')
    print(f'Location of rendered video: Frame Drop Detection/{name_of_rendered_video}')


def render_qr_code_clip(path_to_video: str, *, frame_rate: float, total_amount_of_frames: int, resolution: int = 1000,
                        scale_of_qr_code_image: int = 40):
    """
    Function to call a FFMPEG command to render a video clip of a QR Code sequence.
    :param path_to_video: A string to the directory where you want to save the video to.
    :param frame_rate: A float value to set the frame rate of the video clip.
    :param total_amount_of_frames: An integer value to set the total amount of to be created QR-Codes/Frames.
    :param resolution: An integer value that sets the resolution of the to be rendered video clip.
    :param scale_of_qr_code_image: An integer value to set the scale of the qr codes
    """
    amount_of_leading_zeros = len(str(total_amount_of_frames))
    if os.path.exists(path_to_video):
        os.remove(path_to_video)
    delete_generated_qr_codes()
    generate_qr_codes(total_amount_of_frames, img_scale=scale_of_qr_code_image)

    ffmpeg_command = f'ffmpeg -r {frame_rate} -f image2 -s {resolution}x{resolution} ' \
                     f'-i Images/QR_Code_Frame_%0{amount_of_leading_zeros}d.png -vframes {total_amount_of_frames} ' \
                     f'-vcodec libx264 -crf 25 -pix_fmt yuv420p {path_to_video}'

    print(ffmpeg_command)
    pass_command(ffmpeg_command)


def pass_command(cmd_line: str):
    subprocess.check_output(cmd_line, shell=True)


def get_total_amount_of_frames_from_video(path_to_video: str):
    """
    Function to get total amount of frames in a video file.
    :param path_to_video: Path string to a video file.
    :return: An integer of the total amount of frames in a video file
    """
    cap = cv.VideoCapture(path_to_video)
    total_amount_of_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    print(total_amount_of_frames)

    return total_amount_of_frames
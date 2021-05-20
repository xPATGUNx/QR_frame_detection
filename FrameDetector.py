import os
import time

import cv2 as cv
from pyzbar.pyzbar import decode


class FrameDetector:
    def __qr_code_detection(self, video_file_path):
        cap = cv.VideoCapture(video_file_path)
        frame_index_list = []

        if not cap.isOpened():
            print("Error opening video stream or file")

        print('Scanning for frame IDs...')
        start = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                text_data = str(self.__qr_code_scanner(frame))
                if not text_data == 'None':
                    frame_index_list.append(int(text_data))
                else:
                    frame_index_list.append('QR code was not readable.')
            else:
                break
        end = time.time()
        cap.release()
        cv.destroyAllWindows()
        print('Scan completed after ' + str(end - start) + ' seconds.')
        return frame_index_list

    @staticmethod
    def __qr_code_scanner(obj):
        qr_code = decode(obj)
        for code in qr_code:
            data = code.data.decode('utf-8')
            # print(data)
            return data

    @staticmethod
    def __test_data_file_writer(scan_list: list, video_file_path, expected_amount_of_frames):
        base_name = os.path.basename(video_file_path)
        timestr = time.strftime("%Y %m %d-%H%M%S")
        scan_data_name = ('Scan Results ' + timestr + str(base_name) + '.txt')
        scan_data_dir = ('Scan Results/' + scan_data_name)
        scan_data = open(scan_data_dir, 'w')
        scan_data.write('Detected frames for file "' + video_file_path + '":\n')

        for current_frame in range(1, expected_amount_of_frames + 1):
            occurrence = scan_list.count(current_frame)
            scan_data.write('Frame ' + str(current_frame) + ' occurred ' + str(occurrence) + ' times.\n')
        not_readable_frames = scan_list.count('QR code was not readable.')
        scan_data.write('QR code was not readable for ' + str(not_readable_frames) + ' frames.')
        scan_data.close()
        print('"' + scan_data_name + '"' + ' has been created.')

    @staticmethod
    def __list_frames_for_occurrences(scan_list: list, expected_amount_of_frames):
        list_of_problematic_frames = []
        for current_frame in range(1, expected_amount_of_frames + 1):
            occurrence = scan_list.count(current_frame)
            if occurrence != 1:
                list_of_problematic_frames.append('Frame ' + str(current_frame) +
                                                  ' occurred ' + str(occurrence) + ' times.')
        return list_of_problematic_frames

    def frame_drop_detection(self, video_file_path: str, expected_amount_of_frames: int):
        video_frames = self.__qr_code_detection(video_file_path)
        self.__test_data_file_writer(video_frames, video_file_path, expected_amount_of_frames)
        list_of_detected_frame_drops = self.__list_frames_for_occurrences(video_frames, expected_amount_of_frames)
        return list_of_detected_frame_drops


if __name__ == '__main__':
    # frame_drop_detection('No_QR_Test.mp4', 180)
    # frame_drop_detection('QRCodeScreenCap.mp4', 180)
    # frame_drop_detection('MacBook Pro QuickTime Capture.mp4', 180)
    # frame_drop_detection('MacBook Pro Cubase  Capture 01.mp4', 180)
    # frame_drop_detection('MacBook Pro Cubase  Capture 02.mp4', 180)
    # frame_drop_detection('MacBook Pro QuickTime 60 FPS.mp4', 150)

    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 60 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 60 FPS Cubase 60 FPS Capture 2.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 59.97 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 50 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 30 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 29.97 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 25 FPS Cubase 60 FPS Capture 1.mp4', 150)
    # frame_drop_detection('Intensity Pro 4K Captures/MacBook Pro 24 FPS Cubase 60 FPS Capture 1.mp4', 150)

    # frame_drop_detection('LG4K/LG4K 30FPS Video 60FPS Capture.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 60FPS Video 60FPS Capture.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 60 FPS Video 120 FPS Capture.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 60FPS VLC 120FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 60FPS VLC 60FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 59FPS VLC 59FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 59FPS VLC 59FPS OBS V2.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 50FPS VLC 50FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 30FPS VLC 30FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 29FPS VLC 29FPS OBS.mp4', 150)
    # frame_drop_detection('LG4K/LG4K 25FPS VLC 25FPS OBS.mp4', 150)

    # frame_drop_detection('Elgato/24 FPS.mp4', 150)
    # frame_drop_detection('Elgato/24 FPS new.mp4', 150)
    # frame_drop_detection('Elgato/25 FPS.mp4', 150)
    # frame_drop_detection('Elgato/29 FPS.mp4', 150)
    # frame_drop_detection('Elgato/29 fps new.mp4', 150)
    # frame_drop_detection('Elgato/30 FPS.mp4', 150)
    # frame_drop_detection('Elgato/59 FPS.mp4', 150)
    # frame_drop_detection('Elgato/50 FPS.mp4', 150)
    # frame_drop_detection('Elgato/60 FPS.mp4', 150)
    frame_detector = FrameDetector()
    frame_detector.frame_drop_detection('Video/Elgato/60 FPS.mp4', 150)

import os
import sys
from acrcloud.recognizer import ACRCloudRecognizer, ACRCloudRecognizeType

if __name__ == '__main__':

    '''This module can recognize ACRCloud by most of audio/video file. 
        Audio: mp3, wav, m4a, flac, aac, amr, ape, ogg ...
        Video: mp4, mkv, wmv, flv, ts, avi ...'''
    re = ACRCloudRecognizer(config)

    # recognize by file path, and skip 0 seconds from from the beginning of sys.argv[1].
    def check_file(song):
        re.recognize_by_file(song, 0)

    #buf = open(sys.argv[1], 'rb').read()
    # recognize by file_audio_buffer that read from file path, and skip 0 seconds from from the beginning of sys.argv[1].
    # print re.recognize_by_filebuffer(buf, 0)
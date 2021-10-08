import cv2


def get_video_metadata(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print('FPS, Resolution: ', fps, resolution)
    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]
    print(timestamps)
    cap.release()


def timestamp_from_milisec(ms):
    seconds = (ms/1000) % 60
    seconds = int(seconds)
    minutes = (ms/(1000*60)) % 60
    minutes = int(minutes)
    hours = (ms/(1000*60*60)) % 24
    if hours < 1:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

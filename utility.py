def get_video_metadata(path):
    """
    Use OpenCV to retrieve fps and resolution of a video file.
    
    :param path: Path to video file.
    """
    import cv2
    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    cap.release()
    return (fps, resolution)


def timestamp_from_ms(ms, show_ms=False):
    """
    Convert from milisecond to readable timestamp format. 
    
    :param ms: Time in miliseconds.
    :param show_ms: False: hh:mm:ss | True: mm:ss:ms
    """
    seconds = (ms/1000) % 60
    seconds = int(seconds)
    minutes = (ms/(1000*60)) % 60
    minutes = int(minutes)
    if not show_ms:
        hours = (ms/(1000*60*60)) % 24
        if hours < 1:
            return "%02d:%02d" % (minutes, seconds)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    else:
        milisecs = ms % 1000
        if minutes < 1:
            return "%02ds:%03dms" % (seconds, milisecs)
        return "%02dm:%02ds:%03dms" % (minutes, seconds, milisecs)

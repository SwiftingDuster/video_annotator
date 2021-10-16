import cv2, os, sys
import argparse

# create directories to store individual frames and their labels
os.makedirs("./labels", exist_ok=True)
os.makedirs("./images", exist_ok=True)

# parse the arguments used to call this script
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='name of video file', type=str)
parser.add_argument('--max_obj', help='Maximum number of objects followed', type=int, default=6)
parser.add_argument('--max_frames', help='Maximum number of objects followed', type=int, default=500000)
parser.add_argument('--thresh', help='Threshold for scene changes', type=float, default=20)
args = parser.parse_args()
max_obj = args.max_obj
max_frames = args.max_frames
thresh = args.thresh

fname = os.path.basename(args.name)[:-4]  # filename without extentsion
video = cv2.VideoCapture(args.name)  # Read video

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
ok, frame = video.read()
if not ok:
    print("Cannot read video file")
    sys.exit()

# h, w, _ = frame.shape
# import pdb; pdb.set_trace()
height = 1280
width = 720
initBB = None

frames = 1
prev_mean = 0
count = 0
while ok and frames <= max_frames:
    frame_diff = abs(frame.mean() - prev_mean)
    prev_mean = frame.mean()

    frame = cv2.resize(frame, (height, width))
    name = fname + '_' + str(frames).zfill(4)
    origFrame = frame.copy()

    key = cv2.waitKey(1) & 0xFF

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("s") or frames == 1 or frame_diff > thresh:
        trackers = cv2.MultiTracker_create()
        for i in range(max_obj):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv2.selectROI("Frame", frame, fromCenter=False)
            # create a new object tracker for the bounding box and add it
            # to our multi-object tracker
            if initBB[2] == 0 or initBB[3] == 0:  # if no width or height
                break
            # # start OpenCV object tracker using the supplied bounding box
            tracker = cv2.TrackerCSRT_create()
            trackers.add(tracker, frame, initBB)

    elif key == ord("q"):
        break

    if initBB is not None:
        (tracking_ok, boxes) = trackers.update(frame)

        # save image and bounding box
        if tracking_ok:
            if len(boxes) > 0:  # if there is a box that is being tracked
                if count < 5:
                    count += 1
                    cv2.imwrite('./images/' + name + '.jpg', origFrame)
                    with open('./labels/' + name + '.txt', 'a') as f:
                        for box in boxes:
                            p1 = (int(box[0]), int(box[1]))
                            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
                            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                            centre = [0.5 * (p1[1] + p2[1]) / w, 0.5 * (p1[0] + p2[0]) / h]
                            width, height = (box[3] / w, box[2] / h)
                            f.write(f'0 {centre[0]:.6f} {centre[1]:.6f} {width:.6f} {height:.6f}\n')
                else:
                    count = 0
                    trackers = cv2.MultiTracker_create()
        else:
            initBB = None

    cv2.imshow("Frame", frame)

    ok, frame = video.read()
    frames += 1

video.release()
# close all windows
cv2.destroyAllWindows()

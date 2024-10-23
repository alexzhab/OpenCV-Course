import cv2 as cv
import numpy as np

if __name__ == "__main__":
    video_filename = "video.mp4"
    video = cv.VideoCapture(video_filename)

    while True:

        ret, frame = video.read()

        frame = cv.resize(frame, (640, 480))
        image = cv.resize(image, (640, 480))

        u_green = np.array([104, 153, 70])
        l_green = np.array([30, 30, 0])

        mask = cv.inRange(frame, l_green, u_green)
        res = cv.bitwise_and(frame, frame, mask = mask)

        f = frame - res
        f = np.where(f == 0, image, f)

        cv.imshow("video", frame)
        cv.imshow("mask", f)

        if cv.waitKey(25) == 27:
            break 

    video.release()
    cv.destroyAllWindows()

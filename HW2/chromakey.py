import cv2 as cv
import numpy as np

class ChromaKey():
    def __init__(self, window_size, video_filename, background_filename):
        self.window_size = window_size
        self.window_name = "chromakey"
        self.video_filename = video_filename
        img = cv.imread(background_filename)
        self.background_img = cv.resize(img, self.window_size)
        self.frame = None

        self.color_chosen = False
        self.color = None

    def __update_mask(self):
        l1, u1 = (0, 50) if self.color[1] < 50 else (50, 255)
        l2, u2 = (0, 50) if self.color[2] < 50 else (50, 255)
        lower_color = np.array([255, l1, l2])
        upper_color = np.array([255, u1, u2])
        lower_color[0] = max(int(self.color[0]) - 20, 0)
        upper_color[0] = min(int(self.color[0]) + 20, 255)

        frame_hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(frame_hsv, lower_color, upper_color)
        masked_frame = np.copy(self.frame)
        masked_frame[mask != 0] = [0, 0, 0]

        background_copy = np.copy(self.background_img)
        background_copy[mask == 0] = [0, 0, 0]
        self.frame = background_copy + masked_frame
        cv.imshow(self.window_name, self.frame)

    def __mouse_event(self, event, x, y, flags, param):
        if not self.color_chosen:
            if event == cv.EVENT_LBUTTONDOWN:
                self.color_chosen = True
                frame_hsv = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)
                self.color = frame_hsv[y, x]

    def process(self):
        cv.namedWindow(self.window_name)
        cv.setMouseCallback(self.window_name, self.__mouse_event)

        video = cv.VideoCapture(self.video_filename)
        while video.isOpened():
            ret, self.frame = video.read()

            if ret:
                self.frame = cv.resize(self.frame, self.window_size)
                if not self.color_chosen:
                    cv.imshow(self.window_name, self.frame)
                else:
                    self.__update_mask()

                if cv.waitKey(25) == 27:
                    break
            else:
                break
        video.release()
        cv.destroyAllWindows()

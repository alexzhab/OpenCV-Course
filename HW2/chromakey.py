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
        rgb_index, color_max = np.argmax(self.color), np.max(self.color)
        lower_color = np.zeros(3)
        upper_color = np.zeros(3)
        for i, c in enumerate(self.color):
            if i != rgb_index:
                lower_color[i] = 0
                upper_color[i] = self.chromakey_rate
            else:
                lower_color[i] = max(color_max - self.color_dstrb, 0)
                upper_color[i] = min(color_max + self.color_dstrb, 255)

        mask = cv.inRange(self.frame, lower_color, upper_color)
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
                self.color = np.array(self.frame[y, x], dtype=int)

    def __trackbar_event(self, val):
        if self.color_chosen:
            self.chromakey_rate = val

    def process(self):
        cv.namedWindow(self.window_name)
        cv.setMouseCallback(self.window_name, self.__mouse_event)
        cv.createTrackbar("key_rate", self.window_name, 0, 255, self.__trackbar_event)

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

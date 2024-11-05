import cv2 as cv
import numpy as np

class GameScreen:
    RADIUS = 40
    DIAMETER = 2 * RADIUS

    GAME_NAME = "Game 4 IN A ROW"

    WHITE_COLOR = (255, 255, 255)
    BLACK_COLOR = (0, 0, 0)
    BLUE_COLOR = (255, 0, 0)
    RED_COLOR = (4, 45, 255)
    YELLOW_COLOR = (73, 236, 252)

    def __init__(self, height: int, width: int):
        self.__height = (height + 2) * self.DIAMETER
        self.__width = width * self.DIAMETER
        self.draw_screen()

    def draw_screen(self):
        self.__image = np.zeros((self.__height, self.__width, 3), np.uint8)
        self.draw_rectangle(0, 0, self.__width, self.__height, self.WHITE_COLOR)
        self.draw_rectangle(0, 2 * self.DIAMETER, self.__width, self.__height, self.BLUE_COLOR)

        self.__circles_x = [x for x in range(self.RADIUS, self.__width, self.DIAMETER)]
        self.__circles_y = [y for y in range(2 * self.DIAMETER + self.RADIUS, self.__height, self.DIAMETER)]
        for x in self.__circles_x:
            for y in self.__circles_y:
                self.draw_circle(x, y, self.WHITE_COLOR)

        self.__circles = [[(x, y) for y in self.__circles_y] for x in self.__circles_x]
        self.__map_circles_players = [[0 for y in self.__circles_y] for x in self.__circles_x]

    def draw_rectangle(self, start_x: int, start_y: int, end_x: int, end_y: int, color):
        cv.rectangle(self.__image, (start_x, start_y), (end_x, end_y), color, -1)

    def draw_circle(self, x: int, y: int, color):
        cv.circle(self.__image, (x, y), self.RADIUS, color, -1)

    def put_text(self, text: str, y_shift: int):
        cv.putText(self.__image, text, org=(int(self.__width/3.3), int(self.RADIUS * 3/2) + y_shift), 
                   fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=self.BLACK_COLOR, thickness=2)

    def find_closest_circle(self, mouse_x: int) -> tuple[int, int]:
        closest_circle, circle_x, circle_x_i = 1e4, 0, 0
        for ind, i in enumerate(self.__circles_x):
            if abs(i - mouse_x) < closest_circle:
                closest_circle = abs(i - mouse_x)
                circle_x_i = ind
                circle_x = i
        return circle_x_i, circle_x
    
    def find_empty_circle(self, circle_x: int, player_id: int):
        for i in range(len(self.__circles_x)):
            for j in range(len(self.__circles_y) - 1, -1, -1):
                if self.__circles[i][j][0] == circle_x:
                    if not self.__map_circles_players[i][j]:
                        self.__map_circles_players[i][j] = player_id
                        return self.__circles[i][j][1]
        return None
    
    def draw_circle_falling(self, circle_x_i: int, circle_y: int, color):
        for j in range(len(self.__circles_y)):
            x, y = self.__circles[circle_x_i][j][0], self.__circles[circle_x_i][j][1]
            if y < circle_y:
                self.draw_circle(x, y, color)
                cv.imshow(self.GAME_NAME, self.__image)
                cv.waitKey(20)
                self.draw_circle(x, y, self.WHITE_COLOR)
                cv.imshow(self.GAME_NAME, self.__image)
                cv.waitKey(20)

    def get_map_circles_players(self) -> list:
        return self.__map_circles_players
    
    def get_image(self):
        return self.__image
    
    def get_height(self) -> int:
        return self.__height
    
    def get_width(self) -> int:
        return self.__width

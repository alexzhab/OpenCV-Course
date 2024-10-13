from game_screen import GameScreen
import cv2 as cv

class GamePlay:
    def __init__(self, height: int, width: int):
        self.__num_circles_x = width
        self.__num_circles_y = height
        self.__player_id = 1
        self.__player_changed = True
        self.__game_over = False
        self.__screen = GameScreen(height, width)

    def change_player_id(self):
        self.__player_id = 3 - self.__player_id
        self.__player_changed = True

    def get_player_color(self):
        if self.__player_id == 1:
            return self.__screen.RED_COLOR
        else:
            return self.__screen.YELLOW_COLOR
    
    def check_win(self):
        circles_players_map = self.__screen.get_map_circles_players()
        self.__game_over = self.check_win_hor(circles_players_map) or self.check_win_ver(circles_players_map) or self.check_win_diag(circles_players_map)

    def check_win_ver(self, __map: list) -> bool:
        for i in range(self.__num_circles_x):
            for j in range(self.__num_circles_y - 3):
                if __map[i][j] == __map[i][j+1] == __map[i][j+2] == __map[i][j+3] == self.__player_id:
                    return True
        return False

    def check_win_hor(self, __map: list) -> bool:
        for i in range(self.__num_circles_x - 3):
            for j in range(self.__num_circles_y):
                if __map[i][j] == __map[i+1][j] == __map[i+2][j] == __map[i+3][j] == self.__player_id:
                    return True
        return False

    def check_win_diag(self, __map: list) -> bool:
        for i in range(self.__num_circles_x - 3):
            for j in range(self.__num_circles_y - 3):
                if __map[i][j] == __map[i+1][j+1] == __map[i+2][j+2] == __map[i+3][j+3] == self.__player_id:
                    return True
            
        for i in range(self.__num_circles_x - 1, 2, -1):
            for j in range(self.__num_circles_y - 3):
                if __map[i][j] == __map[i-1][j+1] == __map[i-2][j+2] == __map[i-3][j+3] == self.__player_id:
                    return True
        return False
    
    def mouse_event(self, event, x, y, flags, param):
        global ix
        if not self.__game_over:
            if event == cv.EVENT_MOUSEMOVE:
                self.__player_changed = False
                self.__screen.draw_rectangle(0, self.__screen.DIAMETER, 
                                             self.__screen.get_width(), 2 * self.__screen.DIAMETER, 
                                             self.__screen.WHITE_COLOR)
                self.__screen.draw_circle(x, self.__screen.DIAMETER + self.__screen.RADIUS, self.get_player_color())
                ix = x
            elif event == cv.EVENT_LBUTTONDOWN:
                circle_x_i, circle_x = self.__screen.find_closest_circle(ix)
                circle_y = self.__screen.find_empty_circle(circle_x, self.__player_id)
                if circle_y != None:
                    self.__screen.draw_rectangle(0, 0, self.__screen.get_width(), self.__screen.DIAMETER, self.__screen.WHITE_COLOR)
                    self.__screen.draw_circle_falling(circle_x_i, circle_y, self.get_player_color())
                    self.__screen.draw_circle(circle_x, circle_y, self.get_player_color())
                    self.check_win()
                    self.change_player_id()

    def play(self) -> int:
        cv.namedWindow(self.__screen.GAME_NAME)
        cv.setMouseCallback(self.__screen.GAME_NAME, self.mouse_event)
        while True:
            if self.__game_over:
                self.__screen.draw_rectangle(0, 0,
                                             self.__screen.get_width(), 2 * self.__screen.DIAMETER, 
                                             self.__screen.WHITE_COLOR)
                confetti_img = cv.imread("confetti.png")
                size = 60
                insert_pos = int(self.__screen.get_width()/3.3)
                image = self.__screen.get_image()
                image[15 : size + 15, insert_pos - size : insert_pos] = cv.resize(confetti_img, (size, size), interpolation= cv.INTER_LINEAR)
                self.__screen.put_text(f"Player {self.__player_id} wins!", 0)
                self.__screen.put_text("Press R to play again.", self.__screen.RADIUS)
                cv.imshow(self.__screen.GAME_NAME, self.__screen.get_image())
                return cv.waitKey(0)

            if self.__player_changed:
                self.__screen.draw_rectangle(0, 0,
                                             self.__screen.get_width(), 2 * self.__screen.DIAMETER,
                                             self.__screen.WHITE_COLOR)
                self.__screen.put_text(f"Player {self.__player_id} goes...", 0)
            
            cv.imshow(self.__screen.GAME_NAME, self.__screen.get_image())
            key = cv.waitKey(15)
            if key == 27:
                return key
            
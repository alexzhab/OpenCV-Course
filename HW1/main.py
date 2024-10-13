from game_play import GamePlay
import cv2 as cv

if __name__ == "__main__":
    while(True):
        game = GamePlay(6, 7)

        key = game.play()
        if key != 114:
            break
    cv.destroyAllWindows()

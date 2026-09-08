import sys
import pygame
from engine import MotorJuego


def main():

    pygame.init()
    pygame.mixer.init()

    motor = MotorJuego()
    motor.ejecutar()

    pygame.mixer.quit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

    

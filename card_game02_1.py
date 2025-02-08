import pygame


class card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.width = 60
        self.height = 90
        self.face_up = True
        self.x = 0
        self.y = 0
        self.dragging = False
        self.drag_offset = (0, 0)



class TWGame:


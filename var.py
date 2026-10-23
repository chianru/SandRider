import json

FPS = 60
CELL_SIZE = 30
CELL_NUM = 25

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (173, 204, 96)
BLUE = (0, 0, 255)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
PINK = (251, 198, 207)
CYAN = (0, 255, 255)


with open('items_data.json', 'r') as file:
    items_data = json.load(file)
import random

class Pipe:
    def __init__(self, x, screen_width, screen_height):
        try:
            self.width = 80
            self.gap = 160
            self.x = x
            self.y = random.randint(200, 400)
            self.speed = 5
            self.passed = False
            self.screen_height = screen_height
            
            if screen_width <= 0 or screen_height <= 0:
                raise ValueError("Invalid screen dimensions")
        except Exception as e:
            print(f"Pipe initialization error: {str(e)}")
            raise

    def update(self):
        try:
            self.x -= self.speed
        except AttributeError as e:
            print(f"Pipe update error: {str(e)}")

    def offscreen(self):
        try:
            return self.x < -self.width
        except AttributeError as e:
            print(f"Offscreen check failed: {str(e)}")
            return True
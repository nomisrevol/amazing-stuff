STEP = 10
WINDOW_SIZE = 500


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
    
    def change_direction_to(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, food_position):
        if self.direction == "RIGHT":
            self.position[0] += STEP
        if self.direction == "LEFT":
            self.position[0] -= STEP
        if self.direction == "UP":
            self.position[1] -= STEP
        if self.direction == "DOWN":
            self.position[1] += STEP
        self.body.insert(0, list(self.position));
        if self.position == food_position:
            return True
        self.body.pop()
        return False
    
    def check_collision(self):
        if self.position[0] > WINDOW_SIZE - STEP or self.position[0] < 0:
            print (str(self.position[0]) + " " + str(self.position[1]))
            return True
        if self.position[1] > WINDOW_SIZE - STEP or self.position[1] < 0:
            return True
        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return True
        return False

    def get_head_position(self):
        return self.position
    
    def get_body(self):
        return self.body






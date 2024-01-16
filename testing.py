import turtle
import random

class ColorGuessGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.drawer = turtle.Turtle()
        self.drawer.penup()
        self.drawer.speed(0)
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        self.positions = [(-330, -280), (-290, -280), (-250, -280), (-210, -280), (-170, -280), (-130, -280)]
        self.choice_tracker_positions = [(-300, 280), (-260, 280), (-220, 280), (-180, 280)]  # New positions for tracking
        self.indicator_positions = [(-110, 290), (-100, 290), (-115, 275), (-100, 275)]  # Position
        self.user_choices = []
        self.pattern = self.get_random_num()
        self.selected = [False] * len(self.colors)
        self.max_guesses = 10
        self.current_guess = 0
        self.guess_results = []
        self.original_indicator_positions = [(-100, 290), (-115, 290), (-100, 270), (-115, 270)]  # Original positions  # Keep original positions
        self.original_choice_tracker_positions = [(x, y) for x, y in self.choice_tracker_positions]  # Keep original positions  # Keep original positions
        self.setup_game()

    def get_random_num(self):
        return random.sample(self.colors, 4)

    def draw_circle(self, color, position):
        self.drawer.color(color)
        self.drawer.goto(position)
        self.drawer.dot(35)

    def draw_choice_tracker(self):
        for pos in self.choice_tracker_positions:
            self.drawer.color('gray')  # Neutral/empty color
            self.drawer.goto(pos)
            self.drawer.dot(35)

    def update_choice_tracker(self):
        for i, color in enumerate(self.user_choices):
            if i < len(self.choice_tracker_positions):  # Check to avoid index out of range
                pos = self.choice_tracker_positions[i]
                self.drawer.color(color)
                self.drawer.goto(pos)
                self.drawer.dot(35)

    def outline_circle(self, index):
        self.drawer.color(self.colors[index])
        pos = self.positions[index]
        self.drawer.goto(pos)
        self.drawer.dot(35, 'black')  # larger dot to cover the original
        self.drawer.dot(32, 'white')  # outline

    def update_indicators(self):
        # Clear the indicators from the previous guess
        for pos in self.indicator_positions:
            self.drawer.penup()
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.color('white')  # Assuming the background is white
            self.drawer.dot(10)  # Cover the old indicator with a white dot
            self.drawer.color('white')
            self.drawer.dot(9)

        # Logic to update the indicators based on the current guess
        pattern_copy = self.pattern[:]  # Make a copy of the pattern to mark off found colors
        indicators = ['white'] * 4  # Start with all indicators as white
        print(indicators)
        # First pass for correct positions
        for i, choice in enumerate(self.user_choices):
            if choice == pattern_copy[i]:
                indicators[i] = 'black'
                print(indicators)
                #pattern_copy[i] = None  # This color is correctly guessed, remove it from consideration

        # Second pass for correct colors in incorrect positions
        for i, choice in enumerate(self.user_choices):
            if choice in pattern_copy:  # Avoid counting correct positions twice
                indicators[i] = 'red'
                print(indicators)
                #pattern_copy[pattern_copy.index(choice)] = None  # Remove this color so it's not counted again

        # Draw the indicators
        for i, indicator_color in enumerate(indicators):
            pos = self.indicator_positions[i]
            self.drawer.penup()
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.color(indicator_color)
            self.drawer.dot(8)
            print(indicators)

        # Move the indicator positions down for the next guess
        if self.current_guess < self.max_guesses:
            for i in range(4):
                x, y = self.indicator_positions[i]
                self.indicator_positions[i] = (x, y - 40)
                print(indicators)

    def check_choice(self, x, y):
        if self.current_guess < self.max_guesses and len(self.user_choices) < 4:
            for i, pos in enumerate(self.positions):
                if pos[0] - 25 < x < pos[0] + 25 and pos[1] - 25 < y < pos[1] + 25:
                    if not self.selected[i]:
                        self.user_choices.append(self.colors[i])
                        self.selected[i] = True
                    
                        self.outline_circle(i)
                        self.update_choice_tracker()
                    break  # Stop the loop once a circle is found
            if len(self.user_choices) == 4:
                self.update_indicators()
                self.current_guess += 1
                if self.current_guess == self.max_guesses or self.user_choices == self.pattern:
                    self.end_game()
                else:
                    self.reset_for_next_guess()

    def reset_for_next_guess(self):
        # Move the choice tracker positions down by 50 units on the y-axis for the next guess
        self.choice_tracker_positions = [(x, y - 50 * self.current_guess) for x, y in self.original_choice_tracker_positions]

        # Redraw the original colored circles for the next guess
        self.drawer.penup()  # Lift the pen to avoid drawing lines
        for color, pos in zip(self.colors, self.positions):
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.dot(35, color)
            self.drawer.penup()  # Lift the pen after drawing

        # Redraw the choice tracker for the next guess
        for pos in self.choice_tracker_positions:
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.dot(35, 'gray')
            self.drawer.penup()  # Lift the pen after drawing

        # Reset for the next guess
        self.user_choices = []
        self.selected = [False] * len(self.colors)

    def end_game(self):
        # Handle the end of the game
        if self.user_choices == self.pattern:
            print("Correct! The pattern was:", ', '.join(self.pattern))
        else:
            print("Game Over. The correct pattern was:", ', '.join(self.pattern))
        self.screen.onclick(None)  # Disable further clicks

    '''def compare_choices(self):
        if self.user_choices == self.pattern:
            print("Correct!")
        else:
            print("Incorrect. The correct pattern was:", ', '.join(self.pattern))
        print("Your choices were:", ', '.join(self.user_choices))'''
        

    def setup_game(self):
        for color, pos in zip(self.colors, self.positions):
            self.draw_circle(color, pos)
        self.draw_choice_tracker()  # Draw the choice tracking circles
        self.screen.onclick(self.check_choice)

    def start_game(self):
        self.screen.mainloop()

# Create and start the game
game = ColorGuessGame()
game.start_game()



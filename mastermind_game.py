'''
Agesandro Almondes
CS 5001 Fall 2023
Final Project
'''

import turtle
import random
from GameBoard import GameBoard

class ColorGuessGame(GameBoard):
    '''
    Class is the entire backbone of the MasterMind aka ColorGuessGame
    contains all logic shape registration, check, and click event
    actions. 
    '''
    def __init__(self):
        self.screen = turtle.Screen()
        self.drawer = turtle.Turtle()
        self.drawer.penup()
        self.drawer.speed(0)
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        self.positions = [(-300, -280), (-250, -280), (-200, -280), (-150, -280), (-100, -280), (-50, -280)]
        self.choice_tracker_positions = [(-260, 280), (-220, 280), (-180, 280), (-140, 280)] 
        self.indicator_positions = [(-80, 285), (-70, 285), (-80, 270), (-70, 270)] 
        self.new_choice_tracker_pos = []
        self.original_choice_tracker_positions = self.choice_tracker_positions[:]  
        self.user_choices = []
        self.max_guesses = 10
        self.current_guess = 0
        self.pattern = self.get_random_color()
        self.selected = [False] * len(self.colors)
        self.screen.register_shape("checkbutton.gif")
        self.screen.register_shape("xbutton.gif")
        self.screen.register_shape("quit.gif")
        self.screen.register_shape("quitmsg.gif")
        self.screen.register_shape("winner.gif")
        self.screen.register_shape("Lose.gif")
        self.screen.register_shape("leaderboard_error.gif")
        self.screen.register_shape("file_error.gif")
        self.username = self.get_user_name()
        self.setup_game()

    def get_random_color(self):
        '''
        get_random_num -- get's a random color by using the built in 
        python sample function and the random class that we are 
        allowed to import. Creates a list of 4 colors to be 
        designated pattern
        '''
        return random.sample(self.colors, 4)

    def place_gif_button(self, image, position):
        '''
        Function is responsible for place the correlating gif images 
        to the correct location when called upon. 
        '''
        button = turtle.Turtle()
        button.penup()
        button.shape(image)
        button.goto(position)
        return button

    def on_quit_button(self, x, y):
        '''
        Handles what happens in the even of the quit button being clicked, 
        which in this case prompt the quit msg. While also disabling any 
        furthermore clicks. X, Y aren't used right way however are called 
        when placing gif is needed. 
        '''
        x = None
        y = None
        self.screen.onclick(None)
        self.quit_button = self.place_gif_button("quitmsg.gif", (0, 0))

    def on_confirm_button_click(self, x, y):
        '''
        Handles what happens in the even of the confirm button (check button)
        being clicked, which in this case prompt the quit msg. While also 
        disabling any furthermore clicks. X, Y aren't used right way 
        however are called when placing gif is needed. 
        '''
        x = None
        Y = None
        if len(self.user_choices) == 4:
            self.update_indicators()
            self.current_guess += 1
            if self.current_guess == self.max_guesses or self.user_choices == self.pattern:
                self.end_game()
            else:
                self.reset_for_next_guess()

    def on_remove_button_click(self, x, y):
        '''
        Handles what happens in the even of the remove button( X button)
        being clicked, which in this case prompt the quit msg. While 
        also disabling any furthermore clicks. X, Y aren't used right 
        way however are called when placing gif is needed. 
        '''
        x = None
        y = None
        if self.user_choices:
            removed_choice = self.user_choices.pop()
            removed_index = self.colors.index(removed_choice)
            self.selected[removed_index] = False
            self.redraw_choice_circle(removed_index)
            self.update_choice_tracker()

    def redraw_choice_circle(self, index):
        '''
        Redraws the which ever circle was previous colored, and 
        returns it to the oringinal color. This is the basis for
        reset_choices later
        '''
        color = self.colors[index]
        pos = self.positions[index]
        self.drawer.goto(pos)
        self.drawer.dot(35, color)

    def draw_circle(self, color, position):
        '''
        Draws all circles in for game, takes in color of said circle
        and position. 
        '''
        self.drawer.color(color)
        self.drawer.goto(position)
        self.drawer.dot(35)

    def draw_choice_tracker(self):
        '''
        Draws all choie circles which are initially blank.
        '''
        for pos in self.choice_tracker_positions:
            self.drawer.color('gray')
            self.drawer.goto(pos)
            self.drawer.dot(34)

    def update_choice_tracker(self):
        '''
        Draws all choice circles (in this case 4) which represent which 
        colors the user has selected.
        '''
        for i, pos in enumerate(self.choice_tracker_positions):
            if i < len(self.user_choices):
                color = self.user_choices[i]
            else:
                color = 'gray' 
            self.drawer.goto(pos)
            self.drawer.dot(35, color)

    def outline_circle(self, index):
        '''
        Draws an outline of the circle, called upon later to setup\
        icons
        '''
        self.drawer.color(self.colors[index])
        pos = self.positions[index]
        self.drawer.goto(pos)
        self.drawer.dot(35, 'black') 
        self.drawer.dot(33, 'white')

    def update_indicators(self):
        '''
        Draws all choie circles indicators, which correspond to different
        meaning's relating to position. If color is in the correct position, 
        indictors will be drawn black, if the color is in the incorrect position
        and the is in the pattern. Circle will be colored in red, else will be left 
        blank
        '''
        pattern_copy = self.pattern[:]
        self.drawer.fillcolor('white') 
        self.drawer.pencolor('black')

        for i, choice in enumerate(self.user_choices):
            pos = self.indicator_positions[i]
            self.drawer.penup()
            self.drawer.goto(pos)
            self.drawer.pendown()

            if choice == pattern_copy[i]:
                self.drawer.fillcolor('black')
                self.drawer.begin_fill()
                self.drawer.circle(4)
                self.drawer.end_fill()
            elif choice != pattern_copy[i] and choice in pattern_copy:
                self.drawer.fillcolor('red')
                self.drawer.begin_fill()
                self.drawer.circle(4)
                self.drawer.end_fill()
            else:
                self.drawer.color('black')
                self.drawer.circle(4)
        if self.current_guess < self.max_guesses:
            for i in range(4):
                x, y = self.indicator_positions[i]
                self.indicator_positions[i] = (x, y - 50)
                
    def check_choice(self, x, y):
        '''
        Checks to see if current guess is equal to the pattern 
        if not, the count of guess goes up by one. This keeps count
        of the number of guess so the user never gets more than 10 
        tries. Once user hit's 10 the game ends(break). X and Y are 
        used the cordinates of a user click. Conditional checks to see 
        it's in circle(width of the circle) if so color is selceted and appened
        '''
        if self.current_guess < self.max_guesses and len(self.user_choices) < 4:
            for i, (pos_x, pos_y) in enumerate(self.positions):
                if pos_x - 25 < x < pos_x + 25 and pos_y - 25 < y < pos_y + 25:
                    if not self.selected[i]:
                        self.user_choices.append(self.colors[i])
                        self.selected[i] = True
                        self.outline_circle(i)
                        self.update_choice_tracker()
                        break

    def reset_for_next_guess(self):
        '''
        Resets the color and postions of the next row to be drawn 
        While moving the y axis down 50 units to make sure that 
        the indicators line up with row
        '''
        self.choice_tracker_positions = [(x, y - 50 * self.current_guess) 
                                         for x, y in self.original_choice_tracker_positions]
        self.drawer.penup()
        for color, pos in zip(self.colors, self.positions):
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.dot(35, color)
            self.drawer.penup()
        
        for pos in self.choice_tracker_positions:
            self.drawer.goto(pos)
            self.drawer.pendown()
            self.drawer.dot(35, 'gray')
            self.drawer.penup()
        
        self.user_choices = []
        self.selected = [False] * len(self.colors)
        
    def end_game(self):
        '''
        Handle the end game and presents specific images 
        depending on if the user won or lost the game
        '''
        if self.user_choices == self.pattern:
            self.place_gif_button("winner.gif", (0,0))
            print("Correct! The pattern was:", ', '.join(self.pattern))
            self.update_leaderboard(self.username, self.current_guess)
        else:
            self.place_gif_button("Lose.gif", (0,0))
            print("Game Over. The correct pattern was:", ', '.join(self.pattern))
        self.screen.onclick(None)

    def update_leaderboard(self, username, score):
        '''
        Function updates the leaderbaord .txt file and i writes 
        the users user_name and their corresponding socre, uses 'a for
        both appending and reading file
        '''
        with open("leaderboard.txt", "a") as file:
            file.write(f"{username}: {score}\n")

    def read_leaderboard(self):
        '''
        Reads the information on the leaderbaord .txt, in this 
        case this the user_name and corresponding score of said 
        user. Aware that in this, file is only being read and not
        modified. If failed returns a leaderboard error message.
        '''
        try:
            with open("leaderboard.txt", "r") as file:
                leaderboard_data = file.readlines()
            return leaderboard_data
        except FileNotFoundError:
            error_msg = self.place_gif_button("leaderboard_error.gif", 0,0)
            self.drawer.hide(error_msg)
    
    def get_score(data):
        '''
        Grabs the scores from the .txt file and seperates them by collen'''
        score = data.split(': ')[1]
        return int(score)

    def sort_leaderboard(self):
        '''
        Sortes the leaderboard by score, so when the information is 
        retrived it can be displayed properly
        '''
        leaderbaord_data = self.read_leaderboard()
        sorted_scores = sorted(leaderbaord_data)
        return sorted_scores
    
    def display_leaderboard(self):
        '''
        Writes the Heading and the information for scores, for
        user to see the current leaderbaord socres. 
        '''
        self.drawer.pencolor('blue')
        self.drawer.goto(225, 290)
        title = "Leaderboard:"
        self.drawer.write(title, align="center", font=("Arial", 14, "normal", "bold"))
        leaderboard_data = self.sort_leaderboard()
        start_pos = (190, 245)  
        for i, entry in enumerate(leaderboard_data):
            self.drawer.goto(start_pos[0], start_pos[1] - (20 * i))
            self.drawer.pencolor("blue")
            self.drawer.write(entry, font=("Arial", 14, "normal"))

    def setup_game(self):
        '''
        Handles the whole setup of the game, this includes calling all 
        the main function to make the game work. First by drawing circles, 
        displaying leaderboards, choice tracker etc. This saves the main from having
        to include copious lines of code
        '''
        for color, pos in zip(self.colors, self.positions):
            self.draw_circle(color, pos)
            self.drawer.hideturtle()
        self.draw_choice_tracker()
        self.display_leaderboard()
        self.drawer.hideturtle()
        self.screen.register_shape("checkbutton.gif")
        self.screen.register_shape("xbutton.gif")
    
        self.confirm_button = self.place_gif_button("checkbutton.gif", (30, -275))
        self.remove_button = self.place_gif_button("xbutton.gif", (120, -275))
        self.quit_button = self.place_gif_button("quit.gif", (250, -275))
   
        self.screen.onclick(self.check_choice)
        self.confirm_button.onclick(self.on_confirm_button_click)
        self.remove_button.onclick(self.on_remove_button_click)
        self.quit_button.onclick(self.on_quit_button)
        self.screen.onclick(self.check_choice)

    def start_game(self):
        '''
        Essientially this is the Turtle.Mainloop() that is used to 
        keep the screen open till done.
        '''
        self.screen.mainloop()

def main():

    draw_game = GameBoard()
    game = ColorGuessGame()
    game.start_game()

if __name__ == "__main__":
    main()

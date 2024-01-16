'''Agesandro Almondes 
CS 5001 Fall 2023
Final Project Mastermind Game, Board Helper function
'''

import turtle
from Point import Point
from Marble import Marble

class GameBoard:
    '''
    Class draws the boarders of the all the chocies to cleanly
    setup and keep organized. Sets up the screen with proper screen 
    title, while drawing the background marbles'''
    def __init__(self):
        self.turtle = turtle 
        self.turtle.speed(0)
        self.screen = turtle.Screen()
        self.indicator_positions = [(-80, 288), (-70, 288), (-80, 273), (-70, 273)]
        self.setup_screen()
        self.draw_game_board()
        self.setup_marbles()
        self.draw_marbles()
        self.draw_indicators()
        self.marbles = []

    def get_user_name(self):
        '''
        Method used to get the users user_name is called in Mastermind.py
        '''
        user_name = self.screen.textinput("CS 5001 Mastermind", "Your name")
        return(user_name)

    def setup_screen(self):
        '''
        Setups, the screen dimensions with header on the window stating the game
        title
        '''
        self.screen.title("CS 5001 Mastermind")
        self.screen.setup(700, 700)
    
    def setup_marbles(self):
        '''
        Draw the background for the marlbles to illistate to the user
        how many guess they have.
        '''
        self.default_marble = Marble(Point(-260, 268), "white")

    def draw_marbles(self):
        '''
        draws the empty blank marbles for the positioning
        '''
        self.default_marble.draw_empty_deafulf()

    def draw_indicators(self):
        '''
        Draws the indicator's blank for the board to be 
        complete with each set of 4 indicators corresponding 
        to each row.
        '''
        row_offset = 50  
        num_rows = 10    
        for row in range(num_rows):
            for pos in self.indicator_positions:
                adjusted_pos = (pos[0], pos[1] - row * row_offset)
                self.turtle.penup()
                self.turtle.goto(adjusted_pos)
                self.turtle.pendown()
                self.turtle.color('black')
                self.turtle.dot(8)
                self.turtle.color('white')
                self.turtle.dot(7)

    def draw_rectangle(self, start_pos, color, width, length, height):
        '''
        Logic that is used to draw the rectangles that encapsoulate the 
        different choices, indicators, and leaderboard. This is simpily a shortcut 
        to not having to draw right angles over and over.
        '''
        self.turtle.penup()
        self.turtle.setposition(start_pos)
        self.turtle.pendown()
        self.turtle.pencolor(color)
        self.turtle.width(width)
        for _ in range(2):
            self.turtle.forward(length)
            self.turtle.right(90)
            self.turtle.forward(height)
            self.turtle.right(90)

    def draw_game_board(self):
        '''
        Method is used to draw the actually boarders of the boxes which 
        each contain an aspect of the game. Uses the logic from 
        draw_rectangle
        '''
        self.draw_rectangle((170, 335), 'blue', 7, 150, 550)
        self.draw_rectangle((-330, 335), 'black', 7, 480, 550)
        self.draw_rectangle((-330, -230), 'black', 7, 650, 100)
        self.turtle.hideturtle()
import copy
import sys
import pygame
import numpy as np
import random

from constants import *

#pygame setup

pygame.init()
screen = pygame.display.set_mode( (width,height) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLORS)

title_font = pygame.font.SysFont('chiller',60) #imprintshadow  acaslonprobold
text_font = pygame.font.SysFont('Sans', 20)

def draw_text(text,font,text_col,x,y):
    img = font.render(text, True,text_col)
    screen.blit(img, (x, y))

class Board:

    def __init__(self):
        self.squares = np.zeros((rows,cols))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0
    
    def final_state(self, show = False):
        '''
            return 0 if there is no win
            return 1 if player 1 wins
            return 2 if player 2 wins
        '''
        #virtical
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0 :
                if show:
                    ipos= (col * SQSIZE + SQSIZE // 2, SQSIZE + 20)
                    fpos= (col * SQSIZE + SQSIZE // 2, height - 20)
                    pygame.draw.line(screen, (20, 14, 120), ipos, fpos, LINE_WIDTH + 15)
                return self.squares[0][col]
        
        #horizontal
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0 :
                if show:
                    ipos= (20, row * SQSIZE + SQSIZE // 2 + SQSIZE)
                    fpos= (width-20, row * SQSIZE + SQSIZE // 2 + SQSIZE)
                    pygame.draw.line(screen, (20, 14, 120), ipos, fpos, LINE_WIDTH + 15)
                return self.squares[row][0]

        #descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0 :
            if show:
                ipos= (40, SQSIZE + 40)
                fpos= (width-40, height-40)
                pygame.draw.line(screen, (20, 14, 120), ipos, fpos, LINE_WIDTH + 15)
            return self.squares[0][0]
   
        #ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] !=0 :
            if show:
                ipos= (40, height- 40)
                fpos= (width-40, SQSIZE + 40)
                pygame.draw.line(screen, (20, 14, 120), ipos, fpos, LINE_WIDTH + 15)
            return self.squares[1][1]

        # no win yet 
        return 0

    def mark_sqr(self,row,col,playe):
        self.squares[row][col] = playe
        self.marked_sqrs += 1

    def empty_sqr (self, row , col):     #is a specific position[row][col] empty
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):            # recieve a list containing the positions of empty squares
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level = 1, player = 2 ) :
        self.level = level
        self.player = player
    
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))
        return empty_sqrs[idx] # row,col

    def minimax(self, board, maximizing):
    # terminal cases 
        case = board.final_state()
        # player 1 wins
        if case == 1 :
            return 1, None
        # palyer 2 wins
        if case == 2:
            return -1, None
        # draw
        elif board.isfull() :
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_srqs = board.get_empty_sqrs()
            # i = 0
            for (row,col) in empty_srqs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                # i+=1
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
                    # print(f"this is the current eval : {eval} and this is the current best move {best_move} in max, step {i}")
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_srqs = board.get_empty_sqrs()
            # i = 0
            for (row,col) in empty_srqs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                # i+=1
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
                    # print(f"this is the current eval : {eval} and this is the current best move {best_move} in not max, step {i}")
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0 :
            # random choice
            eval = 'random'
            move = self.rnd(main_board)

        else :
            # minimax algo choice
            eval, move = self.minimax(main_board, False)
        
        print(f'AI has chosen to mark the square is pos {move} with an eval of : {eval}')
        return eval, move # row , col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai =AI()
        self.player = 1 # 1 : X      2 : O
        self.gamemode = 'pvp'  # pvp or ai
        self.running = True
        pygame.draw.rect(screen,whitee, pygame.Rect(10, 200, 580 , 590),580,50)
        self.show_lines()
    
    def over(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def show_lines(self):
        #vertical
        pygame.draw.line(screen, LINE_COLOR , (SQSIZE,SQSIZE),(SQSIZE,height-10),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR , (width-SQSIZE,SQSIZE),(width-SQSIZE,height-10),LINE_WIDTH)
        #horizontal
        pygame.draw.line(screen, LINE_COLOR , (10,SQSIZE*2),(width-10,SQSIZE*2),LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR , (10,SQSIZE*3),(width-10,SQSIZE*3),LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self,row,col):
        if self.player == 1 :
            start_desc = (col * SQSIZE + 50, row * SQSIZE + 50)
            end_desc = (col * SQSIZE + SQSIZE - 50,row * SQSIZE + SQSIZE -50)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQSIZE + 50, row * SQSIZE + SQSIZE - 50)
            end_asc = (col * SQSIZE + SQSIZE - 50,row * SQSIZE + 50)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            


        elif self.player == 2 :
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE //2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def change_gamemode(self):
        if self.gamemode=='ai' : 
            self.reset(pv=True)
        else : 
            self.reset()
            self.gamemode = 'ai'
        print(f'game mode changed to {self.gamemode}')
    
    def change_gamemode_to_ai(self):
        self.reset()
        self.gamemode = 'ai'
    
    def reset(self, pv= False):
        ch = False
        d = False
        if self.ai.level == 0 :
            d = True
        if self.gamemode == 'ai':
            ch = True
        self.__init__()
        if pv:
            d=False
            ch=False
        print('game reseted')
        if ch:
            self.gamemode = 'ai'
        if d :
            self.ai.level = 0
        print(self.gamemode)
            

def main():

    #object
    game = Game()
    board = game.board
    ai = game.ai

    #main loop
    while True:
        draw_text("TIC", title_font, (245,77,98), 165, 20)
        draw_text("TAC", title_font, (20, 14, 120), 255, 20)
        draw_text("TOE", title_font, (94, 160, 40), 345, 20)
        draw_text("Change the gamemode and the difficulty of the AI by pressing these buttons :", text_font, (20, 14, 120), 10, 100)
        draw_text("r : restart the game       g : change the game mode", text_font, (20, 14, 120), 10, 130)
        draw_text("d : easy level                s : hard level (Impossible)", text_font, (20, 14, 120), 10, 160)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit

            if event.type == pygame.KEYDOWN:
                # g : for changing the game mode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                    board = game.board
                    ai = game.ai

                # d : ai level is 0 (random)
                if event.key == pygame.K_d:
                    game.change_gamemode_to_ai()
                    board = game.board
                    ai = game.ai
                    ai.level = 0
                    print("ai level changed to 0 ( ai is dump)")

                # s : ai level is 1 (undefeated)
                if event.key == pygame.K_s:
                    game.change_gamemode_to_ai()
                    board = game.board
                    ai = game.ai
                    ai.level = 1
                    print("ai level changed to 1 ( ai is smart)")

                # r : to restart the game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            if event.type == pygame.MOUSEBUTTONDOWN:
                row = event.pos[1] // SQSIZE
                col = event.pos[0] // SQSIZE
            #    print(row,col)
                if row > 0 :
                    if board.empty_sqr(row-1,col) and game.running:
                        board.mark_sqr(row-1,col, game.player)
                        # print(row-1,col)
                        game.draw_fig(row,col)
                        game.next_turn()
                        print(board.squares)
                        if game.over() : 
                            game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            # ai methodes :
            ev , pos = ai.eval(board)
            board.mark_sqr(pos[0],pos[1],2)
            game.draw_fig(pos[0]+1,pos[1])
            game.next_turn()
            print(board.squares)
            if game.over() : 
                game.running = False
            
            
        pygame.display.update() # update the screen


main()
import pygame
from piece import Piece 
from board import Board 
import os
from solver import Solver
from time import sleep

class Game:
    def __init__(self, size, prob):
        self.board = Board(size, prob)
        pygame.init()
        self.sizeScreen = 800, 800
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0]) 
        self.loadPictures()
        self.solver = Solver(self.board)

    def loadPictures(self):
        self.images = {}
        images_directory = "images"
        for file_name in os.listdir(images_directory):
            if not file_name.endswith(".png"):
                continue
            path = os.path.join(images_directory, file_name)
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (int(self.pieceSize[0]), int(self.pieceSize[1])))
            self.images[file_name.split(".")[0]] = img
        
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (self.board.getWon() or self.board.getLost()):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                if event.type == pygame.KEYDOWN:
                    self.solver.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                self.win()
                running = False
        pygame.quit()
        
    def draw(self):
        top_left = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(top_left, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, top_left)
                top_left = (top_left[0] + self.pieceSize[0], top_left[1])
            top_left = (0, top_left[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            return str(piece.getNumAround()) if not piece.getHasBomb() else 'bomb-at-clicked-block'
        if (self.board.getLost()):
            if (piece.getHasBomb()):
                return 'unclicked-bomb'
            return 'wrong-flag' if piece.getFlagged() else 'empty-block'
        return 'flag' if piece.getFlagged() else 'empty-block'

    def handleClick(self, position, flag):
        index = tuple(int(pos // size) for pos, size in zip(position, self.pieceSize))[::-1] 
        self.board.handleClick(self.board.getPiece(index), flag)

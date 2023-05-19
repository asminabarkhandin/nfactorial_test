import sys
from game import Game

def main():
    #the user needs to define the size of the grid and the probability
    size = int(sys.argv[1]), int(sys.argv[2])
    prob = float(sys.argv[3])
    g = Game(size, prob)
    g.run()

if __name__ == '__main__':
    main()
all:
     g++ -O3 -o game.o Game.cpp
     python3 solver.py
     ./game.o < best_strategy.txt
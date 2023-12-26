import numpy as np
import GUI
ROW_COUNT = 6
COLUMN_COUNT = 7

def CreateBoard():
    Board = np.zeros((6,7))
    return Board

def DropPiece(Board, Row, Column, Piece):
    Board[Row][Column] = Piece


def IsValidMove(Board,Column):
    return Board[5][Column]==0


def GetNextOpenRow(Board,Column):
    for r in range(ROW_COUNT):
        if Board[r][Column] == 0:
            return r

def PrintBoard(Board):
    print("*----------------------*")
    print(np.flip(Board, 0))
    print("*----------------------*")


Board = CreateBoard()

GameOver = False
Turn = 0

while not GameOver:
    if Turn == 0:
        Column = int(input("Player 1 make your selection from (0-6):"))
        if IsValidMove(Board,Column):
            Row = GetNextOpenRow(Board,Column)
            DropPiece(Board, Row, Column, 1)


    else:
        Column = int(input("Player 2 make your selection from (0-6):"))
        if IsValidMove(Board,Column):
            Row = GetNextOpenRow(Board,Column)
            DropPiece(Board, Row, Column, 2)

    row_array = [int(i) for i in list(Board[1, :])]
    print(row_array)
    PrintBoard(Board)
    Turn +=1
    Turn %=2

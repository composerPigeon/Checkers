# Checkers
Small checkers game for two players with graphics theme of angels and devils. Project was implemented using pygame framework.

## Installation
1) after downloading this repository, install dependencies from `requirements.txt` file
    - this will install the pygame framework
2) in your command line now run `python3 main.py`, which will launch the application
3) Window with new game will appear on screen

## User Manual
- when you click pawn or queen it will become selected and it will turn purple with tiles where it's possible to move next with the selected pawn 
- when player is not on turn, his pawns can not be selected

## Rules
- white (in this game angels) plays first
- when you are able to jump, you have to take it
- pawns can move just one tile diagonally to the front
- queens can move just one tile, but in all four diagonal directions
- pawn will become the queen, when you get it to the opponent's side of board
- player wins when he get rid of all opponent's pawns in the game
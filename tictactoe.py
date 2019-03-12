'''
Cindy Kim
CS-UY1114
Final Project: Tic-Tac-Toe
Section EXL1
'''
import turtle
import time
import random

# This list represents the board. It's a list
# of nine strings, each of which is either
# "X", "O", "_", representing, respectively,
# a position occupied by an X, by an O, and
# an unoccupied position. The first three
# elements in the list represent the first row,
# and so on. Initially, all positions are
# unoccupied.
the_board = [ "_", "_", "_",
              "_", "_", "_",
              "_", "_", "_"]

def draw_board(board):
    """
    signature: list(str) -> NoneType
    Given the current state of the game, draws
    the board on the screen, including the
    lines and the X and O pieces at the position
    indicated by the parameter.
    Hint: Write this function first!
    """
    turtle.clear()

    #Draws the horizontal lines of grid
    for horizontal in range (-1, 2, 2):
        turtle.up()
        turtle.setpos(-360, (-120 * horizontal))
        turtle.setheading(0)
        turtle.down()
        turtle.forward(720)
        
    #Draws the vertical lines of grid
    for vertical in range (-1, 2, 2):
        turtle.up()
        turtle.setpos((-120 * vertical), 360)
        turtle.setheading(270)
        turtle.down()
        turtle.forward(720)

    #Grid Info: 240 by 240 for each square, 720 by 720 for entire grid

    for i in range (0, len(board)):
        if (board[i] != "_"):
            turtle.up()
            #Sets position of turtle to the center of the specified square
            if (i <= 2):
                turtle.setpos((240 * i) - 240, 240)
            elif (i <= 5):
                turtle.setpos((240 * (i - 3)) - 240, 0)
            else:
                turtle.setpos((240 * (i - 6)) - 240, -240)

            #Draws an "X"
            if (board[i] == "X"):
                turtle.down()
                turtle.color("red")
                turtle.pensize(5)
                turtle.setheading(0)
                turtle.left(45)
                turtle.forward(106.066)
                turtle.up()
                turtle.left(135)
                turtle.forward(150)
                turtle.left(135)
                turtle.down()
                turtle.forward(212.132)
                turtle.right(135)
                turtle.up()
                turtle.forward(150)
                turtle.right(135)
                turtle.down()
                turtle.forward(106.066)
                turtle.color("black")
                turtle.pensize(1)
            #Draws an "O"
            elif (board[i] == "O"):
                turtle.color("blue")
                turtle.pensize(5)
                turtle.setheading(270)
                turtle.forward(75)
                turtle.left(90)
                turtle.down()
                turtle.circle(75)
                turtle.color("black")
                turtle.pensize(1)
    turtle.update()

def do_user_move(board, x, y):
    """
    signature: list(str), int, int -> bool
    Given a list representing the state of the board
    and an x,y screen coordinate pair indicating where
    the user clicked, update the board
    with an O in the corresponding position. Your
    code will need to translate the screen coordinate
    (a pixel position where the user clicked) into the
    corresponding board position (a value between 0 and
    8 inclusive, identifying one of the 9 board positions).
    The function returns a bool indicated if
    the operation was successful: if the user
    clicks on a position that is already occupied
    or outside of the board area, the move is
    invalid, and the function should return False,
    otherwise True.
    """
    print("user clicked at "+str(x)+","+str(y))
    #Represents the proper y-value for the square that the board needs to update
    #(Calculated by proper center of each square)
    y_addition = int((y - 360)/240) * -3
    #Represents the proper x-value for the square that the board needs to updatee
    board_num = (x + 360)/240
    #Checks board and updates the visual grid 
    if (board[int(board_num) + int(y_addition)] == "_"):
        board[int(board_num) + int(y_addition)] = "O"
        draw_board(board)
        return True
    else:
        print("Sorry, you can't do that.")
        return False

def check_game_over(board):
    """
    signature: list(str) -> bool
    Given the current state of the board, determine
    if the game is over, by checking for
    a three-in-a-row pattern in horizontal,
    vertical, or diagonal lines; and also if the
    game has reached a stalemate, achieved when
    the board is full and no further move is possible.
    If there is a winner or if there is a stalemante, display
    an appropriate message to the user and clear the board
    in preparation for the next round. If the game is over,
    return True, otherwise False.
    """
    end = False
    for j in range (0, len(board)):
        if (board[j] != "_"):
            #Checks if either player can win diagonally
            if ((j == 0 and board[0] == board[4] == board[8]) or
                (j == 2 and board[2] == board[4] == board[6])):
                winner = j
                end = True
            #Checks if either player can win vertically or horizontally
            elif ((j in [0, 3, 6] and board[j] == board[j + 1] == board[j + 2]) or
                  (j in [0, 1, 2] and board[j] == board[j + 3] == board[j + 6])):
                winner = j
                end = True
    #Determines winner
    if (end):
        if (board[winner] == "X"):
            end_screen("The computer wins!", board)
        elif (board[winner] == "O"):
            end_screen("You win!", board)
            
    #Checks if the board is full (TIE)
    count = 0
    for square in range (0, len(board)):
        if (board[square] != "_"):
            count += 1
    if (count == 9):
        end = True
        end_screen("Tie!", board)   
    return end

def end_screen (words, board):
    '''
    str, list(str) -> NoneType
    Displays the end screen including a message and cleans the board.
    '''
    #Centers and writes the end display message
    turtle.goto(0,0)
    turtle.write(words, align = "center", font = ("Arial", 50, "normal"))
    turtle.goto(0,-100)
    turtle.write("Click a square to play again.", align = "center", font = ("Arial", 25, "normal"))
    #Clears the board
    for j in range (0, len(board)):
         board[j] = "_"

def do_computer_move(board):
    """
    signature: list(str) -> NoneType
    Given a list representing the state of the board,
    select a position for the computer's move and
    update the board with an X in an appropriate
    position. The algorithm for selecting the
    computer's move shall be as follows: if it is
    possible for the computer to win in one move,
    it must do so. If the human player is able 
    to win in the next move, the computer must
    try to block it. Otherwise, the computer's
    next move may be any random, valid position
    (selected with the random.randint function).
    """

    testboard = []
    #A testboard to predict what the best next move is (instead of directly changing the board)
    #This loop is to avoid the properties of lists in which just setting them equal to one another changes both
    for i in range (0, len(board)):
        testboard.append(board[i])
        
    #Checks if computer can win in one move (ATTACK)
    for j in range (0, len(board)):
        if (testboard[j] == "_"):
            testboard[j] = "X"
            if (check_win(testboard)):
                board[j] = "X"
                return
    #Checks if user can win in one move (DEFENSE)
            testboard[j] = "O"
            if (check_win(testboard)):
                board[j] = "X"
                return
            testboard[j] = "_"
            
    #The following code is make the computer algorithm a bit smarter!
    #Sets computer move to board[4] if possible
    if (board[4] == "_"):
        board[4] = "X"
        return

    #Last resort: random computer move
    validrand = random.randint(0,8)
    while (board[validrand] != "_"):
        validrand = random.randint(0,8)
    board[validrand] = "X"

def check_win(board):
    '''
    list(str) -> boolean
    If either player can win in one move, then returns True. Otherwise, False.
    '''
    #Checking if either player won diagonally
    if ((board[0] != "_" and board[0] == board[4] == board[8]) or
        (board[2] != "_" and board[2] == board[4] == board[6])):
        return True
    
    for i in range (0, len(board)):
        #Checking if either player won straight
        if (((i == 0 or i == 3 or i == 6) and board[i] != "_" and
            board[i] == board[i + 1] == board[i + 2]) or
            (i <= 2 and board[i] != "_" and board[i] == board[i + 3] == board[i + 6])):
            return True
    return False

def clickhandler(x, y):
    """
    signature: int, int -> NoneType
    This function is called by turtle in response
    to a user click. The parameters are the screen
    coordinates indicating where the click happened.
    The function will call other functions. You do not
    need to modify this function, but you do need
    to understand it.
    """
    if do_user_move(the_board,x,y):
        draw_board(the_board)
        if not check_game_over(the_board):
            do_computer_move(the_board)
            draw_board(the_board)
            check_game_over(the_board)

def main():
    """
    signature: () -> NoneType
    Runs the tic-tac-toe game. You shouldn't
    need to modify this function.
    """
    turtle.tracer(0,0)
    turtle.hideturtle()
    turtle.onscreenclick(clickhandler)
    draw_board(the_board)
    turtle.mainloop()
    
main()

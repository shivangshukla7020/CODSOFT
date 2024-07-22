import random as rd
import time

board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
total_moves = [1,2,3,4,5,6,7,8,9] # Used for AI to generate random moves when required
user_moves = [] # Used by AI to generate defending moves for player
ai_moves = [] # Used by AI to generate winning moves
c = 9 # Keeps to track of attempts

# Function to print board
def printBoard():
  print("\n")
  k = 0
  for i in board:
    q = 0
    print("      ",end='')
    for j in i:
      print(j,end='')
      if(q < 2) :
        q += 1 
        print(" | ",end='')
    print()
    if k < 2 :
      k +=1
      print("   ---------------")
  print("\n")



def check_win(board):
  # Horizontal Check
  if ((board[0][0] == board[0][1]) and (board[0][1] == board[0][2]) and board[0][0] != ' ') : return True
  elif ((board[1][0] == board[1][1]) and (board[1][1] == board[1][2]) and board[1][0] != ' ') : return True
  elif ((board[2][0] == board[2][1]) and (board[2][1] == board[2][2]) and board [2][0] != ' ') : return True 

  # Vertical Check
  elif ((board[0][0] == board[1][0]) and (board[1][0] == board[2][0]) and board[0][0] != ' ') : return True
  elif ((board[0][1] == board[1][1]) and (board[1][1] == board[2][1]) and board[0][1] != ' ') : return True
  elif ((board[0][2] == board[1][2]) and (board[1][2] == board[2][2]) and board[0][2] != ' ') : return True

  # Diagonal Check
  elif ((board[0][0] == board[1][1]) and (board[1][1] == board[2][2]) and board[0][0] != ' ') : return True
  elif ((board[0][2] == board[1][1]) and (board[1][1] == board[2][0]) and board[0][2] != ' ') : return True

  else : return False

def board_empty():
  return c == 8


# Conditions for AI to use for defeating the player
def ai_player():
  # Win cases
  if(2 in ai_moves and 3 in ai_moves and board[0][0] == ' '):
    return 1
  if(1 in ai_moves and 3 in ai_moves and board[0][1] == ' '):
    return 2
  if(1 in ai_moves and 2 in ai_moves and board[0][2] == ' '):
    return 3
  if(5 in ai_moves and 6 in ai_moves and board[1][0] == ' '):
    return 4
  if(4 in ai_moves and 6 in ai_moves and board[1][1] == ' '):
    return 5
  if(4 in ai_moves and 5 in ai_moves and board[1][2] == ' '):
    return 6
  if(8 in ai_moves and 9 in ai_moves and board[2][0] == ' '):
    return 7
  if(7 in ai_moves and 9 in ai_moves and board[2][1] == ' '):
    return 8
  if(7 in ai_moves and 8 in ai_moves and board[2][2] == ' '):
    return 9 
  
  # Middle edges cases to defend
  if (((1 in user_moves and 3 in user_moves) or (5 in user_moves and 8 in user_moves)) and board[0][1]) == ' ':
    return 2
  if (((7 in user_moves and 9 in user_moves) or (2 in user_moves and 5 in user_moves)) and board[2][1]) == ' ':
    return 8
  if (((1 in user_moves and 7 in user_moves) or (5 in user_moves and 6 in user_moves)) and board[1][0]) == ' ':
    return 4
  if (((3 in user_moves and 9 in user_moves) or (4 in user_moves and 5 in user_moves)) and board[1][2]) == ' ':
    return 6
  
  # Corner cases to defend
  if (((2 in user_moves and 3 in user_moves) or (5 in user_moves and 9 in user_moves) or (4 in user_moves and 7 in user_moves)) and board[0][0]) == ' ':
    return 1
  if (((1 in user_moves and 2 in user_moves) or (5 in user_moves and 7 in user_moves) or (6 in user_moves and 9 in user_moves)) and board[0][2]) == ' ':
    return 3
  if (((1 in user_moves and 4 in user_moves) or (5 in user_moves and 3 in user_moves) or (8 in user_moves and 9 in user_moves)) and board[2][0]) == ' ':
    return 7
  if (((3 in user_moves and 6 in user_moves) or (1 in user_moves and 5 in user_moves) or (7 in user_moves and 8 in user_moves)) and board[2][2]) == ' ':
    return 9


  # Center case to defend
  if ((1 in user_moves and 9 in user_moves) or (4 in user_moves and 6 in user_moves) or (7 in user_moves and 3 in user_moves) or (2 in user_moves and 8 in user_moves)) and board[1][1] == ' ' :
    return 5
  
  return rd.choice(total_moves)

# Function to update the board list according to the attempt of user and AI

def make_move(num,sign):
  if num == 1 and board[0][0] == ' ':
    board[0][0] = sign
  elif num == 2 and board[0][1] == ' ':
    board[0][1] = sign
  elif num == 3 and board[0][2] == ' ':
    board[0][2] = sign
  elif num == 4 and board[1][0] == ' ':
    board[1][0] = sign
  elif num == 5 and board[1][1] == ' ':
    board[1][1] = sign
  elif num == 6 and board[1][2] == ' ':
    board[1][2] = sign
  elif num == 7 and board[2][0] == ' ':
    board[2][0] = sign
  elif num == 8 and board[2][1] == ' ':
    board[2][1] = sign
  elif num == 9 and board[2][2] == ' ':
    board[2][2] = sign
  else : return -1
     

while(c > 0):
  printBoard()

  # User TURN ================================================================
  print("Enter your move : ",end = '')
  user_input = int(input())
  check = make_move(user_input,'X')
  while(check == -1):
    print("Wrong Input Enter again : ")
    user_input = int(input())
    check = make_move(user_input,'X')
  printBoard()
  if(check_win(board)):
    print("You WON !!")
    break
  total_moves.remove(user_input)
  user_moves.append(user_input)
  c-=1
  if(c == 0) :
    print("Draw !!")
    break



  # AI's TURN ==================================================================
  print("AI MAKING MOVE.",end = '')
  for i in range(5):
    time.sleep(0.3)
    print(".",end='')
  move = ai_player()
  print(move)
  make_move(move,'O')
  ai_moves.append(move)
  total_moves.remove(move)
  printBoard()
  c-=1
  if(c == 0) :
     print("Draw !!")
     break
  if(check_win(board)):
    print("You Lost")
    break
  
#  Pig
#  For Marie Tsaasan
#  By Adam Hyman
#  Python at Orange Coast - CS231-42100


#  Websites used:
#
#  https://stackoverflow.com/questions/6423814/is-there-a-way-to-check-if-two-object-contain-the-same-values-in-each-of-their-v
#  Used to compare different instances of the same object to each other
#
#  https://www.tutorialspoint.com/How-to-calculate-absolute-value-in-Python
#  Used to get absolute value
#
#  https://stackoverflow.com/questions/306400/how-to-randomly-select-an-item-from-a-list
#  Used in the ending message to select 1 item randomly from a list


#  This code creates a game of Pig as per Marie Tsaasan's specifications for Python 2 @ OCC
#  I tried to follow David Kay's Design Recipe, but couldn't do any assert's.
#  I didn't understand point 6 of DK's DR.
#
#  I skimmed PEP 20 and think my code follows it very well.


#  Used to generate a discrete RV between 1 and 100 for the x & y coordinates of the pig.
#  Used to generate a continuous RV between 0 and 1 to calculate the position of the pig. 
#  Used to choose a random item from a list for the ending message.
import random


#  This is the number of squares on the x axis and on the y-axis of the board.
#  If board size is 10:
#    -  The board is a 10-by-10 board, which will contain 100 squares
#    -  When flipping a pig, both the x and y positions will be random variables between 1 and 10
#  A pig always lands in one square.
#  If 2 pigs land in the same square, it's a Piggyback, and the player that tossed them loses the game
#  If pigs land in adjacent squares, it's an Oinker, and the player that tossed them loses the game
#
#  I think a good value for this is between 15 and 25.  There will then be 225 squares on the board (15 by 15)
#  There is a 1 in 250 chance of a Piggyback and an approximately 3.5% chance of an oinker
#  (because if a Pig lands in a square that isn't on the edge of the board, there will be
#  8 squares that are adjacent, and 8 / 250 = 3.5555%).
#
#  To test the code, you'll want to make the board smaller, to increase the chance of a Piggyback and
#  Oinker
#  I recommend using a board size of 4 or 5 for testing

board_size = 20


#  Pig class
#  A pig that has a position (Side, Razorback, etc) and x & y values for position.
#  The toss function simulates tossing the pig and generates the position, x & y coordinates with
#  random numbers.

class Pig:
  def __init__(self) -> None:
    '''
    Initializes a pig.  Since the position is set whenever a pig is tossed, I'm not sure if this __init__ is necessary.
    But it might be standard Python practice to include it, so I'm leaving it, just in case.
    '''
    self.__position = 'Sider'

  def get_position(self) -> str:
    '''  Returns positio of pig  '''
    return self.__position

  def get_x(self) -> int:
    '''  Returns x coordinate of pig  '''
    return self.__x

  def get_y(self) -> int:
    '''  Returns y coordinate of pig  '''
    return self.__y

  def toss(self) -> None:
    '''
    Simulates tossing a pig.
    Uses random variables to set the position, x & y coordinates
    '''

    #  randint(a, b) gives a random integer between a and b, inclusive.
    #  https://docs.python.org/3/library/random.html
    self.__x = random.randint(1, board_size)
    self.__y = random.randint(1, board_size)
    
    rv = random.random()

    if rv < 2 / 19:
      self.__position = 'Leaning Jowler'  # Prob 2 / 19
    elif rv < 5 / 19:
      self.__position = 'Snouter'         # Prob 3 / 19
    elif rv < 9 / 19:
      self.__position = 'Trotter'         # Prob 4 / 19
    elif rv < 13 / 19:
      self.__position = 'Razorback'       # Prob 4 / 19
    else:
      self.__position = 'Sider'           # Prob 6 / 19

  def on_top (self, other) -> bool:
    '''  Returns true if one pig is on top of another pig.  Otherwize returns false.  '''
    if self.__x == other.get_x() and self.__y == other.get_y():
      return True
    else:
      return False

  def touching (self, other) -> bool:
    '''  Returns true if pigs are in adjacent squares.  False otherwize.  '''

    #  If I removed the check for on_top below, it wouldn't affect the running of the code
    #  because in the Player's toss function, I first check for on_top, and only if that test fails, 
    #  do I check if the pigs are touching.
    #  I'm leaving it in anyways, so that if someone wanted to check touching before on_top, they
    #  wouldn't have to modify the touching function.
    if abs(self.__x - other.get_x()) <= 1 and abs(self.__y - other.get_y()) <= 1 \
      and not (self.on_top (other)):
      return True
    else:
      return False


#  A player that plays the pig game.  Each player tosses 2 pigs.
class Player:

  def __init__(self, name, target) -> None:
    '''  Player has a name, points, target score and 2 pigs that can be tossed  '''
    self.__name = name
    self.__points = 0
    self.__target_score = target
    self.__pig1 = Pig()
    self.__pig2 = Pig()

  def get_points(self) -> int:
    '''  Returns number of points that the player has  '''
    return self.__points

  def turn(self) -> bool:
    '''  A player tosses until they pass or lose the game (Piggyback) or lose all their points (Oinker)  '''

    turn_status = 'Go Again'

    while (turn_status == 'Go Again'):
      current_action = ''

      #  Find out if user wants to ROLL or PASS
      #  No error checking on the users input
      #  Could be added in a future version
      while (current_action.upper()!='ROLL' and current_action.upper()!='PASS'):
        current_action = input(self.__name + ', it is your turn.  Do you want to ROLL or PASS?  ')

      if (current_action.upper() == 'PASS'):
        print('')
        break
        
      if (current_action.upper() == 'ROLL'):
        #  Toss the pigs
        #  Returns 'End of Turn' / 'End of Game' / 'Go Again'
        turn_status = self.toss()

        #  If after  
        if (turn_status == 'End of Turn'):
          return False

        if (turn_status == 'End of Game'):
          return True
        
        

  def toss (self) -> str:
    '''
    Tosses both pigs
    Returns status at the end of the turn
        'End of Turn' / 'End of Game' / 'Go Again'
    '''
    self.__pig1.toss()
    self.__pig2.toss()

    #  Piggy back - one pig on top of another.  This ends the game.
    if self.__pig1.on_top(self.__pig2):
      self.__points = -1
      print('Piggyback!  You lost the game!\n')
      return 'End of Game'

    #  Oinker - pigs are touching
    elif self.__pig1.touching(self.__pig2):
      self.__points = 0
      print('Oinker!  Pigs are touching!  Your score goes to ZERO!\n')
      #  Returns True because turn is over
      return 'End of Turn'

    #  Pigs are in same position
    elif self.__pig1.get_position() == self.__pig2.get_position():
      if self.__pig1.get_position() == 'Sider':
        self.__points += 1
        print('Double Sider!  1 point!')
      elif self.__pig1.get_position() == 'Razorback':
        self.__points += 20
        print('Double Razorback!  20 points!')
      elif self.__pig1.get_position() == 'Trotter':
        self.__points += 20
        print('Double Trotter!  20 points!')
      elif self.__pig1.get_position() == 'Snouter':
        self.__points += 40
        print('Double Snouter!  40 points!')
      elif self.__pig1.get_position() == 'Leaning Jowler':
        self.__points += 60
        print('Double Leaning Jowler!  60 points!')

    #  Pigs are in different positions
    else:
      if self.__pig1.get_position() == 'Sider':
        print('Sider!  0 points!')
      elif self.__pig1.get_position() == 'Razorback':
        self.__points += 5
        print('Razorback!  5 points!')
      elif self.__pig1.get_position() == 'Trotter':
        self.__points += 5
        print('Trotter!  5 points!')
      elif self.__pig1.get_position() == 'Snouter':
        self.__points += 10
        print('Snouter!  10 points!')
      elif self.__pig1.get_position() == 'Leaning Jowler':
        self.__points += 15
        print('Leaning Jowler!  15 points!')

      if self.__pig2.get_position() == 'Sider':
        print('Sider!  0 points!')
      elif self.__pig2.get_position() == 'Razorback':
        self.__points += 5
        print('Razorback!  5 points!')
      elif self.__pig2.get_position() == 'Trotter':
        self.__points += 5
        print('Trotter!  5 points!')
      elif self.__pig2.get_position() == 'Snouter':
        self.__points += 10
        print('Snouter!  10 points!')
      elif self.__pig2.get_position() == 'Leaning Jowler':
        self.__points += 15
        print('Leaning Jowler!  15 points!')
        
    print(self.__name + ' has ' + str(self.__points) + ' points.\n')

    #  Turn is over
    if self.__points == -1 or self.__points >= self.__target_score:
      return 'End of Game'
    #  Turn is not over
    else:
      return 'Go Again'


#  Class that contains the players, and controls them.
#  play_game() is what makes the players play, by running the each player's turn()
#  function, which returns True if the game is over, and false if the game is not over.
#
#  After play_game() has run, it prints a message to congratulate the winner.

class Game():

  def __init__(self) -> None:
    '''  Creates a game, which has 2 players and a target score and a boolean to keep track of whether the game is over  '''
    print('Welcome to the Pig game!\n')

    self.__player1_name = input('Please enter the name of player 1:  ')
    self.__player2_name = input('Please enter the name of player 2:  ')
    
    #  Doesn't validate the input in this version
    #  This must be an integer
    self.__target_score = int(input('Please enter the target score:  '))
    print('')

    self.__player1 = Player(self.__player1_name, self.__target_score)
    self.__player2 = Player(self.__player2_name, self.__target_score)
    
    self.__game_over = False

    self.play_game()

  def play_game(self) -> None:
    '''
    Has the players take turns (using the players turn() function, until the game
    is over.
    When the game is over, it calls ending_message()
    '''

    while (not(self.__game_over)):

      self.__game_over = self.__player1.turn()

      if (not(self.__game_over)):
        self.__game_over = self.__player2.turn()

    #  Player 1 won
    if self.__player1.get_points() >= self.__target_score or self.__player2.get_points == -1:
      self.ending_message(self.__player1_name, self.__player2_name)
    #  Player 2 won
    else:
      self.ending_message(self.__player2_name, self.__player1_name)

  def ending_message(self, winner, loser):
    '''  Print random victory message  '''
    m1 = ['Congratulations', 'Great job', 'Way to go', 'Solid performance', 'Nicely done']
    m2 = ['Second place goes to', 'You defeated', 'Nice attempt', 'Better luck next time']
    print (random.choice(m1) + ' ' + winner + '!!  ' + random.choice(m2) + ' ' + loser + '.')
    print ('Thank you for playing the Pig game!')

#  Creates and starts a game of Pig
mygame = Game()

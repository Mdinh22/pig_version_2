import random


class player:
    """Custom class to track player name and score."""

    def __init__(self, name, score):
        self.name = name
        self.score = score


def take_name(name) -> player:
    """Constructor for a new player object."""
    new_player = player(name, 0)
    return new_player


assert type(take_name("TestPlayer")) == player


def roll_pig() -> list:
    """ Rolls a pig, taking two results from five
    possible outcomes, with repeats possible."""
    potential_results = ["Sider", "Razorback", "Trotter",
                         "Snouter", "Leaning Jowler"]
    roll_result = random.choices(potential_results,
                                 weights=[35, 30, 22, 9, 4], k=2)
    return roll_result


assert roll_pig()[0] in ["Sider", "Razorback", "Trotter",
                         "Snouter", "Leaning Jowler"]


def roll_oinker() -> bool:
    """Rolls for the chance of an Oinker occurring."""
    oinker_roll = random.randint(0, 50)
    if oinker_roll == 1:
        return True
    else:
        return False


assert type(roll_oinker()) == bool


def roll_piggyback() -> bool:
    """Rolls for the chance of a Piggyback occurring."""
    piggyback_roll = random.randint(0, 100)
    if piggyback_roll == 1:
        return True
    else:
        return False


assert type(roll_piggyback()) == bool


def get_result_doubles(double_rolls) -> int:
    """Calculates the result of a doubles roll."""
    if double_rolls[0] == "Sider":
        return 1
    if double_rolls[0] == "Razorback":
        return 20
    if double_rolls[0] == "Trotter":
        return 20
    if double_rolls[0] == "Snouter":
        return 40
    if double_rolls[0] == "Leaning Jowler":
        return 60


assert get_result_doubles(["Snouter", "Snouter"]) == 40


def get_result_mixed(mixed_rolls) -> int:
    """Calculates the result of a mixed roll."""
    mixed_result = 0
    for pig in mixed_rolls:
        if pig == "Sider":
            mixed_result += 0
        elif pig == "Razorback":
            mixed_result += 5
        elif pig == "Trotter":
            mixed_result += 5
        elif pig == "Snouter":
            mixed_result += 10
        elif pig == "Leaning Jowler":
            mixed_result += 15
    return mixed_result


assert get_result_mixed(["Snouter", "Trotter"]) == 15


def get_result(roll_results, rolling_player, other_player) -> list:
    """Calls the calculation functions and
    reports the results, changing the player's score."""
    if roll_piggyback():
        rolling_player.score = -1
        other_player.score = 999999
        return ["Piggyback: One pig is atop the other. You lose!", 2]
    elif roll_oinker():
        rolling_player.score = 0
        return ["Oinker: The pigs are touching. "
                "You have lost your points!", 1]
    elif roll_results[0] == roll_results[1]:
        rolling_player.score += get_result_doubles(roll_results)
        return ["Double Roll of: Two " + roll_results[0] + "s", 0]
    else:
        rolling_player.score += get_result_mixed(roll_results)
        return ["Mixed Roll of " + roll_results[0] +
                " and " + roll_results[1], 0]


assert_player1 = player("Assert1", 0)
assert_player2 = player("Assert2", 0)
assert get_result(["Snouter", "Snouter"],
                  assert_player1, assert_player2)[1] in [0, 1, 2]


def player_roll(player1, player2) -> None:
    """Facilities a single turn for a player, allowing them to roll or pass
    # unless they roll one of the two round-ending outcomes."""
    print("...........................")
    print(player1.name + " : " + str(player1.score) +
          ", " + player2.name + " : " + str(player2.score))
    print("...........................")
    print("Your turn, " + player1.name)
    print()

    finished = 0

    while finished == 0:
        turn_choice = input("ROLL or PASS? ")
        if turn_choice.lower() == "pass":
            finished = 1
        if turn_choice.lower() == "roll":
            result_rolls = roll_pig()
            roll_result = get_result(result_rolls, player1, player2)
            print("You rolled a " + roll_result[0])
            finished = roll_result[1]
            print("Your score is " + str(player1.score) + ".\n")


def show_winner(player1, player2) -> None:
    """Shows the winner, denoted as the player with the highest score."""
    print("...........................")
    print("GAME OVER")
    print(player1.name + ": " + str(player1.score))
    print(player2.name + ": " + str(player2.score))
    if player1.score > player2.score:
        print(player1.name + " has won!")
    elif player2.score > player1.score:
        print(player2.name + " has won!")


if __name__ == "__main__":
    print("...........................")
    print("Welcome to the game of pig!")
    print("...........................")

    p1_name = input("Please enter the first player's name. ")
    player_one = take_name(p1_name)
    p2_name = input("Now for the second player. ")
    player_two = take_name(p2_name)

    print("How many points should the target be?")
    win_score = int(input("Enter the winning point "
                          "threshold as an integer: "))

    while player_one.score < win_score and player_two.score < win_score:
        player_roll(player_one, player_two)
        if player_one.score == -1 \
                or player_two.score == -1 \
                or player_one.score >= win_score \
                or player_two.score >= win_score:
            break
        player_roll(player_two, player_one)

    show_winner(player_one, player_two)

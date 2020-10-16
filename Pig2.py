import random
import sys
import time

class Player:
    def __init__(self, name, total=0):
        self.name = name
        self.total = total

    def newTotal(self, newPoint):
        self.total = self.total + newPoint

    def decision(self, game_total=0):
        roll = input("Press r to roll and h to pass")
        return roll

class ComputerPlayer(Player):
    def decision(self, game_total):
        limit = 100 - self.total
        limit = 25 if limit > 25 else limit

        if ( game_total < limit ):
            roll = 'r'
            rolling = 'rolling'
        else:
            roll = 'h'
            rolling = 'passing'

        return roll

class PlayerFactory:
    def getPlayer(self, player_type, name):
        if player_type == 'h':
            return Player(name)
        if player_type == 'c':
            return ComputerPlayer(name)

class Dice:
    def __init__(self, roll=0):
        self.roll =  roll

    def newRoll(self, seed): 
        random.seed(seed)
        self.roll = random.randrange(1, 7)
        return self.roll

class GameCenter:
    def __int__(self, players, total=0):
        self.player1 = players[1]
        self.player2 = players[2]
        self.turnTotal = total

    def turnScore(self, newPoint):
        self.turnTotal = self.turnTotal + newPoint
        return self.turnTotal

    def totalScoreCheck(self, player, win_ponts):
        score = player.total + self.turnTotal
        if score >= win_ponts:
            player.total = score
            print ("{}, congratulations! You won!!".format(player.name))
            print ('Your final score is ', player.total)
            self.gameOver()

    def turnSwitch(self, current_player):
        self.turnTotal = 0
        print ('Switching turns.')
        return 2 if current_player == 1 else 1

    def statusMessage(self, player, new_roll):
        print ("%s rolled %s. Score for this turn is %s and player's total score is %s" % \
        (player.name, new_roll, self.turnTotal, player.total ))

    def welcomeMessage(self, player):
        print ("%s, your current score is %s. Good luck!" % \
        (player.name,player.total))

    def gameOver(self):
        print ("Restart to play again." )   
        sys.exit()

class Proxy:
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp
        self.dice = None
        self.dice = Dice()

    def timeCheck(self, timestamp):
        if (self.timestamp == 0 or self.timestamp > time.time() ):
            seed = time.time()
            return self.dice.newRoll(seed)
        else:
            print("Game Over")
            print ("Time is up!")
            sys.exit() 


def main():
    player1 = input('enter player type: "c" - computer, "h" -human')
    player2 = input('enter player type: "c" - computer, "h" -human')
    timed = input('for timed game enter y')
    factory = PlayerFactory()
    game = GameCenter()

    players = { 1: factory.getPlayer(player1,'player1'),
                2: factory.getPlayer(player2,'player2')}

    if timed=='y':
        timestamp = time.time() + 60
    else:
        timestamp = 0

    p = Proxy(timestamp)

    current_player = 1
    game.turnTotal = 0
    game.welcomeMessage(players[current_player])

    while (players[current_player].total < 100) :
        new_roll = p.timeCheck(timestamp)

        roll = players[current_player].decision(game.turnTotal)

        if roll == 'r':

            print ("DICE: ", new_roll)
            if new_roll == 1:
                game.turnTotal = 0
                game.statusMessage(players[current_player],new_roll)
                current_player = game.turnSwitch(current_player)
                game.welcomeMessage(players[current_player])
                p.timeCheck(timestamp)
            else:
                game.turnTotal = game.turnScore(new_roll)
                game.statusMessage(players[current_player],new_roll)
                game.totalScoreCheck(players[current_player], 100)
                p.timeCheck(timestamp)

        elif roll == 'h':
            p.timeCheck(timestamp)
            print (players[current_player].name, " adds ", game.turnTotal, " points to his total of ", players[current_player].total)
            players[current_player].newTotal(game.turnTotal)
            current_player = game.turnSwitch(current_player)
            game.welcomeMessage(players[current_player])

        else:
            print ("Press r to roll or h to pass")

        p.timeCheck(timestamp)


if __name__ == '__main__':
    main()

import random

"""This class holds information on a match, performs player pairings and calculates points"""


class Match:
    # Default Constructor for a Match
    def __init__(self, tournament, players=None, winner=None, completed=None, points=None, ):
        self.players = players
        self.winner = winner
        self.completed = completed
        self.points = points if points is not None else {}
        self.tournament = tournament

    # Performs pairing based on rounds. In beginning pairs randomly, after pairs based on points
    def pairing(self):
        if self.tournament.curr_round == 1:
            all_players = self.tournament.players[:]
            if len(all_players) % 2 != 0:
                print("Cannot pair odd number of players.")
                return []
            random.shuffle(all_players)
            matches = []
            for i in range(0, len(all_players), 2):
                if i + 1 < len(all_players):
                    matches.append((all_players[i], all_players[i + 1]))
            return matches
        else:
            # Pairing based on points for subsequent rounds
            self.calculate_points()
            sort_players = sorted(self.points.keys(), key=lambda player: self.points.get(player, 0), reverse=True)
            matches = []
            while len(sort_players) >= 2:
                player1 = sort_players.pop(0)
                player2 = sort_players.pop(0) if sort_players else None
                if player2 is None:
                    # If there's an odd number of players, pair the last player with a bye
                    matches.append((player1, "bye"))
                else:
                    matches.append((player1, player2))
            return matches

    # Method adds a point for a player if they are declared the winner of a match
    def calculate_points(self):
        for round_data in self.tournament.rounds:
            winner = round_data.get("winner")
            if winner:
                if winner not in self.points:
                    self.points[winner] = 1  # Assign 1 point to the winner
                else:
                    self.points[winner] += 1
                players = round_data.get("players")
                loser = players[0] if players[0] != winner else players[1]
                if loser not in self.points:
                    self.points[loser] = 0
            elif winner is None:
                players = round_data.get("players")
                if players:
                    for player in players:
                        if player not in self.points:
                            self.points[player] = 0.5
                        else:
                            self.points[player] += 0.5

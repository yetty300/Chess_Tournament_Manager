import json
import os

"""THis holds the information for a tournament as well as some basic functions (save, create and load)"""


class Tournament:
    """
    Program creates a tournament instance. Loads a tournament instance, saves a tournament instance
    and deletes a tournament instance.
    """

    # Constructor outline for a tournament (has empty attributes to start)
    def __init__(self, name=None, start=None, end=None, num_rounds=None, curr_round=None, complete=None,
                 venue=None, players=None, finished=None, rounds=None):

        self.name = name
        self.start_date = start
        self.end_date = end
        self.venue = venue
        self.num_rounds = num_rounds
        self.curr_round = curr_round
        self.complete = complete
        self.players = players
        self.finished = finished
        self.rounds = rounds

    # Defines each category and relates it to constructor attributes
    def __str__(self):
        return f"Tournament: {self.name}\nVenue: {self.venue}\n From: {self.start_date}\nTo: {self.end_date}\n" \
               f"Rounds: {self.rounds}\nPlayers: {self.players}\nNumber of Rounds: {self.num_rounds}\n" \
               f"Completed: {self.complete}\nCurrent Round: {self.curr_round}"

    # Creates a new tournament through user input and formats it, so it outputs correctly on screen

    def create(self):
        self.name = input("Enter tournament name: ")
        self.start_date = input("Enter start date (DD-MM-YYYY): ")
        self.end_date = input("Enter end date (DD-MM-YYYY): ")
        self.venue = input("Enter venue: ")
        self.num_rounds = int(input("Enter number of rounds: "))
        self.curr_round = 1
        self.complete = False
        self.players = []
        self.finished = False
        self.rounds = []

    def format(self):
        """Serialize the tournament object to JSON-compatible format"""
        return {
            "name": self.name,
            "dates": {
                "from": self.start_date,
                "to": self.end_date,
            },
            "venue": self.venue,
            "number_of_rounds": self.num_rounds,
            "current_round": self.curr_round,
            "completed": self.complete,
            "players": self.players,
            "rounds": self.rounds
        }

    # Method saves tournament instance to data folder in its own JSON file
    def save(self, filename=None):
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")
        if filename is None:
            if self.name is not None:
                filename = f"data/tournaments/{self.name.replace(' ', '_')}.json"
            else:
                print("No Tournament file to save.")
                return
        else:
            filename += f"data/tournaments/{filename}.json"

        with open(filename, 'w') as fp:
            json.dump(self.format(), fp, indent=4)
        print(f"Tournament data saved to {filename}")

    # Method loads a tournament JSON by name through user input from data folder
    @classmethod
    def load(cls, filename):

        if not os.path.exists(filename):
            print(f"No tournament found with the name '{filename}'.")
            return None

        with open(filename) as fp:
            data = json.load(fp)
        try:
            return cls(
                name=data["name"],
                start=data["dates"]["from"],
                end=data["dates"]["to"],
                venue=data["venue"],
                num_rounds=data["number_of_rounds"],
                curr_round=data["current_round"],
                complete=data["completed"],
                players=data["players"],
                finished=data.get("finished", "false"),
                rounds=data["rounds"],
            )
        except KeyError as e:
            print(f"Error missing key in tournament datta: {e}")
            return None

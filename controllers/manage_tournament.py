import os
import json

from models.match import Match


class ManageTournament:

    def __init__(self, tournament):
        self.tournament = tournament

    def menu(self):
        print("Select option: ")
        print("1. Register player for tournament")
        print("2. Enter results for matches in current round")
        print("3. Advance to the next round")
        print("4. Get tournament report")
        print("5. View Tournament")
        print("6. Delete Tournament")
        print("7. Go back to main menu")

        try:
            choice = int(input("Select option: "))
            if choice == 1:
                self.register_player()
            elif choice == 2:
                self.enter_results()
            elif choice == 3:
                self.advance_round()
            elif choice == 4:
                self.generate_report()
            elif choice == 5:
                self.view_tournament()
            elif choice == 6:
                self.delete()
            elif choice == 7:
                return
            else:
                print("invalid choice")
        except ValueError:
            print("Invalid input. Please select a number")

    # Method advances the round of the tournament then call pair method and marks complete and finished if necessary
    def advance_round(self):
        if self.tournament.curr_round == self.tournament.num_rounds:
            print("Tournament Finished")
            self.menu()
        print("Are you sure you want to advance to the next round?")
        choice = input("yes or no: ").lower()
        if choice == "yes":
            if self.tournament.curr_round < self.tournament.num_rounds:
                self.tournament.curr_round += 1
                self.pair()
                print("Advanced round by one, new matches generated.")
        elif choice == "no":
            print("Round not advanced.")
        else:
            print("Invalid choice")
            self.advance_round()
        self.tournament.save()
        self.menu()

    # Method prints the information of current loaded tournament
    def view_tournament(self):
        print("Tournament View")
        print(f"Name: {self.tournament.name}")
        print(f"Start Date: {self.tournament.start_date}")
        print(f"End Date: {self.tournament.end_date}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Number of Rounds: {self.tournament.num_rounds}")
        print(f"Current Round: {self.tournament.curr_round}")
        print(f"Completed: {self.tournament.complete}")
        print(f"Players: {self.tournament.players}")
        print(f"Finished: {self.tournament.finished}")
        print(f"Rounds: {self.tournament.rounds}")
        self.menu()

    # Method registers players for tournament by searching a combined list of players then calls pair method

    def register_player(self):
        all_players = []
        files = []
        for file_name in os.listdir("data/clubs"):
            if file_name.endswith(".json"):
                files.append(os.path.join("data/clubs", file_name))
        for file in files:
            with open(file) as fp:
                data = json.load(fp)
                players = data.get("players", [])
                all_players.extend(players)
        for i, player in enumerate(all_players, start=0):
            print(f"{i}.{player}")

        def search_player_by_id(chess_id):
            for player in all_players:
                if player.get("chess_id") == chess_id:
                    return player
            return None

        def search_player_by_name(name):
            matching_players = []
            for player in all_players:
                if name.lower() in player.get("name").lower():
                    matching_players.append(player)
            return matching_players

        add_another_player = True
        chosen_player_ids = []
        while add_another_player:
            choice = input("Please type in name to search by name or ID to search by ID or 'quit' to exit: ").lower()
            if choice == "id":
                chess_id = input("Enter chess ID: ")
                player = search_player_by_id(chess_id)
                if player:
                    chosen_player_ids.append(chess_id)
                else:
                    print("Player not found with that ID.")
            elif choice == "quit":
                break
            elif choice == "name":
                name = input("Enter player name (partial or full): ")
                matching_players = search_player_by_name(name)
                if matching_players:
                    print("Matching players:")
                    for i, player in enumerate(matching_players, start=1):
                        print(f"{i}. {player['name']} (ID: {player['chess_id']})")
                    player_index = int(input("Select player number: ")) - 1
                    if 0 <= player_index < len(matching_players):
                        chosen_player = matching_players[player_index]
                        chosen_player_ids.append(chosen_player["chess_id"])
                    else:
                        print("Invalid player number.")
                else:
                    print("No matching players found.")
            else:
                print("Invalid choice.")

            add_another_player_input = input("Add another player? (yes/no): ")
            add_another_player = add_another_player_input.lower() == "yes"

            if add_another_player_input.lower() != "yes":
                self.tournament.players.extend(chosen_player_ids)
                self.tournament.save()
                self.pair()
                self.menu()

    # Method allows user to enter the winner of the matches that are not complete yet
    def enter_results(self):
        for match in self.tournament.rounds:
            if not match["completed"]:
                winner_input = input(f"Enter the winner of match {match['players'][0]} vs {match['players'][1]}: ")
                if winner_input in match["players"]:
                    match["winner"] = winner_input
                    match["completed"] = True
                else:
                    print("Invalid input. Please enter a valid player ID.")

            # Check if all matches are completed for the current round
        if all(match["completed"] for match in self.tournament.rounds):
            # Check if it's the final round
            if self.tournament.curr_round == self.tournament.num_rounds:
                self.tournament.finished = True
                self.tournament.complete = True
            self.tournament.save()  # Save the tournament data
            self.menu()  # Return to the menu
        else:
            print("Not all matches are completed yet.")

    def generate_report(self):
        if not self.tournament.rounds:
            print("No round data initialized, unable to generate report")
            return

        for rounds in self.tournament.rounds:
            print("Round printing")
            print(rounds)
            complete = rounds["completed"]
            if not complete:
                print("Cannot generate report. Some matches are not complete.")
                return

        # Calculate points for all matches
        for round_matches in self.tournament.rounds:
            winner = round_matches["winner"]
            if winner is None:
                # Handle cases where winner is None
                pass
            else:
                # Increment points for the winner
                pass

        # Get accumulated points for each player
        accumulated_points = {player: 0 for player in self.tournament.players}
        for round_matches in self.tournament.rounds:
            winner = round_matches["winner"]
            if winner is not None:
                accumulated_points[winner] += 1
            else:
                # Handle cases where winner is None
                pass

        # Sort players by accumulated points
        sorted_players = sorted(accumulated_points.items(), key=lambda x: x[1], reverse=True)

        # Generate report
        report_content = f"""
Tournament Report
-----------------

Tournament Name: {self.tournament.name}
Start Date: {self.tournament.start_date}
End Date: {self.tournament.end_date}
Players:
            
"""

        for player_id, points in sorted_players:
            report_content += f"Player ID: {player_id}, Accumulated Points: {points}\n"

        report_content += "\nMatches:\n"
        for round_num, round_matches in enumerate(self.tournament.rounds, 1):
            report_content += f"Round {round_num}:\n"
            report_content += (f"  Match {round_num}: Winner - {round_matches['winner']},"
                               f" Complete - {round_matches['completed']}\n")

        with open(f"{self.tournament.name}_report.txt", "w") as file:
            file.write(report_content)

        print("Report generated successfully.")

    # Method allows user to delete a tournament JSON by user input
    def delete(self):
        tournament_name = self.tournament.name
        print(tournament_name)
        filename = f"data/tournaments/{tournament_name.replace(' ', '_')}.json"
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Tournament '{tournament_name}' JSON deleted.")
                return
            else:
                print("No file with that name found.")
                self.menu()
        except Exception as e:
            print(f"An error occurred while deleting the tournament JSON file: {e}")

    # Method calls paring function in Match and prints out results
    def pair(self):
        match = Match(tournament=self.tournament)
        matches = match.pairing()
        if matches:
            for match in matches:
                player1, player2 = match
                round_data = {
                    "players": [player1, player2],
                    "completed": False,
                    "winner": None
                }
                self.tournament.rounds.append(round_data)
            self.tournament.save()  # Saving the tournament after generating matches
        else:
            print("No matches generated")

        self.menu()  # Returning to the menu after generating matches

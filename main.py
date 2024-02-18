import json
import os
from models.tournament import Tournament
from controllers.manage_tournament import ManageTournament
from manage_clubs import App

choice = None
while True:
    start_files = []
    tournament_folder = os.path.join("data", "tournaments")
    if os.path.exists(tournament_folder):
        for file_name in os.listdir(tournament_folder):
            if file_name.endswith(".json"):
                file_path = os.path.join(tournament_folder, file_name)
                with open(file_path) as file:
                    data = json.load(file)
                    finished = data.get("finished", False)
                    if not finished:
                        start_date = data["dates"]["from"]
                        start_files.append((file_name, start_date))
    if len(start_files) > 1:
        start_files.sort(key=lambda x: x[1])
        print("Available Tournament Files:")
        for i, (file_name, start_date) in enumerate(start_files, start=1):
            print(f"{i}. {file_name} - Start Date: {start_date}")
    elif len(start_files) == 1:
        selected_file = start_files[0][0]
        selected_file_path = os.path.join(tournament_folder, selected_file)
        data = Tournament.load(selected_file_path)
        manage = ManageTournament(data)
        manage.view_tournament()

    print("Main Menu")
    print("1. Create tournament")
    print("2. View active tournament(s)")
    print("3. View finished tournaments")
    print("4. Manage Clubs")
    print("5. Exit Program")
    choice = int(input("enter your choice: "))

    if choice == 1:
        tourny = Tournament()
        Tournament.create(tourny)
        Tournament.save(tourny)

    elif choice == 2:
        if start_files:
            if len(start_files) > 1:

                try:
                    selection = int(input("Select a file to view (enter the number): ")) - 1
                    selected_file = start_files[selection][0]
                    selected_file_path = os.path.join(tournament_folder, selected_file)
                    data = Tournament.load(selected_file_path)
                    if data:
                        manage = ManageTournament(data)
                        manage.menu()
                except (ValueError, IndexError):
                    print("Invalid selection.")
            else:
                selected_file = start_files[0][0]
                selected_file_path = os.path.join(tournament_folder, selected_file)
                data = Tournament.load(selected_file_path)
                if data:
                    manage = ManageTournament(data)
                    manage.menu()
        else:
            print("No active Tournaments.")
    elif choice == 3:
        finished_json_files = []

        tournament_folder = os.path.join("data", "tournaments")
        if os.path.exists(tournament_folder):
            for file_name in os.listdir(tournament_folder):
                if file_name.endswith(".json"):
                    file_path = os.path.join(tournament_folder, file_name)
                    with open(file_path) as file:
                        data = json.load(file)
                        finished = data.get("finished", False)
                        if finished:
                            start_date = data["dates"]["from"]
                            finished_json_files.append((file_name, start_date))

        if finished_json_files:
            # Sort the list of tuples by start date
            finished_json_files.sort(key=lambda x: x[1])
            print("Available Tournament Files:")
            for i, (file_name, start_date) in enumerate(finished_json_files, start=1):
                print(f"{i}. {file_name} - Start Date: {start_date}")

            try:
                selection = int(input("Select a file to view (enter the number): ")) - 1
                selected_file = finished_json_files[selection][0]
                selected_file_path = os.path.join(tournament_folder, selected_file)
                data = Tournament.load(selected_file_path)
                if data:
                    manage = ManageTournament(data)
                    manage.menu()
            except (ValueError, IndexError):
                print("Invalid selection")

    elif choice == 4:
        app = App()
        app.run()
    elif choice == 5:
        print("Exiting program")
        break
    else:
        print("invalid choice")

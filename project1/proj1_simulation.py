"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
from proj1_event_logger import Event, EventList
from adventure import AdventureGame, use_command, use_menu
from game_entities import Player


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    #   - _player: The Player instance that the simulation uses
    _game: AdventureGame
    _events: EventList
    _player: Player
    _commands: list[str]

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)
        self._player = Player()
        self._commands = commands

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""
        step_num = 1
        for choice in self._commands:
            location = self._game.get_location()
            print("========================== Step Number: " + str(step_num) + ". ==========================")
            print("Location:", location.name)
            print("You chose to:", choice)

            item_commands = [item.command_name for item in self._player.get_inventory() if item.use_command is not None]
            menu = ["look", "inventory", "score", "undo", "log", "quit"]

            if choice in menu:
                use_menu(choice, self._game, self._player, self._events, location)
            else:
                if choice in item_commands:
                    command = self._game.get_item(choice.split(" ")[1]).use_command
                else:
                    command = location.commands[choice]

                if use_command(command, self._game, self._player, location):
                    self._events.add_event(Event(location.id_num, choice, command, False))
            step_num = step_num + 1
            if self._player.moves_left == 0:
                print("You ran out of moves! \nThe project went unsubmitted and you recieved a 0% :( ......")


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    win_walkthrough = ["go south", "go south", "go south", "talk to professor", "go north", "go west", "pickup charger",
                       "go east", "go north", "go west", "talk to group member", "go east", "go north",
                       "submit project"]
    expected_log = [1, 2, 9, 7, 7, 9, 6, 6, 9, 2, 8, 8, 2,
                    1]
    win_sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    win_sim.run()
    assert expected_log == win_sim.get_id_log()

    lose_demo = ["go south", "go east", "go east", "go west", "go west", "go west", "go east", "go south", "go east",
                 "go west", "go south", "go north", "go west", "go east", "go north"]
    expected_log = [1, 2, 3, 4, 3, 2, 8, 2, 9, 5, 9, 7, 9, 6, 9]
    lose_sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    lose_sim.run()
    assert expected_log == lose_sim.get_id_log()

    inventory_demo = ["pickup notebook", "go south", "pickup scrap paper", "go east", "search bookshelves", "go west",
                      "go west", "search bookshelves", "inventory"]
    expected_log = [1, 1, 2, 2, 3, 3, 2, 8]
    inventory_sim = AdventureGameSimulation('game_data.json', 1, inventory_demo)
    inventory_sim.run()
    assert expected_log == inventory_sim.get_id_log()

    scores_demo = ["go south", "go east", "search bookshelves", "score", "go west", "go south", "go south",
                   "talk to professor", "score"]
    expected_log = [1, 2, 3, 3, 2, 9, 7]
    scores_demo = AdventureGameSimulation('game_data.json', 1, scores_demo)
    scores_demo.run()
    assert expected_log == scores_demo.get_id_log()

    # Showcase buy command
    # Simulation will "buy" cash by exchanging scrap paper
    # Simulation will then "buy" coffee by exchanging cash for coffee
    buy_demo = ["go south", "pickup scrap paper", "inventory", "throw out scrap paper", "inventory", "go east",
                "go east", "buy coffee", "inventory"]
    expected_log = [1, 2, 2, 2, 3, 4]
    buy_demo = AdventureGameSimulation('game_data.json', 1, buy_demo)
    buy_demo.run()
    assert expected_log == buy_demo.get_id_log()

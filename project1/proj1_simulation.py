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
from adventure import AdventureGame, use_command
from game_entities import Command, Location, Item, Player


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

    # TODO: Copy/paste your code from ex1_simulation below, and make adjustments as needed
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

            if choice in item_commands:
                command = self._game.get_item(choice.split(" ")[1]).use_command
            else:
                command = location.commands[choice]
            if use_command(command, self._game, self._player, location):
                self._events.add_event(Event(location.id_num, choice, command, False))
            step_num = step_num + 1


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    # TODO: Modify the code below to provide a walkthrough of commands needed to win and lose the game
    win_walkthrough = ["go south", "pickup scrap paper"]
    expected_log = []  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your walkthrough
    win_sim = AdventureGameSimulation('game_data.json', 1, win_walkthrough)
    win_sim.run()
    # assert expected_log == win_sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = []
    expected_log = []  # Update this log list to include the IDs of all locations that would be visited
    # Uncomment the line below to test your demo
    # lose_sim = AdventureGameSimulation('game_data.json', 1, lose_demo)
    # assert expected_log == lose_sim.get_id_log()

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    # inventory_demo = [..., "inventory", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # scores_demo = [..., "score", ...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)

    # Note: You can add more code below for your own testing purposes

"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
import json
from typing import Any, Optional

from game_entities import Command, Location, Item, Player
from proj1_event_logger import Event, EventList


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the location id of the current location
        - ongoing: keeps the loop running till the moves_left > = 0
        - WIN_CONDITION: the winning condition in a list

    Representation Invariants:
        - len(_locations) > 0
        - len(_items) > 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.
    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_location_id: int
    ongoing: bool
    WIN_CONDITION: list[Any] = [1, "charger", "USB"]

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        self._locations, self._items = self._load_game_data(game_data_file)

        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], dict[str, Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['commands'])
            locations[loc_data['id']] = location_obj

        items = {}
        for item_data in data['items']:
            if 'use_command' not in item_data:
                item_obj = Item(item_data['name'], item_data['description'])
            else:
                item_obj = Item(item_data['name'], item_data['description'], item_data["command_name"],
                                item_data['use_command'])
            items[item_data['name']] = item_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item:
        """Return Item object associated with the given item name

        Preconditions:
            - item_name in self._items
        """
        return self._items[item_name]


def use_menu(option: str, the_game: AdventureGame, the_player: Player, the_game_log: EventList,
             the_location: Location) -> None:
    """ Use menu action"""
    if option == "undo":
        if game_log.is_empty():
            print("There is no events to undo")
            return
        undo_command(the_game_log.get_last_event(), the_game, the_player, the_game_log, the_location)
        return

    print("------------------------------------------------")
    if option == "look":
        print(the_location.name + ":")
        print(the_location.long_description)
    elif option == "log":
        the_game_log.display_events()
    elif option == "inventory":
        the_player.show_inventory()
    elif option == "score":
        print("Score: " + str(the_player.score))
    elif option == "quit":
        print("Quiting Game...")
        the_game.ongoing = False
    print("------------------------------------------------")


def use_command(the_command: Command, the_game: AdventureGame, the_player: Player, the_location: Location) -> bool:
    """ Use command, returns true if succesful"""
    print("------------------------------------------------")
    if the_command.command_type == 'go':
        the_game.current_location_id = the_command.next_location
        the_player.change_moves(-1)
        print("A move was used")
        print("------------------------------------------------")
        return True

    if the_command.command_type == 'buy':
        cost_item = the_game.get_item(the_command.cost)
        if not the_player.has_item(cost_item):
            print("You are missing a required item, " + cost_item.name)
            return False
        the_player.remove_item(cost_item)
    if the_command.command_type in {'pickup', 'buy'}:
        the_command.available = False
        the_command.print_command_text()
        item = the_game.get_item(the_command.item)
        the_player.give_item(item)
    elif the_command.command_type in {'talk', 'unlock'}:
        the_command.available = False
        the_command.print_command_text()

    print("------------------------------------------------")

    if the_command.score_change != 0:
        the_player.change_score(the_command.score_change)
        print("You gained " + str(the_command.score_change) + " Score")
        print("------------------------------------------------")

    if the_command.unlocked_commands is not None:
        for c in the_command.unlocked_commands:
            if the_command.command_type == 'unlock':
                the_game.get_location(the_command.unlock_location).commands[c].available = True
            else:
                the_location.commands[c].available = True
    return True


def undo_command(prev_event: Event, the_game: AdventureGame, the_player: Player, the_game_log: EventList,
                 the_location: Location) -> None:
    """Undo previous commmand"""
    prev_command = prev_event.command
    prev_command.available = True
    print("Undoing: " + prev_event.command_name)
    if prev_event.new_loc:
        the_game.get_location(prev_event.loc_id_num).visited = False
    if new_location:
        the_location.visited = False
    if prev_command.command_type == 'go':
        the_game.current_location_id = prev_event.loc_id_num
        the_player.change_moves(1)
    elif prev_command.command_type == 'pickup':
        item = the_game.get_item(prev_command.item)
        the_player.remove_item(item)
    elif prev_command.command_type == 'buy':
        cost_item = the_game.get_item(prev_command.cost)
        the_player.give_item(cost_item)

        item = the_game.get_item(prev_command.item)
        the_player.remove_item(item)

    the_player.change_score(prev_command.score_change * -1)
    if prev_command.unlocked_commands is not None and location is not None:
        for c in prev_command.unlocked_commands:
            if prev_command.command_type == 'unlock':
                the_game.get_location(prev_command.unlock_location).commands[c].available = False
            else:
                the_location.commands[c].available = False
    the_game_log.remove_last_event()
    return


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
    player = Player()
    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    print("================================================")
    while game.ongoing:

        location = game.get_location()
        new_location = False

        print(location.name + ":")
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True
            new_location = True

        win_con_loc = game.WIN_CONDITION[0]
        win_con_item1, win_con_item2 = game.get_item(game.WIN_CONDITION[1]), game.get_item(game.WIN_CONDITION[2])
        if location.id_num == win_con_loc and player.has_item(win_con_item1) and player.has_item(win_con_item2):
            location.commands["submit project"].available = True

        print("======================================")
        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        available_commands = [c for c in location.commands if location.commands[c].available]
        item_commands = [item.command_name for item in player.get_inventory() if item.use_command is not None]

        for action in available_commands:
            print("-", action)
        for action in item_commands:
            print("-", action)

        print("Moves Left: ", player.moves_left)
        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in available_commands and choice not in menu and choice not in item_commands:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        if choice == "submit project":
            game.ongoing = False

        if choice in menu:
            # Handle menu actions
            use_menu(choice, game, player, game_log, location)
        else:
            # Handle non-menu actions
            if choice in item_commands:
                command = game.get_item(choice.split(" ")[1]).use_command
            else:
                command = location.commands[choice]
            if use_command(command, game, player, location):
                game_log.add_event(Event(location.id_num, choice, command, new_location))

        print("================================================")

        if player.moves_left == 0:
            print("You ran out of moves! \nThe project went unsubmitted and you recieved a 0% :( ......")
            game.ongoing = False

    print("----- GAME FINISHED -----")
    print("Score: " + str(player.score))

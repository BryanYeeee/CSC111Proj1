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
from typing import Optional

from game_entities import Command, Location, Item, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TODO add descriptions of public instance attributes as needed

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.
    _locations: dict[int, Location]
    _items: dict[str, Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
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
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        for item_data in data['items']:
            if item_data['use_command'] == "":
                item_obj = Item(item_data['name'], item_data['description'])
            else:
                item_obj = Item(item_data['name'], item_data['description'], item_data['use_command'])
            items[item_data['name']] = item_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]

    def get_item(self, item_name: str) -> Item:
        """Return Item object associated with the given item name

        Preconditions:
            - item_name in self._items
        """
        return self._items[item_name]


def use_menu(choice: str, game: AdventureGame, player: Player, game_log: EventList):
    """ Use menu action
    """
    if choice == "undo":
        if game_log.is_empty():
            print("There is no events to undo")
            return
        undo_command(game_log.get_last_event(), game, player, game_log)
        return

    print("------------------------------------------------")
    if choice == "look":
        print(location.name + ":")
        print(location.long_description)
    elif choice == "log":
        game_log.display_events()
    elif choice == "inventory":
        player.show_inventory()
    print("------------------------------------------------")


def use_command(command: Command, game: AdventureGame, player: Player) -> bool:
    """ Use command, returns true if succesful
    """
    if command.command_type == 'go':
        game.current_location_id = command.next_location
        return True

    print("------------------------------------------------")

    if command.command_type == 'buy':
        cost_item = game.get_item(command.cost)
        if not player.has_item(cost_item):
            print("You are missing a required item, " + cost_item.name)
            return False
        player.remove_item(cost_item)
    if command.command_type == 'pickup' or command.command_type == 'buy':
        command.available = False
        command.print_command_text()
        item = game.get_item(command.item)
        player.give_item(item)
    elif command.command_type == 'talk':
        command.available = False
        command.print_command_text()

    print("------------------------------------------------")

    if command.unlocked_commands is not None:
        for c in command.unlocked_commands:  # NEED DOCSTRING FOR THIS
            location.commands[c].available = True
    return True


def undo_command(prev_event: Event, game: AdventureGame, player: Player, game_log: EventList):
    """Undo previous commmand

    """
    prev_command = prev_event.command
    prev_command.available = True
    print("Undoing: " + prev_event.command_name)
    if prev_event.new_loc:
        game.get_location(prev_event.loc_id_num).visited = False
    if new_location:
        location.visited = False
    if prev_command.command_type == 'go':
        game.current_location_id = prev_event.loc_id_num
    elif prev_command.command_type == 'pickup':
        item = game.get_item(prev_command.item)
        player.remove_item(item)
    elif prev_command.command_type == 'buy':
        cost_item = game.get_item(command.cost)
        player.give_item(cost_item)

        item = game.get_item(command.item)
        player.remove_item(item)

    if prev_command.unlocked_commands is not None:
        for c in prev_command.unlocked_commands:
            location.commands[c].available = False
    game_log.remove_last_event()
    return


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
    player = Player()
    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    print("================================================")
    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()
        new_location = False

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        print(location.name + ":")
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True
            new_location = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        available_commands = ([c for c in location.commands if location.commands[c].available] +
                              ['use ' + item.name for item in player.get_inventory() if item.use_command is not None])
        for action in available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            use_menu(choice, game, player, game_log)
        else:
            # Handle non-menu actions
            command = None
            if choice[0:3] == 'use':
                command = game.get_item(choice[4:]).use_command
                print(command.use_text)
                if command.unlocked_commands is not None:
                    for c in command.unlocked_commands:
                        location.commands[c].available = True
            else:
                command = location.commands[choice]
                if use_command(command, game, player):
                    game_log.add_event(Event(location.id_num, choice, command, new_location))

        print("================================================")

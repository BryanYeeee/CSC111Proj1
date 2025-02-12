"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Command:
    """A Command that can be called by Player. Different attributes will have values based on which command type this
    class represents

    Instance Attributes:
        - command_type: the type of command this command is
        - available: whether the command is currently executable by the player
        - score_change: integer value representing the change in score when calling this command
        - command_text: the text displayed when this command is called, None if no text will be displayed
        - next_location: the id of the location Player will move to, None if Player remains still
        - item: the name of the item added to the Player's inventory, None if the Player is not given any item
        - cost: the name of the item that is removed from the Player's inventory, None if the Player's inventory remains
        - unlocked_commands: list of strings corresponding to the newly available commands, None if no commands are unlocked

    Representation Invariants:
        - command_type in ["go", "pickup", "use", "buy", "talk", "exchange", "unlock"]
        - not command_type == "go" or next_location is not None
        - not command_type == "pickup" or item is not None
        - not command_type == "buy" or (item is not None and cost is not None)
        - not command_type == "talk" or command_text is not None
        - not command_type == "unlock" or command_text is not None
    """
    command_type: str
    available: bool
    score_change: int
    command_text: Optional[str] = None
    next_location: Optional[int] = None
    item: Optional[str] = None
    cost: Optional[str] = None
    unlock_location: Optional[int] = None
    unlocked_commands: Optional[list[str]] = None

    def __init__(self, command_type: str, result: Any, command_text: str = None, available: bool = True,
                 unlocked_commands: list[str] = None, score_change: int = 0):
        self.command_type = command_type
        self.available = available
        if self.command_type == 'go':
            self.next_location = result
        elif self.command_type == 'pickup':
            self.item = result
        elif self.command_type == 'buy':
            self.cost = result[0]
            self.item = result[1]
        elif self.command_type == "unlock":
            self.unlock_location = result

        if not (unlocked_commands == [] or unlocked_commands is None):
            self.unlocked_commands = unlocked_commands
        if not (command_text == "" or command_text is None):
            self.command_text = command_text

        self.score_change = score_change

    def print_command_text(self) -> None:
        """Prints command text"""
        if self.command_text is not None:
            print(self.command_text)


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - name: name of the item
        - description: description of the item

    Representation Invariants:
        - not command_name is None or use_command is None
    """
    name: str
    description: str
    command_name: Optional[str] = None
    use_command: Optional[Command] = None

    def __init__(self, name, description, command_name=None, use_command=None) -> None:
        """Initialize a new item.

        # TODO Add more details here about the initialization if needed
        """

        self.name = name
        self.description = description
        self.command_name = command_name
        if use_command is not None:
            self.use_command = Command(*use_command)


@dataclass
class Player:
    """The player in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - _inventory: list of Items that the Player is holding
        - score: Integer of the Player's score
        - moves_left: Integer number of moves left

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """
    _inventory: list[Item]
    score: int
    moves_left: int

    def __init__(self) -> None:
        """Initialize a new Player.

        # TODO Add more details here about the initialization if needed
        """

        self._inventory = []
        score = 0
        moves_left = 12

    def has_item(self, item: Item) -> bool:
        """Return whether the Player has an item or not"""
        return item in self._inventory

    def give_item(self, item: Item) -> None:
        """Add an Item into the Player's inventory"""
        self._inventory.append(item)
        print(item.name + ": " + item.description)
        print(item.name + " was added into your inventory.")

    def remove_item(self, item: Item):
        """Remove an Item from Player's inventory"""
        self._inventory.remove(item)
        print(item.name + " was removed from your inventory.")

    def get_inventory(self) -> list[Item]:
        """Return the inventory"""
        return self._inventory

    def show_inventory(self) -> None:
        """Prints a list of the Players inventory, along with descriptions of each item"""
        print('Inventory: ', [item.name for item in self._inventory])
        for item in self._inventory:
            print("- " + item.name + ": " + item.description)


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - name: name of this location
        - brief_description: brief description of this location
        - long_description: long description of this location
        - commands: dictionary asociating the name of a Command to the Command class. Stores the available command options
        - visited: whether or not the Player has visited this location before

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """
    id_num: int
    name: str
    brief_description: str
    long_description: str
    commands: dict[str, Command]
    visited: bool

    def __init__(self, location_id, name, brief_description, long_description, commands,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.commands = {c: Command(*commands[c]) for c in commands}
        self.visited = visited

    def set_command_available(self, command: str, available: bool):
        """Make a command unavailable or unavailable

        Preconditions:
            - command in self._available_commands
        """
        self.commands[command].available = available


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

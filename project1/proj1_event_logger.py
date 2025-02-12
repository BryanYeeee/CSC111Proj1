"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional
from game_entities import Command


# TODO: Copy/paste your ex1_event_logger code below, and modify it if needed to fit your game


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - loc_id_num: Integer id of this event's location
    - command_name: The name of the command
    - command: The Command object associated with the event
    - new_loc: Boolean value which says if this event is firstly visited
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    # NOTES:
    # This is proj1_event_logger (separate from the ex1 file). In this file, you may add new attributes/methods,
    # or modify the names or types of provided attributes/methods, as needed for your game.
    # If you want to create a special type of Event for your game that requires a different
    # set of attributes, you can create new classes using inheritance, as well.

    # TODO: Add attributes below based on the provided descriptions above.
    loc_id_num: int
    command_name: str
    command: Command
    new_loc: Optional[bool] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - # TODO add descriptions of instance attributes here
        - first: Event object representing the first game event
        - last: Event object representing the last game event

    Representation Invariants:
        - # TODO add any appropriate representation invariants, if needed
        - first.prev is None
        - last.next is None
        - last.next_command is None
    """
    first: Optional[Event] = None
    last: Optional[Event] = None

    def __init__(self) -> None:
        """Initialize a new empty event list."""

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """Display all events in chronological order."""
        if self.is_empty():
            print("No events to display")
            return
        curr = self.first
        print("Location (Before Command) | Command")
        while curr:
            if curr.new_loc:
                print(f"{curr.loc_id_num} | {curr.command_name} (New Location)")
            else:
                print(f"{curr.loc_id_num} | {curr.command_name}")
            curr = curr.next

    def is_empty(self) -> bool:
        """Return whether this event list is empty."""

        # TODO: Your code below
        return self.first is None

    def add_event(self, event: Event) -> None:
        """Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        # Hint: You should update the previous node's <next_command> as needed

        # TODO: Your code below
        cur_event = self.first
        if cur_event is None:
            self.first = event
            self.first.next = self.last
            self.last = event
            self.last.prev = self.first
            return

        event.prev = self.last
        self.last.next = event
        self.last = event

    def remove_last_event(self) -> None:
        """Remove the last event from this event list.
        If the list is empty, do nothing."""

        # Hint: The <next_command> and <next> attributes for the new last event should be updated as needed

        # TODO: Your code below
        if self.first is None:
            return
        if self.first == self.last:
            self.first = None
            self.last = None
            return
        self.last = self.last.prev
        self.last.next = None

    def get_last_event(self) -> Event:
        """ Returns the last event in this event list"""
        return self.last

    def get_id_log(self) -> list[int]:
        """Return a list of all location IDs visited for each event in this list, in sequence."""

        # TODO: Your code below
        id_list = []
        cur_event = self.first
        while cur_event is not None:
            id_list.append(cur_event.loc_id_num)
            cur_event = cur_event.next
        return id_list

    # Note: You may add other methods to this class as needed


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

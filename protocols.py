from typing import Protocol

class SeatingPlanInputGetter(Protocol):
    def get_seat_class_input(self) -> int:
        ...
    
    def get_desired_seat_number(self, desired_seat_class: int) -> int:
        ...

    def 
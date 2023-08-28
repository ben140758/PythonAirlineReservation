from typing import Protocol
import seat_plan

class SeatingPlanInputGetter(Protocol):
    def get_seat_class_input(self) -> int:
        ...
    
    def get_desired_seat_number(self, desired_seat_class: int) -> int:
        ...

class SeatingPlanClassSeatCheckerBase(Protocol):
    _seating_plan: seat_plan.SeatingPlan

    def is_current_seat_class_full(self, current_seat_class: int) -> bool:
        ...

    def is_seat_class_above_full(self, upper_seat_class: int) -> bool:
        ...

    def is_seat_class_below_full(self, lower_seat_class: int) -> bool:
        ...

    
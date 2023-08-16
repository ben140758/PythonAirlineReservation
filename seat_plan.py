import seat_plan_formatter

class SeatingPlan:
    _booked_seats: list [int]
    _class_seperation_indexes: list [int]
    _formatter = seat_plan_formatter.SeatingPlanFormatter
    TOTAL_SEATS = 90

    def __init__(self, formatter: seat_plan_formatter.SeatingPlanFormatter, *seat_classification_seperators: int):
        self._booked_seats = []
        self._class_seperation_indexes = [0, *seat_classification_seperators]
        self._formatter = formatter

    def book_seat(self, seat_number: int) -> bool:
        if self.is_seat_booked(seat_number):
            return False
        self._booked_seats.append(seat_number)
        return True
    
    @property
    def remaining_seats_per_class(self) -> list[int]:
        seats_per_class = self._get_seats_per_class()
        remaining_seats_per_class = self._discount_booked_seats(seats_per_class)
        return remaining_seats_per_class

    def _get_seats_per_class(self) -> list[int]:
        seats_per_class = []
        classes = self._class_seperation_indexes.copy()
        classes.reverse()
        for index, class_index in enumerate(classes):
            if not index:
                seats_per_class.append(self.TOTAL_SEATS - class_index)
            else:
                seats_per_class.append(classes[index - 1] - class_index)
        return seats_per_class

    def _discount_booked_seats(self, seats_per_class: list[int]) -> list[int]:
        for booked_seat_number in self._booked_seats:
            self._discount_booked_seat(seats_per_class, booked_seat_number)
        return seats_per_class

    def _discount_booked_seat(self, seats_per_class, booked_seat_number):
        classes = self._class_seperation_indexes.copy()
        classes.reverse()
        for index, seat_class_number in enumerate(classes):
            if (booked_seat_number - seat_class_number) > 0:
                seats_per_class[index] -= 1
                return seats_per_class
            
    def is_seat_booked(self, seat_number: int) -> bool:
        return seat_number in self._booked_seats

    def is_seat_in_class(self, seat_number: int, seat_class: int) -> bool:
        actual_seat_class = self.get_seat_class(seat_number)
        return actual_seat_class == seat_class

    def get_seat_class(self, seat_number: int) -> int:
        for index, class_separation_index in enumerate(self._class_seperation_indexes):
            if class_separation_index // seat_number > 0:
                return index
        return len(self._class_seperation_indexes) 
            
    def __repr__(self) -> str:
        return self._formatter.generate_seating_plan_string(self._booked_seats, self._class_seperation_indexes)
    
 
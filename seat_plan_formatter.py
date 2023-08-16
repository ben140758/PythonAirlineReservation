from abc import ABC, abstractclassmethod, abstractproperty

class SeatingPlanFormatter(ABC):
    @abstractclassmethod
    def generate_seating_plan_string(self, booked_seats, row_seperation_indexes):
        ...


class FunctionalSeatingPlanFormatter(SeatingPlanFormatter):

    def generate_seating_plan_string(self, booked_seats: list[int], row_seperation_indexes: list[int]) -> str:
        PLANE_SEAT_QUANTITY = 90
        seat_plan_string = ""
        for seat_number in range(1, PLANE_SEAT_QUANTITY + 1):
            seat_plan_string += self._get_seat_string(seat_number, booked_seats)
            seat_plan_string += self._add_newline_if_end_of_row(seat_number)
            seat_plan_string += self._add_newline_if_end_of_seat_class(seat_number, row_seperation_indexes)
        return seat_plan_string

    def _get_seat_string(self, seat_number: int, booked_seats: list[int]) -> str:
        seat_string = ""
        seat_string += self._get_seat_serial_number(seat_number, booked_seats)
        seat_string += self._add_tab_if_end_of_group(seat_number)
        return seat_string
        
    def _get_seat_serial_number(self, seat_number: int, booked_seats: list[int]) -> str:
        seat_taken = self._is_seat_booked(seat_number, booked_seats)
        if (seat_taken):
            return "[XX]"
        return f"[{str(seat_number).zfill(2)}]"

    def _is_seat_booked(self, seat_number: int, booked_seats: list[int]) -> bool:
        return seat_number in booked_seats
    
    def _add_tab_if_end_of_group(self, seat_number: int) -> str:
        SEAT_GROUP_QUANTITY = 3
        if seat_number % SEAT_GROUP_QUANTITY == 0:
            return "\t"
        return ""
    
    def _add_newline_if_end_of_row(self, seat_number: int) -> str:
        ROW_SEAT_QUANTITY = 9
        if seat_number % ROW_SEAT_QUANTITY == 0:
            return "\n"
        return ""
    
    def _add_newline_if_end_of_seat_class(self, seat_number: int, row_seperation_indexes: list[int]) -> str:
        if seat_number in row_seperation_indexes:
            return "\n"
        return ""
    

class ArraySeatingPlanFormatter(SeatingPlanFormatter):
    
    def generate_seating_plan_string(self, booked_seats: list[int], row_seperation_indexes: list[int]) -> str:
        seating_plan_array = self._get_seating_plan_array()
        for row_index, row in enumerate(seating_plan_array):
            for seat_index, seat in enumerate(row):
                seat_string = str(seating_plan_array[row_index][seat_index]).zfill(2)
                seating_plan_array[row_index][seat_index] = f"[{seat_string}]"
        seating_plan_array = self._mark_booked_seats(seating_plan_array, booked_seats)
        seating_plan_array = self._mark_class_boundaries(seating_plan_array, row_seperation_indexes)
        seating_plan_array = self._add_formatting_to_seating_plan(seating_plan_array)
        seating_plan = self._convert_to_string(seating_plan_array)
        return seating_plan
    
    def _get_seating_plan_array(self) -> list [list [int]]:
        NUMBER_OF_ROWS = 10
        SEATS_PER_ROW = 9
        seating_plan = []
        for row_number in range(NUMBER_OF_ROWS):
            row = []
            for row_seat in range(SEATS_PER_ROW):
                seats_before_row = row_number * SEATS_PER_ROW
                seat_number = row_seat + seats_before_row + 1
                row.append(seat_number)
            seating_plan.append(row)

        return seating_plan

    def _mark_booked_seats(self, seating_plan_array: list[list[int]], booked_seats: list[int]) -> list[list[int | str]]:
        NUMBER_OF_ROWS = 10
        SEATS_PER_ROW = 9
        for row_number in range(NUMBER_OF_ROWS):
            for row_seat in range(SEATS_PER_ROW):
                seating_plan_array = self._mark_seat(row_number, row_seat, seating_plan_array, booked_seats)
        return seating_plan_array

    def _mark_class_boundaries(self, seating_plan_array: list[list[int]], row_seperation_indexes: list[int]):
        NUMBER_OF_ROWS = 10
        SEATS_PER_ROW = 9
        for row_number in range(NUMBER_OF_ROWS):
            for row_seat in range(SEATS_PER_ROW):
                seating_plan_array = self._mark_class_boundary(row_number, row_seat, seating_plan_array, row_seperation_indexes)
        return seating_plan_array
    
    def _mark_seat(self, row_number: int, row_seat: int, seating_plan_array: list[list[int]], booked_seats: list[int]) -> list[list[int | str]]:
        SEATS_PER_ROW = 9
        seat_number = (row_number * SEATS_PER_ROW) + (row_seat + 1)
        if seat_number in booked_seats:
            seating_plan_array[row_number][row_seat] = "[XX]"
        return seating_plan_array

    def _mark_class_boundary(self, row_number: int, row_seat: int, seating_plan_array: list[list[int | str]], row_seperation_indexes: list[int]) -> list[list[int | str]]:
        SEATS_PER_ROW = 9
        seat_number = (row_number * SEATS_PER_ROW) + (row_seat + 1)
        if seat_number in row_seperation_indexes:
            seating_plan_array[row_number][row_seat] += "\n"
        return seating_plan_array

    def _format_seat_string(self, seat: int) -> str:
        if (seat < 10):
            return f"[0{seat}]"
        return f"[{seat}]"
    
    def _add_formatting_to_seating_plan(self, seating_plan: list[list[int | str]]) -> list[list[int | str]]:
        for index, row in enumerate(seating_plan):
            seating_plan[index] = self._add_group_separations(row)
        return seating_plan

    def _add_group_separations(self, row: list[int | str]) -> str:
        SEAT_GROUP_QUANTITY = 3
        for index in range(len(row)):
            if (index + 1) % SEAT_GROUP_QUANTITY == 0:
                row[index] = row[index] + "\t"
        return row
    
    def _convert_to_string(self, seating_plan_array: list[list[str]]) -> str:
        seating_plan_string = ""
        for row in seating_plan_array:
            seating_plan_string += ''.join(row) + "\n"
        return seating_plan_string
    
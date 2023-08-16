import inputsanitisers
import seat_plan
import protocols

class AirlineReservationFrontEnd(protocols.SeatingPlanInputGetter):
    def __init__(self, seating_plan: seat_plan.SeatingPlan,input_sanitiser: inputsanitisers.InputSanitiserFactory) -> None:
        self.current_flight = 1
        self._seating_plan = seating_plan
        #self._seating_plan.book_seat(9)
        self._input_sanitiser_factory = input_sanitiser
        self._input_sanitiser_factory.register_input_sanitiser("primitive", inputsanitisers.PrimitiveTypeInputSanitiser)
        self._input_sanitiser_factory.register_input_sanitiser("choice", inputsanitisers.ChoiceInputSanitiser)

    def get_seat_class_input(self) -> int:
        choices = {"First Class": 1, "Business Class": 2, "Economy Class": 3}
        prompt = f"---Flight {self._generate_flight_number()}--\nPlease type 1 for First Class\nPlease type 2 for Business Class\nPlease type 3 for Economy Class\n : "
        sanitiser = self._get_input_sanitiser("choice", choices=list(choices.values()))
        class_choice = None
        while not class_choice:
            class_choice = sanitiser.get_sanitised_input(int, prompt)
            if not class_choice:
                print("Please ensure you are entering a valid potential option, try again\n")
        return class_choice
        
    def _get_input_sanitiser(self, required_input_type: str, **kwargs) -> inputsanitisers.InputSanitiser:
        return self._input_sanitiser_factory.create(required_input_type, **kwargs)
    
    def _generate_flight_number(self):
        flight_number = f"FL{str(self.current_flight).zfill(2)}"
        self.current_flight += 1
        return flight_number
    
    # TODO: THIS FUNCTION
    def get_desired_seat_number(self, desired_seat_class: int) -> int:
        seats_left_in_class = self._get_seats_in_class(desired_seat_class)
        if not seats_left_in_class:
            self._does_user_want_class_change(desired_seat_class)
        manually_select_seat = self._does_user_want_seat_choice()
        #TODO is seat class full if so, auto select seat
        if manually_select_seat:
            return self._get_seat_number_from_user(desired_seat_class)

    def _get_seats_in_class(self, seat_class: int) -> int:
        remaining_seats_in_flight = self._seating_plan.remaining_seats_per_class
        remaining_seats_in_seat_class = remaining_seats_in_flight[len(remaining_seats_in_flight) - seat_class]
        return remaining_seats_in_seat_class
    
    def _does_user_want_class_change(self, current_seat_class: int) -> bool:
        is_seat_class_upgradeable = self.is_seat_class_upgradeable(current_seat_class)
        prompt = "------------\nNo seats are available in your class, would you like an upgrade in class?\n y/n "
        sanitiser = self._get_input_sanitiser("primitive")
    
    def _is_seat_class_upgradeable(self, seat_class: int) -> bool:
        ...

    def _does_user_want_seat_choice(self) -> bool:
        prompt = "------------\nWould you like to choose a seat number in your desired seating class?\n y/n "
        sanitiser = self._get_input_sanitiser("primitive")
        valid_received_input = None
        while not valid_received_input:
            valid_received_input = sanitiser.get_sanitised_input(bool, prompt)
            if valid_received_input is None:
                print("Please ensure you are entering y/n, please try again\n")
        return valid_received_input

    # TODO: REFACTOR THIS FUNCTION
    def _get_seat_number_from_user(self, desired_seat_class: int) -> int:
        print(f"------------\n{self._seating_plan}")
        prompt = "------------\nWhich seat from your chosen seating class would you like?\n : "
        sanitiser = self._get_input_sanitiser("primitive")
        desired_seat_number = None
        seat_unbooked = None
        seat_choice_in_correct_class = None
        while not desired_seat_number or not seat_unbooked or not seat_choice_in_correct_class:
            desired_seat_number = None
            desired_seat_number = sanitiser.get_sanitised_input(int, prompt)
            if not desired_seat_number:
                print("------------\nPlease enter a valid seat number and try again")
                continue
            seat_choice_in_correct_class = self._seating_plan.is_seat_in_class(desired_seat_number, desired_seat_class)
            if not seat_choice_in_correct_class:
                print("------------\nPlease ensure that the entered seat number is in your designated seat class, try again")
                continue
            seat_unbooked = not self._seating_plan.is_seat_booked(desired_seat_number)
            if not seat_unbooked:
                print("------------\nThis seat is taken, choose a different seat.")
        return desired_seat_number
    

if __name__ == "__main__":
    afe = AirlineReservationFrontEnd(inputsanitisers.PrimitiveTypeInputSanitiser())
    #print(afe.input_sanitiser.get_sanitised_input(float, "AAAAAAA\t"))
    
import frontend
import seat_plan
import seat_plan_formatter
import inputsanitisers

if __name__ == "__main__":
    seat_plan_formatter = seat_plan_formatter.FunctionalSeatingPlanFormatter()#ArraySeatingPlanFormatter()
    seating_plan = seat_plan.SeatingPlan(seat_plan_formatter, 18, 45)
    input_sanitiser = inputsanitisers.PrimitiveTypeInputSanitiser()
    #choice_sanitiser = inputsanitisers.ChoiceInputSanitiser("a", "b", "c")
    factory = inputsanitisers.InputSanitiserFactory()
    frontend = frontend.AirlineReservationFrontEnd(seating_plan, factory)
    #frontend._seating_plan.book_seat(10)
    seat_class = frontend.get_seat_class_input()
    seat_number = frontend.get_desired_seat_number(seat_class)
    print(seat_number)
    #print(frontend._generate_flight_number())
    #print(frontend._generate_flight_number())
    '''seating_plan.book_seat(50)
    seating_plan.book_seat(9)
    seating_plan.book_seat(18)
    print(seating_plan)
    print(seating_plan.remaining_seats_per_class)'''
    #print(18 + 26 + 44)
        # Get User Details1

        # Generate Flight Number
        # Get Seat Type1
        

        # Generate Seat Plan Stringawd
    #print("HELLO WORLD!")3
    
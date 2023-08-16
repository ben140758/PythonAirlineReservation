from abc import ABC, abstractmethod


class InputSanitiser(ABC):
    @abstractmethod
    def get_sanitised_input(self, return_type: any, question: str) -> any:
        ...


class InputSanitiserFactory:
    def __init__(self) -> None:
        self._input_sanitisers = {}

    def register_input_sanitiser(self, key: str, input_sanitiser: InputSanitiser) -> None:
        self._input_sanitisers[key] = input_sanitiser

    def create(self, key: str, **kwargs) -> InputSanitiser:
        input_sanitiser = self._input_sanitisers.get(key)
        if not input_sanitiser:
            raise ValueError(key)
        return input_sanitiser(**kwargs) 


class ChoiceInputSanitiser(InputSanitiser):
    def __init__(self, choices: list[str | int | float | bool]) -> None:
        self.choices = choices

    def get_sanitised_input(self, return_type: any, question: str) -> any:
        user_input = input(question)
        try:
            casted_input = return_type(user_input)
        except ValueError:
            return None
        if not casted_input in self.choices:
            return None
        return casted_input


class PrimitiveTypeInputSanitiser(InputSanitiser):
    def __init__(self):
        ...
    
    def get_sanitised_input(self, return_type: type [int | float | str | bool], question: str) -> any:
        input_functions = {
            int: self._get_sanitised_int_input,
            float: self._get_sanitised_float_input,
            str: self._get_sanitised_string_input,
            bool: self._get_sanitised_bool_input
        }
        return input_functions[return_type](question)

    def _get_sanitised_int_input(self, question: str) -> int:
        return self._get_sanitised_numeric_input(int, question)
    
    def _get_sanitised_float_input(self, question: str) -> float:
        return self._get_sanitised_numeric_input(float, question)
    
    def _get_sanitised_numeric_input(self, numeric_type: type[int | float], question: str) -> int | float:
        try:
            user_input = numeric_type(input(question))
        except ValueError:
            return None
        return user_input
    
    def _get_sanitised_string_input(self, question: str) -> str:
        user_input = input(question)
        if user_input == "":
            return None
        return user_input
    
    def _get_sanitised_bool_input(self, question: str) -> bool:
        user_input = input(question).lower()
        possible_positive_answers = ["true", "yes", "y", "1"]
        possible_negative_answers = ["false", "no", "n", "0"]
        if user_input in possible_positive_answers:
            return True
        if user_input in possible_negative_answers:
            return False
        return None
        
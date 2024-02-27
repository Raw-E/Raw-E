import datetime
from data.databases.mongodb_atlas.database_operations import state_of_being_related as state_of_being_database_operations

class StateOfBeingActions:
    """
    Manages actions related to tracking the state of being of a user.

    This class provides functionalities to track and record a user's state of being, including both verbal descriptions and numerical ratings.

    Attributes:
        user_name (str): The name of the user whose state of being is being tracked.
    """

    def __init__(self, user_name):
        """
        Initializes the StateOfBeingActions class with the user's name.

        Parameters:
            user_name (str): The name of the user.
        """
        self.user_name = user_name

    def track_state_of_being(self):
        """
        Tracks the user's state of being by collecting verbal and numerical inputs.

        Asks the user for a verbal description of their state of being and a numerical rating on a scale of 0 to 10.
        Validates the numerical input and stores the data in the database.

        Exceptions:
            ValueError: If the numerical input is not between 0 and 10.
        """
        verbal_input = input("What was your average state of being since you last tracked? If this is your first time tracking just state your current state of being: ")
        numerical_input = input("On a scale of 0 to 10, how would you rate your current state of being? (0 being the worst you've ever experienced, 10 being the best you've ever experienced): ")
        
        # Validate and convert numerical input to a float
        try:
            numerical_input = float(numerical_input)
            if numerical_input < 0 or numerical_input > 10:
                raise ValueError("The number must be between 0 and 10.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            return
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state_data = {
            "user_name": self.user_name,
            "timestamp": current_time,
            "verbal_state": verbal_input,
            "numerical_rating": numerical_input
        }
        
        state_of_being_database_operations.add_state_of_being(state_data)
        print("State of being tracked successfully.")
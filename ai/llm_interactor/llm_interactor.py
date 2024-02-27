import os
from typing import Optional
from openai import OpenAI

class LLMInteractor:
    """
    A class to interact with OpenAI's API for generating model responses.

    This class encapsulates the functionality to communicate with OpenAI's API,
    allowing for easy generation of responses from various models based on input messages.

    Attributes:
        client (OpenAI): An instance of the OpenAI client used to make API requests.
    """

    def __init__(self):
        """
        Initializes the LLMInteractor by creating an instance of the OpenAI client.
        This client will be used to interact with OpenAI's API for generating model responses.
        """
        self.client = OpenAI()

    def get_response(self, messages: list, model: str = "gpt-4-0125-preview", temperature: float = 0.7, max_tokens: int = 4000) -> Optional[str]:
        """
        Retrieves a response from the specified model based on the input messages.

        Sends a request to the OpenAI API using the provided parameters to generate a text response.
        The response is tailored based on the input messages, with options to specify the model,
        control the randomness of the response through temperature, and limit the response length with max_tokens.

        Parameters:
            messages (list): A list of message dictionaries, where each dictionary has a 'role' key ('user' or 'assistant')
                             and a 'content' key with the message text.
            model (str): The identifier of the model to use for generating responses. Defaults to "gpt-4-0125-preview".
            temperature (float): Controls the randomness in the response generation, with a range from 0 to 1.
                                 A lower temperature results in less random responses. Defaults to 0.7.
            max_tokens (int): The maximum number of tokens (words and punctuation) to generate in the response. Defaults to 4000.

        Returns:
            Optional[str]: The generated response text from the model as a string, or None if an error occurs during the API call.
        """
        try:
            response = self.client.chat.completions.create(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            
            # Extracts and returns the content of the first message in the response.
            # Assumes the response is structured with at least one choice containing a message.
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
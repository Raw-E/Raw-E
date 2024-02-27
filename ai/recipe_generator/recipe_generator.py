import json
import re
import random
import os
from nltk.corpus import words
from ai.llm_interactor.llm_interactor import LLMInteractor

# Ensure nltk 'words' dataset is downloaded for word selection
import nltk
nltk.download('words', quiet=True)

class RecipeGenerator:
    """
    A class to generate and score recipes using a language model.

    This class utilizes a language model to generate recipes based on a random inspiration word
    and a specified recipe type. It also scores the recipes based on health and taste criteria.

    Attributes:
        word_list (list): A list of words from the nltk corpus.
        llm_interactor (LLMInteractor): An instance to interact with the language model.
    """

    def __init__(self):
        """
        Initializes the RecipeGenerator with a list of words and an LLMInteractor instance.
        """
        self.word_list = words.words()
        self.llm_interactor = LLMInteractor()

    def get_recipe_generation_prompt(self):
        """
        Generates a prompt for recipe generation based on a random inspiration word and recipe type.

        Returns:
            str: A prompt string for generating a recipe.
        """
        inspiration_word = random.choice(self.word_list)
        recipe_type = random.choice(["vegan", "vegan and raw"])
        return f'Generate a {recipe_type} recipe with ingredients and steps. Use the word "{inspiration_word}" to shape the recipe name and recipe (the recipe name should still be understandable). Then score the recipe from 1 to 100 (use up to 1 decimal) on health and taste. Your output should in this JSON format: {{"recipe": {{"name": "...", "ingredients": ["i1", "i2", "..."], "instructions": ["i1", "i2", "..."]}}, "healthScore": #, "tasteScore": #}}'

    def generate_and_score_recipe(self):
        """
        Generates a recipe and scores it based on the generated prompt.

        Returns:
            tuple: A tuple containing the generated recipe in JSON format and its score, or (None, None) if an error occurs.
        """
        recipe_generation_prompt = self.get_recipe_generation_prompt()
        messages = [{"role": "user", "content": recipe_generation_prompt}]
        recipe_response = self.llm_interactor.get_response(messages, temperature=0.8)
        cleaned_recipe_response = re.sub(r'^.*?({.*}).*$', r'\1', recipe_response, flags=re.DOTALL)

        try:
            recipe_json = json.loads(cleaned_recipe_response)
        except json.JSONDecodeError as e:
            print(f"Failed to decode the recipe response into JSON: {e}")
            return None, None

        score = self.score_recipe(recipe_json)
        return recipe_json, score

    def score_recipe(self, recipe):
        """
        Scores the recipe based on predefined evaluation criteria.

        Args:
            recipe (dict): The recipe in JSON format to be scored.

        Returns:
            float: The total score of the recipe, or None if an error occurs.
        """
        try:
            with open('ai/recipe_generator/recipe_evaluation_dimensions.json', 'r') as file:
                evaluation_criteria = json.load(file)
        except FileNotFoundError:
            print("Evaluation criteria file not found.")
            return None

        health_score = evaluation_criteria['healthWeight'] * recipe['healthScore']
        taste_score = evaluation_criteria['tasteWeight'] * recipe['tasteScore']

        total_score = health_score + taste_score
        
        return total_score

    # Additional methods for ranking, feedback collection, etc., can be added here
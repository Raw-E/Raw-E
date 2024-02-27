# Import necessary modules and classes
from ai.recipe_generator.recipe_generator import RecipeGenerator
from user_actions.state_of_being_actions import StateOfBeingActions

def generate_multiple_recipes(recipe_generator, n=10):
    """
    Generates multiple recipes using the provided recipe generator.

    Parameters:
    - recipe_generator: An instance of RecipeGenerator used to generate recipes.
    - n (int): The number of recipes to generate. Defaults to 10.

    Returns:
    - list: A list of tuples, each containing a recipe and its score.
    """
    recipes = []
    for _ in range(n):
        recipe, score = recipe_generator.generate_and_score_recipe()
        recipes.append((recipe, score))
    return recipes

def rank_and_display_recipes(recipes):
    """
    Ranks the generated recipes by score and displays them to the user.

    Parameters:
    - recipes (list): A list of tuples, each containing a recipe and its score.
    """
    ranked_recipes = sorted(recipes, key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=True)

    while True:
        print("\nTop recipes based on score:")
        for index, (recipe, score) in enumerate(ranked_recipes, start=1):
            if recipe is None or recipe.get('recipe') is None:
                print(f"{index}. Recipe data is missing - Score: {score}")
            else:
                print(f"{index}. {recipe['recipe']['name']} - Score: {score}")

        choice = input("\nEnter the number of the recipe you want to examine in more detail, or 'q' to quit: ")
        if choice.isdigit():
            selected_index = int(choice) - 1
            if 0 <= selected_index < len(ranked_recipes):
                selected_recipe = ranked_recipes[selected_index][0]
                display_recipe_details(selected_recipe)
                prompt_save_recipe(selected_recipe)
            else:
                print("Invalid selection.")
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid input. Please enter a valid number or 'q' to quit.")

def display_recipe_details(recipe):
    """
    Displays the details of a selected recipe.

    Parameters:
    - recipe (dict): The recipe to display.
    """
    print(f"\nName: {recipe['recipe']['name']}")
    print("Ingredients:")
    for ingredient in recipe['recipe']['ingredients']:
        print(f"- {ingredient}")
    print("Instructions:")
    for instruction in recipe['recipe']['instructions']:
        print(f"- {instruction}")

def prompt_save_recipe(recipe):
    """
    Prompts the user to save the recipe and handles their response.

    Parameters:
    - recipe (dict): The recipe the user may choose to save.
    """
    save_choice = input("\nDo you want to save this recipe? (y/n): ")
    if save_choice.lower() == 'y':
        save_recipe_to_file(recipe)

def save_recipe_to_file(recipe):
    """
    Saves the selected recipe to a file.

    Parameters:
    - recipe (dict): The recipe to save.
    """
    with open("data/recipes/saved_preliminary_recipes.txt", "a") as file:
        file.write(f"Name: {recipe['recipe']['name']}\n")
        for ingredient in recipe['recipe']['ingredients']:
            file.write(f"- {ingredient}\n")
        for instruction in recipe['recipe']['instructions']:
            file.write(f"- {instruction}\n")
        file.write("\n---\n\n")
    print("Recipe saved successfully.")

if __name__ == "__main__":
    # Main program loop for user interaction
    while True:
        print("\nMain Menu")
        print("1. Generate Recipes")
        print("2. State Your State of Being")
        print("3. Exit")
        choice = input("Please choose an option (1-3): ")

        if choice == '1':
            n = input("How many recipes would you like to generate? ")
            if n.isdigit():
                n = int(n)
                recipe_generator = RecipeGenerator()
                recipes = generate_multiple_recipes(recipe_generator, n)
                rank_and_display_recipes(recipes)
            else:
                print("Please enter a valid number.")
        elif choice == '2':
            StateOfBeingActions("Raw-E").track_state_of_being()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
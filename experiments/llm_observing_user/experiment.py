from openai import OpenAI
import os
import json

# Initialize the OpenAI client
client = OpenAI()

# Global list to store the conversation history
conversation_history = []

# Counter for tracking messages since the last observation
messages_since_last_observation = 0

def analyze_interaction():
    """
    Analyzes the conversation history to make an observation about the user.

    This function sends the conversation history to the LLM with a specific
    instruction to observe the user's behavior or characteristics, then stores
    the observation in a file.

    Returns:
        dict: A dictionary containing the observation about the user.
    """
    global messages_since_last_observation
    
    # Prepare the analysis prompt as a system message
    analysis_prompt = "Make an observation about the user based on the conversation history."
    
    # Temporarily add the analysis prompt to the conversation for this analysis only
    temp_conversation_history = conversation_history.copy()
    temp_conversation_history.append({"role": "system", "content": analysis_prompt})
    
    # Call the LLM to analyze the conversation history and make observations
    analysis_completion = client.chat.completions.create(
        messages=temp_conversation_history,
        model="gpt-4-0125-preview",
    )
    
    # Extract the observation from the response
    observation = analysis_completion.choices[0].message.content
    
    # Store the observation in a file
    with open("llm_observations_of_user.txt", "a") as file:
        file.write(observation + "\n")
    
    # Reset the counter since an observation has been made
    messages_since_last_observation = 0
    
    return {"observation": observation}

try:
    while True:
        # Prompt the user for input
        user_input = input("You: ")
        
        # Check for exit command
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        # Add the user's input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Increment the counter for messages since the last observation
        messages_since_last_observation += 1

        # Generate a response from the LLM based on the conversation history
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model="gpt-4-0125-preview",
        )
        response = chat_completion.choices[0].message.content

        # Add the LLM's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response})

        # Display the LLM's response
        print("LLM:", response)

        # Optionally, analyze the interaction and make observations every 2 messages
        if messages_since_last_observation >= 2:
            observation = analyze_interaction()  # This function now uses the global conversation_history
            print("Observation:", observation['observation'])

except KeyboardInterrupt:
    # Handle manual script termination
    print("\nSession ended.")
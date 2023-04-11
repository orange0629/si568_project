import openai

# Set up OpenAI API Key here
openai.api_key = "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"


class DarkMist:
    """
        Basic class holding the game. Contains all chat logs and game related functions.
    """

    # Container of all chat logs
    messages = []
    
    # Basic system prompt about the game rule and settings
    game_rule_message = {
         "role": "system", "content": "You are playing a text adventure game with me. " 
         "I lost all his memory and wake up in a dark mist. " 
         "There's a princess imprisoned in a castle by the devil, " 
         "and the ultimate goal of the game is to beat the devil " 
         "and rescure the princess. However, I has limited ability at first, " 
         "and I should first hone himself, find partners, find weapons, " 
         "get information about the world before I go to the castle. " 
         "You must wait for reply from me in each step about what I want to do next. " 
         "My decision must be reasonable. Don't give options to me. The game should be difficult. " 
         "Some decisions should be harmful, which can lead me to be dead and game over. " 
         "I can also choose to talk with NPCs like villagers, witchs, knights, or any other reasonable NPCs."}
    
    def __init__(self):
        """
            Initialize the message container by the game rule system message

            Parameters: 
                self (class DarkMist): The instance calling the function
            
            Returns:
                None
        """
        self.messages = [self.game_rule_message]
        
    def get_reply(self):
        """
            Get the reply from the chatbot based on the current message container
            
            Parameters: 
                self (class DarkMist): The instance calling the function
            
            Returns:
                reply (String): The reply message from the chatbot
        """
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        reply = chat.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply
    
    def add_player_message(self, input_message):
        """
            Add a user message to the message container
            
            Parameters: 
                self (class DarkMist): The instance calling the function
                input_message (String): The new message to add to the message container
            
            Returns:
                None
        """
        self.messages.append({"role": "user", "content": input_message})

    def regret_message(self):
        """
            Go back to the player's last decision in game
            
            Parameters: 
                self (class DarkMist): The instance calling the function
            
            Returns:
                None
        """
        if((len(self.messages) >= 3) and (self.messages[-1]["role"] == "assistant")):
            # Remove the last two messages in the container
            self.messages = self.messages[0: -2]
            print("System -> Success! You are now back to this step:")
            print("System ->", self.messages[-1]["content"])
        else:
            print("System -> Failed to go back your last decision.")

    def print_help_text(self):
        """
            Print the complete list of available commands
            
            Parameters: 
                self (class DarkMist): The instance calling the function
            
            Returns:
                None
        """
        print("System -> \"/start\": Restart the game whereever you are.")
        print("System -> \"/regret\": Go back to your last decision.")
        print("System -> \"/quit\": Exit the game.")




if __name__ == '__main__':

    # Initialize the instance of game
    main_game = DarkMist()

    print("\nSystem -> Welcome to Dark Mist, a text adventure game made by Lechen Zhang. Type \"/start\" to start the game or \"/quit\" to leave!")
    print("System -> You can type \"/help\" for a complete list of available commands!")

    # Get player's input
    user_input = input("\nUser -> ")

    # Only quit when user input is /quit
    while(user_input != "/quit"):

        if(user_input == "/help"):
            main_game.print_help_text()

        elif(user_input == "/start"):
            main_game.__init__()
            print("System ->", main_game.get_reply())

        elif(user_input == "/regret"):
            main_game.regret_message()

        elif((len(main_game.messages) > 1) and ('/' not in user_input)):

            # Add player's input to the message container when game is activated
            main_game.add_player_message(user_input)

            # Print the reply from the chatbot
            print("System ->", main_game.get_reply())

        else:
            print("Invalid command! Type \"/help\" for a complete list of available commands!")
        
        # Get player's new input
        user_input = input("\nUser -> ")
        
                


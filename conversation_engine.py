"""
Conversational Engine - Talk with Gemini about anything
1. Create new chat
2. Method inputting user action
3. Method outputting model response
"""
from google import genai
# from google.genai import types
import os

class ConversationEngine:
    # Initialize client object and chat text file based on path provided
    def __init__ (self, ai_model, API_KEY, chat_path, system_chat_instructions, model_temperature=0.7):
        # initializing variables and model client object
        self.chat_path = chat_path
        self.ai_model = ai_model
        self.model_temperature = model_temperature
        self.client = genai.Client(api_key= API_KEY)

        # Creating directory if it doesn't exist
        directory = os.path.dirname(chat_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Writing system instruction to chat file
        if not(os.path.exists(path=chat_path)):
            with open(chat_path, 'w') as file:
                file.write("*__System__*: "+ system_chat_instructions + '\n\n')
        
    # Modify chat file according to User action
    def UserInputToFile(self, chat_file_path_flag, user_chat_prompt='', chat_file_path=''):
        '''
        chat_file_path_flag values -> False, True
        False -> Normal text prompt for Model
        True -> Add chat file contents as inputted prompt

        chat_file_path -> if equal to 'all' then add contents of all sibling files as inputted prompt
        '''
        if not chat_file_path_flag:
            if(user_chat_prompt):
                # Appending user prompt to current file
                with open(self.chat_path, 'a') as file:
                        file.write("*__User__*: " + user_chat_prompt + '\n\n')
            else:
                raise "user_chat_prompt cant be empty!"
        else:
            if(chat_file_path):
                contents = '```----------Past Chats Start-----------\n\n'
                
                if(chat_file_path.lower() == 'all'):
                    curr_dir = os.path.dirname(self.chat_path)
                    curr_file = os.path.basename(self.chat_path)
                    # add contents of sibling files as inputted prompt
                    for chat_file in os.listdir(curr_dir):
                        if(chat_file!= curr_file):
                            with open(curr_dir+'/'+chat_file, 'r') as file:
                                contents += f"-----{chat_file}-----\n\n" + file.read() + '\n\n'
                    
                else:
                    # add contents of provided file as inputted prompt
                    with open(chat_file_path, 'r') as file:
                        contents += file.read() + '\n\n'
                
                contents += '----------Past Chats End-----------```'
                
                # inserting tabspace before all lines of contents
                content_lines_list = contents.split('\n')
                for i in range(len(content_lines_list)):
                    content_lines_list[i] = f'\t{content_lines_list}'

                # Writing contents to current chat file
                with open(self.chat_path, 'a') as file:
                    file.write("*__User__*: Below are the contents of past conversations between us. Consider it for future answers.\n" + '\n'.join(contents) + '\n\n')
            else:
                raise "chat_file_path cant be empty!"
            
    # Modify chat file with AI response
    def AIOutputToFile(self) -> str:
        # Get AI response for current chat file
        with open(self.chat_path, 'r') as file:
            contents = file.read()
        response = self.client.models.generate_content(
            model = self.ai_model,
            contents = contents,
            # config=types.GenerateContentConfig(
            #     temperature=self.model_temperature,
            # ),
        )
        
        # Add response to chat file
        with open(self.chat_path, 'a') as file:
            file.write("*__Assistant__*: " + response.text + '\n\n')

        # return response
        return response.text
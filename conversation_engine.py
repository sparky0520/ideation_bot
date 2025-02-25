"""
Conversational Engine - Talk with Gemini about anything
1. Create new chat
2. Method inputting user action
3. Method outputting model response
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import os

# MODEL INITIALIZATION

# defining quantization config
bnb_config = BitsAndBytesConfig(
    llm_int8_enable_fp32_cpu_offload=True,
    load_in_8bit=True,  # 8 bit quantization
)

# model_name = "microsoft/Phi-3.5-mini-instruct"
model_name = "microsoft/phi-2"

# Loading tokenizer - converts text to numbers/tokens for model to compute and predict
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Loading model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # offloads excess layers to cpu if needed
    quantization_config=bnb_config  # efficient quantization
)

class ConversationEngine:
    # Initialize new chat
    def __init__ (self, chat_path, system_chat_instructions, temperature = 0.7):
        self.chat_path = chat_path
        self.model_temperature = temperature

        # Creating directory if it doesn't exist
        directory = os.path.dirname(chat_path)
        os.makedirs(directory, exist_ok=True)
        
        # Writing system instruction to chat file if it doesn't exists
        if not(os.path.exists(chat_path)):
            with open(chat_path, 'w', encoding='utf-8') as file:
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
                with open(self.chat_path, 'a', encoding='utf-8') as file:
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
                            with open(curr_dir+'/'+chat_file, 'r', encoding='utf-8') as file:
                                contents += f"-----{chat_file}-----\n\n" + file.read() + '\n\n'
                    
                else:
                    # add contents of provided file as inputted prompt
                    with open(chat_file_path, 'r', encoding='utf-8') as file:
                        contents += file.read() + '\n\n'
                
                contents += '----------Past Chats End-----------```'
                
                # inserting tabspace before all lines of contents
                content_lines_list = contents.split('\n')
                for i in range(len(content_lines_list)):
                    content_lines_list[i] = f'\t{content_lines_list[i]}'

                # Writing contents to current chat file
                with open(self.chat_path, 'a', encoding='utf-8') as file:
                    file.write("*__User__*: Below are the contents of past conversations between us. Consider it for future answers.\n" + '\n'.join(contents) + '\n\n')
            else:
                raise "chat_file_path cant be empty!"
            
    # Modify chat file with AI response
    def AIOutputToFile(self) -> str:
        # Get AI response for current chat file
        with open(self.chat_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        
        inputs = tokenizer(contents, return_tensors='pt').to(model.device)
        with torch.no_grad():
            output = model.generate(**inputs, max_new_tokens=150, temperature=0.7, do_sample=True)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Add response to chat file
        with open(self.chat_path, 'a', encoding='utf-8') as file:
            file.write("*__Assistant__*: " + response + '\n\n')

        # return response
        return response
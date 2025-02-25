from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# MODEL INITIALIZATION
model_name = "tiiuae/Falcon3-1B-Instruct"

# Loading tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Loading model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # Offloads layers if needed
    torch_dtype=torch.float16,
)

class ConversationEngine:
    def __init__(self, chat_path, system_chat_instructions, temperature=0.7):
        self.chat_path = chat_path
        self.model_temperature = temperature

        # Create chat directory if it doesn't exist
        directory = os.path.dirname(chat_path)
        os.makedirs(directory, exist_ok=True)
        
        # Write system instructions if chat file doesn't exist
        if not os.path.exists(chat_path):
            with open(chat_path, 'w', encoding='utf-8') as file:
                file.write(f"### System Instructions:\n{system_chat_instructions}\n\n")

    # Append user input to chat file
    def UserInputToFile(self, chat_file_path_flag, user_chat_prompt='', chat_file_path=''):
        if not chat_file_path_flag:
            if user_chat_prompt:
                with open(self.chat_path, 'a', encoding='utf-8') as file:
                    file.write(f"### User:\n{user_chat_prompt}\n\n")
            else:
                raise ValueError("user_chat_prompt cannot be empty!")
        else:
            if chat_file_path:
                contents = "\n### Past Chats:\n"

                if chat_file_path.lower() == 'all':
                    curr_dir = os.path.dirname(self.chat_path)
                    curr_file = os.path.basename(self.chat_path)
                    for chat_file in os.listdir(curr_dir):
                        if chat_file != curr_file:
                            with open(os.path.join(curr_dir, chat_file), 'r', encoding='utf-8') as file:
                                contents += f"\n--- {chat_file} ---\n" + file.read() + '\n'
                else:
                    with open(chat_file_path, 'r', encoding='utf-8') as file:
                        contents += file.read() + '\n'

                # Truncate if too long
                if len(contents) > 1000:
                    contents = contents[-1000:]

                # Append past chat reference to current chat file
                with open(self.chat_path, 'a', encoding='utf-8') as file:
                    file.write(f"### User:\nHere are past conversations for reference:\n{contents}\n\n")
            else:
                raise ValueError("chat_file_path cannot be empty!")

    # Generate AI response and update chat file
    def AIOutputToFile(self) -> str:
        # Read and truncate chat history if needed
        with open(self.chat_path, 'r', encoding='utf-8') as file:
            contents = file.read()

        # Keep only the last 1000 characters for context
        if len(contents) > 1000:
            contents = contents[-1000:]

        # Prepare input for model
        prompt = contents.strip() + "\n\n### Response:\n"
        inputs = tokenizer(prompt, return_tensors='pt').to(model.device)

        # Generate AI response
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.2,
                do_sample=True,
                num_return_sequences=1
            )

        response = tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # Append response to chat file
        with open(self.chat_path, 'a', encoding='utf-8') as file:
            file.write(f"### Assistant:\n{response}\n\n")

        return response

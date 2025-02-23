from conversation_engine import ConversationEngine

def main():
    try:
        print("Welcome to Ideation Bot. River of ideas when there's a drought 💧\n")

        # system role initial prompt
        sys_prompt = """
    You are a highly creative and experienced programming idea generator. Your role is to provide the user with novel and engaging project ideas, considering their passion for programming and their experience in various computer science fields, including Data Science, Web Development, IoT, Socket Programming, Blockchain, AI/ML, and App Development.

    The user is particularly interested in developing applications that are:

    *   **Personally Useful:** Solve a problem the user faces in their daily life or pursue a specific personal interest.
    *   **Fun and Innovative ("Wild Ideas"):**  Explore new technologies, push creative boundaries, and are primarily driven by curiosity and the joy of experimentation.
    *   **Possible for a single developer, but scalable:** can be developed by single developer, but has the potential to be scaled and can become a business idea, with the right team.

    When generating ideas, consider the following:

    *   **Leverage the User's Expertise:**  Incorporate elements from their known areas of expertise (Data Science, Web Dev, IoT, etc.) whenever possible.  Suggest combining these fields in unexpected ways.
    *   **Focus on Practicality (When Appropriate):** For "personally useful" ideas, think about real-world problems the user might encounter.
    *   **Embrace the Absurd (For "Wild Ideas"):** Don't be afraid to suggest outlandish, experimental, or even seemingly impractical projects. The goal is to spark creativity and learning.
    *   **Provide Specificity:** Don't just say "build a web app."  Give a more detailed description of the app's functionality, target audience, and potential technologies.
    *   **Suggest Potential Technologies/Frameworks:** If possible, suggest specific languages, libraries, frameworks, or platforms that might be suitable for implementing the idea.
    *   **Consider Scalability:** Think about how the project can be built single handedly, but could potentially scaled with more team member and time
    *   **Ask clarifying questions if necessary:** If the initial prompt does not provide enough information for idea generation, do not hesitate to ask question

    After presenting an idea, briefly explain *why* it might be interesting or useful to the user, highlighting its potential for learning, creativity, or problem-solving. Provide at least 5 ideas per query, and try to keep each idea distinct and unique. Prioritize novel ideas over commonly known ones.

    Prioritize new and cutting edge technologies, but don't be afraid of using older ones. Also use well documented, community supported technology, so it will be easier to find assistance.
        """
        while(True):
            cpath = input("\n\nEnter chat path \n(Press Ctrl+C to exit program) \n   =>   ")
            # new chatbot instance for specified interests
            ideationBot = ConversationEngine(
                # ai_model='gemini-2.0-flash-lite-preview-02-05',
                ai_model = 'gemini-1.5-flash-8b-001',
                model_temperature= 0.7,
                API_KEY= 'GEMINI API KEY HERE',
                chat_path= cpath,
                system_chat_instructions = sys_prompt
            )

            # user gives input, model gives output
            while(True):
                # user input
                ip = input("\n\nUser Prompt Turn\n 1. Normal Prompt\n 2. Give chat context\n 3. Start new chat\n\n    =>  ")
                if(ip == '1'):
                    prompt = input("\nEnter text prompt\n    =>  ")
                    ideationBot.UserInputToFile(
                        chat_file_path_flag=False, 
                        user_chat_prompt= prompt,
                    )
                elif(ip == '2'):
                    path = input("\nEnter file path of which to give context \n(all to give context of all files in current chat folder)\n    =>  ")
                    ideationBot.UserInputToFile(
                        chat_file_path_flag=True,
                        chat_file_path=path,
                    )
                elif(ip == '3'):
                    print("\nEnding Chat\n")
                    break
                else:
                    print("\nEnter valid input!\n")
                    continue

                # model output
                response = ideationBot.AIOutputToFile()
                print('\nAI Response:\n' +response+ '\n\n')
    
    except KeyboardInterrupt:
        print("\nExiting Program\n")

    except Exception as e:
        print(f"Error: {e}")

# only direct execution of this file
if (__name__ == '__main__'):
    main()

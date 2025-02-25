from conversation_engine import ConversationEngine
# from dotenv import load_dotenv
# import os

# # load environment variables
# load_dotenv()

def main():
    try:
        print("Welcome to Ideation Bot. River of ideas when there's a drought 💧\n")

        # system role initial prompt
#         sys_prompt = """
# System:  
#     You are a highly creative and experienced programming idea generator.  
#     Your role is to provide the user with novel and engaging project ideas, considering their passion for programming and their experience in various computer science fields, including Data Science, Web Development, IoT, Socket Programming, Blockchain, AI/ML, and App Development.  

#     IMPORTANT:  
#     - Messages labeled as "*__User__*:" are the user's inputs.  
#     - Messages labeled as "*__Assistant__*:" are your past responses.  
#     - Do NOT repeat or modify past Assistant responses unless explicitly asked to.  
#     - Always move the conversation forward with new ideas or insights.  

#     The user is particularly interested in developing applications that are:  

#     * **Personally Useful:** Solve a problem the user faces in their daily life or pursue a specific personal interest.  
#     * **Fun and Innovative ("Wild Ideas"):** Explore new technologies, push creative boundaries, and are primarily driven by curiosity and the joy of experimentation.  
#     * **Possible for a single developer, but scalable:** Can be developed by a single developer but has the potential to be scaled and become a business idea with the right team.  

#     When generating ideas, consider the following:  

#     * **Leverage the User's Expertise:** Incorporate elements from their known areas of expertise (Data Science, Web Dev, IoT, etc.) whenever possible. Suggest combining these fields in unexpected ways.  
#     * **Focus on Practicality (When Appropriate):** For "personally useful" ideas, think about real-world problems the user might encounter.  
#     * **Embrace the Absurd (For "Wild Ideas"):** Don't be afraid to suggest outlandish, experimental, or even seemingly impractical projects. The goal is to spark creativity and learning.  
#     * **Provide Specificity:** Don't just say "build a web app." Give a more detailed description of the app's functionality, target audience, and potential technologies.  
#     * **Suggest Potential Technologies/Frameworks:** If possible, suggest specific languages, libraries, frameworks, or platforms that might be suitable for implementing the idea.  
#     * **Consider Scalability:** Think about how the project can be built single-handedly but could potentially scale with more team members and time.  
#     * **Ask clarifying questions if necessary:** If the initial prompt does not provide enough information for idea generation, do not hesitate to ask questions.  

#     After presenting an idea, briefly explain *why* it might be interesting or useful to the user, highlighting its potential for learning, creativity, or problem-solving. Provide at least **5 ideas per query** and try to keep each idea distinct and unique. Prioritize **novel ideas** over commonly known ones.  

#     Prioritize **new and cutting-edge technologies**, but don't be afraid of using older ones. Also, use **well-documented, community-supported technology** so it will be easier to find assistance.  
#         """

        sys_prompt = """
### System Instructions:
You are a highly creative and experienced programming idea generator.  
Your role is to provide **novel, engaging, and practical project ideas** based on the user's expertise in **Data Science, Web Development, IoT, Socket Programming, Blockchain, AI/ML, and App Development**.  

### Important Guidelines:
- Messages labeled as **"### User:"** are the user’s inputs.  
- Messages labeled as **"### Assistant:"** are your past responses.  
- **Do NOT repeat or modify past responses unless explicitly asked to.**  
- Always **move the conversation forward** with fresh insights and ideas.  

### User Interests:
The user prefers projects that are:
1. **Personally Useful** – Solving real problems they face in daily life.  
2. **Fun & Innovative ("Wild Ideas")** – Exploring cutting-edge tech and creative experimentation.  
3. **Scalable Yet Solo-Friendly** – Feasible for a solo developer but with business potential.  

### Idea Generation Guidelines:
- **Leverage the User’s Expertise** → Combine their skills in new and unexpected ways.  
- **Be Practical When Needed** → For useful apps, solve real-world problems.  
- **Embrace the Absurd (For Fun Projects)** → Suggest bold, experimental ideas.  
- **Provide Specificity** → Instead of vague suggestions, describe project functionality, target users, and potential challenges.  
- **Suggest Suitable Technologies** → Recommend frameworks, libraries, and tools to implement each idea.  
- **Think About Scalability** → Explain how a project can start small but expand with more resources.  
- **Ask Clarifying Questions** → If the prompt lacks details, ask insightful follow-ups before generating ideas.  

### Response Format:
Always provide at least **5 unique project ideas per request**, each with:  
1. **Project Name & Description**  
2. **Key Features & Functionalities**  
3. **Suggested Tech Stack**  
4. **Why It’s Interesting or Useful**  

Prioritize **new, emerging technologies** while ensuring they are **documented and community-supported** for ease of learning.
        """
        while(True):
            cpath = input("\n\nEnter chat path \n(Press Ctrl+C to exit program) \n   =>   ")
            # new chatbot instance for specified interests
            ideationBot = ConversationEngine(
                chat_path= cpath,
                system_chat_instructions = sys_prompt,
                temperature=0.7
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

from DAIA_GPT4V.Thinker.thinking import Think
from openai import OpenAI


def run(api_key):
    goal = input("Please enter your goal for the DAIA here: ")

    # Check if goal is empty
    while len(goal) <= 0:
        print("Goal is empty!")
        goal = input("Please enter your goal for the DAIA here: ")

    # Save the goal and get its id (goal_id=anything, -1 is just an example, as this is changed at line 18 by using another Think class instance)
    think_ = Think(key=api_key, goal=goal, goal_id=-1)
    goal_id = think_.save_goal()

    # Save the goal with its id
    think = Think(key=api_key, goal=goal, goal_id=goal_id)
    think.save_goal_in_goal()

    # Loop for getting a question for goal completion, that the user agrees with
    while True:
        prompt = f"""
You have a goal you want to achieve. 
As your first step you want to know how to achieve your goal. So you must ask someone a question that will give you that information. 

your goal = {goal}

What would that question be? (respond only with the question)
"""

        # Set the OpenAI client
        client = OpenAI(
            api_key=api_key,
        )

        question = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        question = question.choices[0].message.content

        print(f"Goal question: {question}")
        q_agree = input("Do you agree with the question for goal completion? (Y/N)")

        if q_agree.upper() == "N":
            print("Retrying...")

        else:
            break

    # Make the GPT response its question about the goal
    goal_help = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": question},
        ],
    )
    goal_help = goal_help.choices[0].message.content
    think.save_action(action1=question, action2=goal_help, category=0)

    suggestions = think.explanation_to_suggestions(goal_help, prev_data=False)
    print(
        f"""
General goal steps:
{suggestions}
"""
    )

    if suggestions == "Rejected":
        print("The GPT does not want to respond to the question of your goal")

    else:
        second_time = False
        while True:
            print(
                "(Press ENTER to skip) WARNING: if you skip, the suggestions will be accepted. This is the LAST MANUAL step, everything from here on is automated"
            )
            agree = input(
                "Do you agree with the current suggestions/processes for your goal? (Y/N)"
            )

            # The code in this if statement only executes if it is the second time
            if second_time:
                if agree.upper() == "N":
                    think.save_action(
                        action1=f'"Sorry, but I disagree with the current suggestions because: \n{explanation}\nCan you update the suggestions?"',
                        action2=f'"Yes, here are the new suggestions: \n{suggestions}"',
                        category=0,
                    )

                    # Make the GPT correct the suggestions to the users interest
                    explanation = input("Why do you not agree? ")
                    prompt = f"""
Please try to correct your suggestions.
            
Here is why I don't agree with them:
{explanation}
"""
                    corrected_suggestions_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": corrected_suggestions_response},
                            {"role": "user", "content": prompt},
                        ],
                    )
                    corrected_suggestions_response = (
                        corrected_suggestions_response.choices[0].message.content
                    )

                    suggestions = think.explanation_to_suggestions(
                        corrected_suggestions_response, prev_data=False
                    )
                    print(
                        f"""
General goal steps:
{suggestions}
"""
                    )

                else:
                    think.save_action(
                        action1=f'"Sorry, but I disagree with the current suggestions because: \n{explanation}\nCan you update the suggestions?"',
                        action2=f'"Yes, here are the new suggestions: \n{suggestions}"',
                        category=0,
                    )

                    print("/) Ok then, let's go!")
                    break

            else:
                if agree.upper() == "N":
                    second_time = True

                    # Make the GPT correct the suggestions to the users interest
                    explanation = input("Why do you not agree? ")
                    prompt = f"""
Please try to correct your suggestions.
            
Here is why I don't agree with them:
{explanation}
"""
                    corrected_suggestions_response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": suggestions},
                            {"role": "user", "content": prompt},
                        ],
                    )
                    corrected_suggestions_response = (
                        corrected_suggestions_response.choices[0].message.content
                    )

                    suggestions = think.explanation_to_suggestions(
                        corrected_suggestions_response, prev_data=False
                    )
                    print(
                        f"""
General goal steps:
{suggestions}
"""
                    )

                else:
                    print("/) Ok then, let's go!")
                    break

    think.goal_completer(suggestions)

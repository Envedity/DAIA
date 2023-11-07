import asyncio

from pathlib import Path
from DAIA_GoalTimed.Thinker.thinking import Think
from utils.openaicaller import caller


async def run(api_key):
    goal = input("Please enter your goal for the DAIA here: ")

    while len(goal) <= 0:
        print("Goal is empty!")
        goal = input("Please enter your goal for the DAIA here: ")

    think_ = Think(key=api_key, goal=goal, goal_id=-1)
    goal_id = await think_.save_goal()

    think = Think(key=api_key, goal=goal, goal_id=goal_id)
    await think.save_goal_in_goal()

    #        personal = input('''
    # (Press ENTER to skip)
    # Would you like to add some personal information to the DAIA? (this is optional, but could be helpful when dealing with goals involving payment and account info)
    # (Y/N) ''')
    #
    #        if personal.upper() == 'Y':
    #            crypto_wallet_addres = input(
    #                'Enter your crypto wallet address here: ')
    #            # Credit card option
    #            # ...
    #            print('When the DAIA thinks it needs to deposit anything into your accounts, it will first ask you before doing so')

    while True:
        prompt = f"""
You have a goal you want to achieve. 
As your first step you want to know how to achieve your goal. So you must ask someone a question that will give you that information. 

your goal = {goal}

What would that question be? (respond only with the question)             
"""

        question = await caller.generate_response(
            api_key=api_key,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )

        question = question["choices"][0]["message"]["content"]

        print(f"Goal question: {question}")
        q_agree = input("Do you agree with the question for goal completion? (Y/N)")

        if q_agree.upper() == "N":
            print("Retrying...")

        else:
            break

    goal_help = await caller.generate_response(
        api_key=api_key,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}],
    )

    goal_help = goal_help["choices"][0]["message"]["content"]

    await think.save_action(action1=question, action2=goal_help, category=0)
    previous_data = await think.short_remember(
        f"""
What are the suggestions in the response, based on the given response and previous data?

Previous data: >> previous context missing <<
Response: {goal_help}

Please provide the suggestions sequentially, without any additional text. For instance:
1. Suggestion
2. Suggestion
Additional suggestions mentioned in the response...

If the response explicitly rejects providing suggestions, please type "Rejected" on the first line of your response, followed by an explanation of why no suggestions or advice were given.

If the response does not include any suggestions or provides information other than suggestions, please generate your own suggestions based on the provided response and previous data. For example:
1. Suggestion
2. Suggestion
Additional suggestions based on the provided response and previous data...
"""
    )

    prompt = f"""
What are the suggestions in the response, based on the given response and previous data?

Previous data: {previous_data}
Response: {goal_help}

Please provide the suggestions sequentially, without any additional text. For instance:
1. Suggestion
2. Suggestion
Additional suggestions mentioned in the response...

If the response explicitly rejects providing suggestions, please type "Rejected" on the first line of your response, followed by an explanation of why no suggestions or advice were given.

If the response does not include any suggestions or provides information other than suggestions, please generate your own suggestions based on the provided response and previous data. For example:
1. Suggestion
2. Suggestion
Additional suggestions based on the provided response and previous data...
"""

    suggestions = await caller.generate_response(
        api_key=api_key,
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    suggestions = suggestions["choices"][0]["message"]["content"]

    await think.save_action(action1=prompt, action2=suggestions, category=0)

    if suggestions[0:5].lower() in "reject":
        print(
            f"""
Goal {suggestions}
"""
        )

    else:
        print("Goal accepted!")
        print(
            f"""
General goal steps:
{suggestions}
"""
        )

        second_time = False
        while True:
            print(
                "(Press ENTER to skip) WARNING: if you skip, the suggestions will be accepted. This is the LAST MANUAL step, everything from here on is automated"
            )
            agree = input(
                "Do you agree with the current suggestions/processes for your goal? (Y/N)"
            )

            if second_time:
                if agree.upper() == "N":
                    await think.save_action(
                        action1=f'"Sorry, but I dissagree with the current suggestions because: \n{explanation}\nCan you update the suggestions?"',
                        action2=f'"Yes, here are the new suggestions: \n{suggestions}"',
                        category=0,
                    )

                    explanation = input("Why do you not agree? ")

                    prompt = f"""
Please try to correct your suggestions.
            
Here is why I don't agree with them:
{explanation}
"""

                    suggestion_correction = await caller.generate_response(
                        api_key=api_key,
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": suggestion_correction},
                            {"role": "user", "content": prompt},
                        ],
                    )

                    suggestion_correction = suggestion_correction["choices"][0][
                        "message"
                    ]["content"]

                    prompt = f"""
Please provide the suggestions mentioned in the following response:

Response: {suggestion_correction}

List only the suggestions in a sequential manner, without any additional text. For example:
1. Suggestion
2. Suggestion
Additional suggestions mentioned in the response...

If the response explicitly rejects providing suggestions, please type "Rejected" on the first line of your response, followed by an explanation of why no suggestions or advice were given.

If the response does not include any suggestions or provides information other than suggestions, please generate your own suggestions based on the provided response. For example:
1. Suggestion
2. Suggestion
Additional suggestions based on the provided response...
"""

                    suggestions = await caller.generate_response(
                        api_key=api_key,
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                    )

                    suggestions = suggestions["choices"][0]["message"]["content"]

                    if suggestions[0:5].lower() in "reject":
                        print(
                            f"""
Goal {suggestions}
"""
                        )

                    else:
                        print("Goal accepted!")
                        print(
                            f"""
General goal steps:
{suggestions}
"""
                        )

                else:
                    await think.save_action(
                        action1=f'"Sorry, but I dissagree with the current suggestions because: \n{explanation}\nCan you update the suggestions?"',
                        action2=f'"Yes, here are the new suggestions: \n{suggestions}"',
                        category=0,
                    )

                    print("/) Ok then, let's go!")
                    break

            else:
                if agree.upper() == "N":
                    second_time = True
                    explanation = input("Why do you not agree? ")

                    prompt = f"""
Please try to correct your suggestions.
            
Here is why I don't agree with them:
{explanation}
"""

                    suggestion_correction = await caller.generate_response(
                        api_key=api_key,
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": suggestions},
                            {"role": "user", "content": prompt},
                        ],
                    )

                    suggestion_correction = suggestion_correction["choices"][0][
                        "message"
                    ]["content"]

                    prompt = f"""
Please provide the suggestions mentioned in the following response:

Response: {suggestion_correction}

List only the suggestions in a sequential manner, without any additional text. For example:
1. Suggestion
2. Suggestion
Additional suggestions mentioned in the response...

If the response explicitly rejects providing suggestions, please type "Rejected" on the first line of your response, followed by an explanation of why no suggestions or advice were given.

If the response does not include any suggestions or provides information other than suggestions, please generate your own suggestions based on the provided response. For example:
1. Suggestion
2. Suggestion
Additional suggestions based on the provided response...
"""

                    suggestions = await caller.generate_response(
                        api_key=api_key,
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                    )

                    suggestions = suggestions["choices"][0]["message"]["content"]

                    if suggestions[0:5].lower() in "reject":
                        print(
                            f"""
Goal {suggestions}
"""
                        )

                    else:
                        print("Goal accepted!")
                        print(
                            f"""
General goal steps:
{suggestions}
"""
                        )

                else:
                    print("/) Ok then, let's go!")
                    break

    await think.goal_completer(suggestions)


# think.goal_completer(suggestions)

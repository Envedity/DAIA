from utils.openaicaller import caller, models_max_tokens
from DAIA_GoalTimed.Memory.memory import Memory
from utils.tokens import num_tokens_from_messages


class Think:
    def __init__(self, key: str, goal: str, goal_id: int):
        self.openai_api_key = key
        self.goal = goal
        self.goal_id = goal_id

    async def goal_completer(self, suggestions: str):
        real_suggestions = self.get_suggestions(suggestions)
        for suggestion in real_suggestions:
            sub_suggestions = await self.suggestion_splitter(suggestion)

        # Process the first level of suggestions
        # for suggestion in self.suggestions:
        #    explanation = self.suggestion_explainer(suggestion, ...)
        #    action = self.action(explanation, ...)
        #
        #    # Continue processing sub-suggestions as long as the action is False
        #    while action == False:
        #        sub_suggestions = self.suggestion_splitter(explanation, ...)
        #
        #        # Process each sub-suggestion
        #        for sub_suggestion in sub_suggestions:
        #            sub_explanation = self.suggestion_explainer(sub_suggestion, ...)
        #            sub_action = self.action(sub_explanation, ...)
        #
        #            # Continue processing sub-sub-suggestions as long as the sub-action is False
        #            while sub_action == False:
        #                sub_sub_suggestions = self.suggestion_splitter(sub_explanation, ...)
        #
        #                # Process each sub-sub-suggestion
        #                for sub_sub_suggestion in sub_sub_suggestions:
        #                    sub_sub_explanation = self.suggestion_explainer(sub_sub_suggestion, ...)
        #                    sub_sub_action = self.action(sub_sub_explanation)
        #
        #                    if sub_sub_action == False:
        #                        # Continue processing sub-sub-suggestions
        #                        continue
        #                    else:
        #                        # Do the action for sub-sub-suggestion
        #                        pass
        #
        #                # Check if there are more sub-sub-suggestions
        #                if not sub_sub_suggestions:
        #                    sub_action = True  # Exit the sub-action loop if there are no more sub-sub-suggestions
        #
        #            # Do the action for sub-suggestion
        #            pass
        #
        #        # Check if there are more sub-suggestions
        #        if not sub_suggestions:
        #            action = True  # Exit the action loop if there are no more sub-suggestions
        #
        #    print(f'Action {suggestion} done')
        #    pass

        # OR

        # for suggestion in self.suggestions:
        #    explanation = self.suggestion_explainer(suggestion, ...)
        #    action = self.action(explanation, ...)
        #
        #    if action == False:
        #        sub_suggestions = self.suggestion_splitter(explanation, ...)
        #
        #        for sub_suggestion in sub_suggestions:
        #            sub_explanation = self.suggestion_explainer(sub_suggestion, ...)
        #            sub_action = self.action(explanation, ...)
        #
        #            if sub_action == False:
        #                sub_sub_suggestions = self.suggestion_splitter(sub_explanation, ...)
        #
        #                for sub_sub_suggestion in sub_sub_suggestions:
        #                    sub_sub_explanation = self.suggestion_explainer(sub_sub_suggestion, ...)
        #                    sub_sub_action = self.action(sub_sub_explanation)
        #
        #                    if sub_sub_action == False:
        #                        # Do the same....
        #
        #                    else:
        #                        pass
        #                        # Do the action
        #
        #            else:
        #                pass
        #                # Do the action
        #
        #    else:
        #        pass
        #        # Do the action

    def action_compleation():
        pass
        # Compleate actions

    async def action(
        self,
        suggestion: str,
        os: str,
        commands: str,
        screen_data: str,
        previous_data: str,
    ):
        str_commands = ""
        for command in commands:
            str_commands = str(command) + "\n"

        while True:
            executable = await caller.generate_response(
                api_key=self.openai_api_key,
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
Can you determine if the provided suggestion, along with the given commands and current screen data, is specific enough to be executed on the {os}? Please provide the first command with its expected outcome to complete the suggestion if it is possible. Consider the following information:

Given commands:
{str_commands}

Previous data:
{previous_data}

Current screen information:
{screen_data}

Suggestion:
{suggestion}

If the suggestion is sufficiently specific and can be carried out on the {os} using the provided commands and current screen data, please type the first command along with its expected outcome, like this:
1. [command][perameter of command or none] (expected outcome)
    
If the suggestion is not specific enough, please state "Not specific"
""",
                    }
                ],
            )

            if executable == "Not specific" or executable == '"Not specific"':
                return False

            else:
                return executable

    async def suggestion_explainer(self, suggestion: str):
        previous_info = await self.short_remember(
            f"""
You have a goal you want to achieve.
You have already gotten some information on the steps to achieving your goal.
So, based on the previous steps and information you must ask someone a question that will give you the information to complete your current step to progress toward achieving your goal. 

your goal = {self.goal}
your previous steps and information = >>previous context missing<<
your current step = {suggestion}

What would that question be? (respond only with the question)
"""
        )

        prompt = f"""
You have a goal you want to achieve. 
You have already gotten some information on the steps to achieving your goal.
So, based on the previous steps and information you must ask someone a question that will give you the information to complete your current step to progress toward achieving your goal. 

your goal = {self.goal}
your previous steps and information = {previous_info}
your current step = {suggestion}

What would that question be? (respond only with the question)             
"""

        # print(f'Previous info for {suggestion}: {previous_info}\n \n')

        question = await caller.generate_response(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        question = question["choices"][0]["message"]["content"]

        await self.save_action(action1=prompt, action2=question, category=0)

        # print(f'Prompt for {suggestion}: {previous_info}\n \n')

        suggestion_suggestions = await caller.generate_response(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
{question}
""",
                }
            ],
        )

        await self.save_action(
            action1=question,
            action2=suggestion_suggestions["choices"][0]["message"]["content"],
            category=0,
        )

        # print(f'Explanation for {suggestion}: {suggestion_suggestions}\n \n')

        return suggestion_suggestions["choices"][0]["message"]["content"]

    async def suggestion_splitter(self, suggestion: str):
        explanation = await self.suggestion_explainer(suggestion)
        previous_data = await self.short_remember(
            f"""
What are the suggestions in the response based on the given response and previous data?

Previous data: >>previous data missing<<
Response: {explanation}

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
What are the suggestions in the response based on the given response and previous data?

Previous data: {previous_data}
Response: {explanation}

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

        while True:
            sub_suggestions = await caller.generate_response(
                api_key=self.openai_api_key,
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            sub_suggestions = sub_suggestions["choices"][0]["message"]["content"]

            await self.save_action(action1=prompt, action2=sub_suggestions, category=0)

            if sub_suggestions[0:5].lower() in "reject":
                print(
                    f"""
Sub-suggestion {sub_suggestions}\n \n
"""
                )

            else:
                print(
                    f"""
General '{suggestion}' steps:
{sub_suggestions}\n \n
"""
                )

                return sub_suggestions

    async def gpt_memory_capacity(self, data, gpt_role, gpt):
        max_tokens = models_max_tokens[gpt]
        message = {"role": gpt_role, "content": data}
        message_list = [message]
        tokens = await num_tokens_from_messages(message_list)

        if tokens < max_tokens:
            return True

        else:
            return False

    async def save_goal(self):
        goal_summary = await self.generate_title(self.goal, "goal")

        memory = Memory()
        new_goal = memory.create_goal_object(goal_summary)
        memory.save_objects_in_db([new_goal])

        return new_goal.goal_id

    async def save_goal_in_goal(self):
        memory = Memory()

        goal_action = memory.create_action_object(
            goal_id=self.goal_id,
            title="Final Goal",
            category="Goal",
            full_data=self.goal,
            important_data=f"The Final Goal is: {self.goal}",
        )
        memory.save_objects_in_db([goal_action])

    async def save_action(self, action1: str, action2: str, category: int):
        """
        Category:
        "question=>response" = int 0
        "response=>action" = int 1
        "action=>result" = int 2
        "result=>action" = int 3
        """

        categories = [
            "question=>response",
            "response=>action",
            "action=>result",
            "result=>action",
        ]

        first = categories[category].split("=")[0]
        second = categories[category].split(">")[-1]

        memory = Memory()

        data = f'[1. {first}]: "{action1}",\n[2. {second}]: "{action2}"'
        title = await self.generate_title(data, f'"{first} with its {second}"')
        previous_important_data = await self.short_remember(
            f"""
Given the following context:
>>previous context missing<<

And the input data:
"{data}"

Please use the provided context to extract and present the most important data from the input.
""",
        )

        important_data = await self.get_important_data(data, previous_important_data)

        new_action = memory.create_action_object(
            self.goal_id, title, categories[category], data, important_data
        )
        memory.save_objects_in_db([new_action])

    async def short_remember(self, need: str):
        memory = Memory()

        previous_important_data = ""
        for action in memory.get_ordered_actions_of_goal(self.goal_id, 100):
            previous_important_data = previous_important_data + "".join(
                f'[{getattr(action, "action_id")}. Action: (Title of action: "{getattr(action, "title")}", Important data of action: "{getattr(action, "important_data")}")]\n'
            )

        if len(previous_important_data) <= 0:
            return "Nothing has hppened yet."

        previous_data = await caller.generate_response(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Given the following context:
"{previous_important_data}"

And the input data:
"{need}"

Please input the necessary, relevant, and concise context from the following context to complete the input. Your input should address the gaps in the provided input data, ensuring accurate responses without any future errors or issues.

Please avoid addressing the prompt directly. Only provide the crucial context. Keep your response minimal and to the point.
""",
                }
            ],
        )

        # print(
        #    f'Previous_info: {previous_data["choices"][0]["message"]["content"]}\n \n')

        return previous_data["choices"][0]["message"]["content"]

    async def get_important_data(self, data: str, previous_data: str):
        important_data = await caller.generate_response(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Given the following context:
"{previous_data}"

And the input data:
"{data}"

Please use the provided context to extract and present the most important data from the input.
""",
                }
            ],
        )

        return important_data["choices"][0]["message"]["content"]

    async def generate_title(self, data: str, item_category: str):
        title = await caller.generate_response(
            api_key=self.openai_api_key,
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Provide a concise title (<75 chars) describing the {item_category}.

{item_category} = "{data}"
""",
                }
            ],
        )

        return title["choices"][0]["message"]["content"]

    def get_suggestions(self, suggestions: str):
        suggestions_ = suggestions
        for n in range(0, 40):
            number = 40 - n
            suggestions_ = suggestions_.replace(f"{number}.", "%_%")

        suggestions_ = suggestions_.replace("\n", "")
        real_suggestions = suggestions_.split("%_%")

        if real_suggestions.count("") > 0:
            real_suggestions.remove("")

        return real_suggestions

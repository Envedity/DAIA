QUESTION = """
You are seeking guidance to accomplish a specific objective. To initiate your journey towards this goal, you need crucial information that can only be obtained by asking the right question.

Goal: {goal}

What question should you ask to gain the necessary insight for achieving your goal? Please respond with just the question.
"""

IS_SCREENSHOT_RELEVANT_TO_GOAL = """
Examine the attached screenshot of the {os_name} operating system. Identify and describe any elements in the screenshot that are relevant to the suggestion of achieving the goal: {goal}.
"""

LIST_COMMANDS_FOR_SUGGESTION = """
Evaluate the feasibility of implementing the suggested action on the {os_name} operating system, using the provided commands and the current screen data. Consider the following inputs:

- Given Commands: {str_commands}
- Previous Data: {previous_data}
- Current Screen Information: {screen_data}
- Suggestion: {suggestion}

Response Format:
If the suggestion can be executed on the {os_name} OS:
- Provide a response in JSON format:
  {"status": "possible", "commands": [{"command": "command name", "parameter": "parameter(s) of command, if any", "expected_outcome": "a detailed description of the expected result"}]}

If the suggestion is not specific enough for execution:
- Provide a response in JSON format with a reason for the impossibility:
  {"status": "impossible", "commands": [], "reason": "Not specific enough due to [brief explanation]"}
"""

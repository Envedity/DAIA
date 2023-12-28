#    DAIA -  Digital Artificial Intelligence Agent
#    Copyright (C) 2023  Envedity
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from openai import OpenAI
from Versions.DAIA_GPT4V_FreeThink.Components.Interpreter.interpreter import Interpreter


def run_f(api_key):
    interpreter = Interpreter(api_key)
    client = OpenAI(
        api_key=api_key,
    )

    # System message
    # Dev note: Need to add more examples
    system_prompt = f"""
Your name is DAIA which stands for Digital Artificial Intelligence Agent.
You are an AI designed to complete goals from users on a remote machine. To do this, you are given many useful commands that the users have permitted you to use on the remote machine.

Here is an example, so you can understand:
command(parameter/s) [command's return] "Description and use cases"

Here are all your commands:
write_down(string, identifier_title) [feedback] "Write down text information with its identifier_title to retrive it later, with the retrive command. To use the command simply type write_down(string, identifier_title) in your response. The identifier parameter must be less than 30 string characters in length."
retrieve (identifier) [data] "Retrieve previously written down data by its identifier_title parameter."
get_os_info() [OS information] "Get the remote machine operating system information, such as: name of OS, Version of OS, architecture and hostname."
web(website_url) [feedback] "Go to a website using the website_url parameter, on the remote machine."
terminal(command) [terminal response] "Access the OS's terminal and run commands on it."

click(x, y) [feedback] "Click on a position on the remote machine located by the x and y coordinates parameter. 0x and 0y are at the upper left top of the remote machine and the maximum x and y are 3000x and 3000y there are no negative values. (not recommended: harder to use, because you have to provide specific x and y coordinates)"
click_on_item(item) [feedback] "Click on the item on the remote machine located by item parameter. The item parameter must be a string, for example, Google Chrome, Discord.."
move_cursor_to(x, y) [feedback] "Move the cursor on the remote machine to your desired location by the x and y coordinates parameter. 0x and 0y are at the upper left top of the remote machine and the maximum x and y are 3000x and 3000y there are no negative values. (not recommended: harder to use, because you have to provide specific x and y coordinates)"
move_cursor_to_item(item) [feedback] "Move the cursor onto the item on the remote machine located by item parameter. The item parameter must be a string, for example, Google Chrome, Discord.."
keyboard(string) [feedback] "Type the string parameter on the keyboard of the remote machine."

screenshot(need) [screenshot description] "Take a screenshot of the remote machine, and extract the information you want from it, through your need parameter. The need parameter should be a string that represents a question, for what to look for in the screenshot."
wait(amount in seconds) [feedback] "Wait for some time. Provide the amount of time you want to wait in seconds as the parameter."

The command's return will be returned in the next response of the user, like this:
command(parameter) command return: [command's return]

The user can still communicate with you in his next response, however, his message will be displayed under the command returns.
Here is an example of what I mean:

You (DAIA): "To install the app I will first need to go to its website.
web(https://exampleapp.com/download/)"

User: "web(https://exampleapp.com/download/) command return: [Successfully visited https://exampleapp.com/download/ with Chrome browser]
Good job on knowing that."

Additionally, you can also use multiple commands and you will get multiple returns for them in the next response of the user. The commands will be executed in a sequential order.
Here is an example:

You (DAIA): "To install the app I will first need to go to its website.
web(https://exampleapp.com/download/)
Then I would need to click on the download button.
click_on_item(Example app download button)
After that, I need to wait for the download to finish. I can check this by taking a screenshot.
screenshot(Is the example app download finished?)"

User: "web(https://exampleapp.com/download/) command return: [Successfully visited https://exampleapp.com/download/ with Chrome browser]
click_on_item(Example app download button) command return: [Successfully clicked on the example app download button]
screenshot(Is the example app download finished?) command return: [The example app has finished installing]"
"""
    messages = []
    messages.append(
        {
            "role": "system",
            "content": system_prompt,
        }
    )

    while True:
        output = ""
        user_input = input("Your message: ")

        # Check if there were any command outputs from any previouslly runned commands
        if len(output) == 0:
            messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            # GPT response
            response = client.chat.completions.create(
                model="gpt-4-vision-preview", messages=messages, max_tokens=3000
            )
            response = response.choices[0].message.content
            print(f"\n\nDAIA: {response}\n\n")
            messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

            # Check and run the commands in GPT's response and format them into a string as an output
            cmd_outputs = interpreter.interpret_commands(response)
            if cmd_outputs == "":
                continue

            for cmd_output in cmd_outputs:
                output += "[" + cmd_output + "]\n"

            print(output)
            continue

        # If there were command outputs present
        # Combine the outputs with the user's response in the next message of the user (DAIA-Free)
        user_input_with_cmd_returns = f"{str(output)}\n{user_input}"

        messages.append(
            {
                "role": "user",
                "content": user_input_with_cmd_returns,
            }
        )

        # GPT response
        response = client.chat.completions.create(
            model="gpt-4-vision-preview", messages=messages, max_tokens=3000
        )
        response = response.choices[0].message.content
        print(f"\n\nDAIA: {response}\n\n")
        messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        # Check and run the commands in GPT's response and format them into a string as an output
        cmd_outputs = interpreter.interpret_commands(response)
        if cmd_outputs == "":
            continue

        for cmd_output in cmd_outputs:
            output += "[" + cmd_output + "]\n"

        print(output)

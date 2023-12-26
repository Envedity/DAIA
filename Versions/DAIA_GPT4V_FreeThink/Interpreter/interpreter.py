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
from Versions.DAIA_GPT4V_FreeThink.OS_control.os_controller import OSController
from Versions.DAIA_GPT4V_FreeThink.DVAI.GPT_4_with_Vision import DVAI
from pathlib import Path
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import subprocess
import re


class Interpreter:
    """
    Interpret commands of the given input content

    Supported commands:
    'write_down': self.write_down,
    'retrieve': self.retrieve,
    'get_os_info': self.get_os_info,
    'web': self.web,
    'terminal': self.terminal,
    'click': self.click,
    'click_on_item': self.click_on_item,
    'move_cursor_to': self.move_cursor_to,
    'move_cursor_to_item': self.move_cursor_to_item,
    'keyboard': self.keyboard,
    'screenshot': self.screenshot,
    'wait': self.wait,
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        # Initialize the OpenAI client and the commands
        self.client = OpenAI(api_key=api_key)
        self.commands = {
            "write_down": self.write_down,
            "retrieve": self.retrieve,
            "get_os_info": self.get_os_info,
            "web": self.web,
            "terminal": self.terminal,
            "click": self.click,
            "click_on_item": self.click_on_item,
            "move_cursor_to": self.move_cursor_to,
            "move_cursor_to_item": self.move_cursor_to_item,
            "keyboard": self.keyboard,
            "screenshot": self.screenshot,
            "wait": self.wait,
        }

        self.os_controller = OSController()

    def interpret_commands(self, input_content: str):
        """
        See if the commands are in the input_content parameter, and if they are then run them and return the output
        """

        commands = self.extract_commands(input_content)

        # Check if there are any commands
        if commands == "":
            return ""

        # Running commands
        command_returns = []
        for command in commands:
            command_name, params = command

            # If the commands do not have a parameter
            if len(params) <= 0 or len(params[0]) == 0:
                if command_name in self.commands:
                    command_function = self.commands[command_name]
                    command_return = command_function()
                    command_returns.append(
                        f"{command_name} command return: {command_return}"
                    )
                    continue

            # If there is only one parameter to the command, then convert the parameter to a string
            if len(params) == 1:
                params = params[0]

            if command_name in self.commands:
                command_function = self.commands[command_name]
                command_return = command_function(params)
                command_returns.append(
                    f"{command_name} command return: {command_return}"
                )

        return command_returns

    def extract_commands(self, input_content: str):
        """
        Extract commands from the input_content parameter
        """

        # Regular expression to extract commands from user input
        pattern = r"(\w+)\(([^)]*)\)"
        matches = re.findall(pattern, input_content)
        if len(matches) == 0:
            return ""

        commands = [
            (match[0], [param.strip() for param in match[1].split(",")])
            for match in matches
        ]

        return commands

    def write_down(self, string: str, identifier_title: str):
        """
        Save the string text information in a .txt file with the name being its identifier_title parameter to retrieve it later with the retrieve command
        """

        writedown_file = Path(
            f"DAIA/Versions/DAIA_GPT4V_Free/Memory/Writedown_files/{identifier_title}.txt"
        )
        writedown_file.write_text(string)

        return (
            f'Successfully wrote down: "{string}" with identifier "{identifier_title}"'
        )

    def retrieve(self, identifier: str):
        """
        Retrieve previously written down text
        """

        writedown_file = Path(
            f"DAIA/Versions/DAIA_GPT4V_Free/Memory/Writedown_files/{identifier}.txt"
        )
        # writedown_files = writedown_dir.glob('*.txt')

        return f'Retrieved data for identifier {identifier}: "{writedown_file.read_text()}"'

    def get_os_info(self):
        os_info = self.os_controller.get_system_info()

        return f'OS: {os_info["OS"]}, Version: {os_info["Version"]}, Architecture: {os_info["Architecture"]}, Hostname: {os_info["Hostname"]}'

    def web(self, website_url: str):
        """
        Open the website with its websitre_url with a Chrome webdriver using selenium
        """

        # Specifing the browser options
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--log-level=3")
        browser = webdriver.Chrome(options=options)

        browser.get(website_url)

        return f"Successfully visited {website_url} with Google Chrome"

    def terminal(self, command: str):
        """
        Run commands on the terminal and return their outputs
        """

        r_command = subprocess.run(command, capture_output=True, text=True)

        if r_command.returncode == 0:
            # Return the stdout of the command
            return r_command.stdout

        else:
            # If the command fails
            return f"Error: [{r_command.returncode}]:\n{r_command.stderr}"

    def click(self, x, y):
        self.os_controller.click(x, y)

        return f"Successfully clicked at {x}x, {y}y"

    def click_on_item(self, item: str):
        """
        Click on an item (known by the item parameter) on the screen, by first taking a screenshot, then giving the screenshot to the DVAI, then asking it to give coordinates for the item location on the screen and, then clicking at those coordinates

        Dev note: The DVAI (GPT-4-with-Vision) currently cannot know the coordinates of what it is seeing,
        because of this we should add a coordinate map image over the screen when the screenshot is taken so that the DVAI can then know at what coordinates its item is.
        """

        location = self.screenshot(
            f"Where on the provided screenshot is {item}? Provide the location in x and y coordinates. For example: 500x 200y"
        )
        x_value, y_value = self.extract_coordinates(location)

        self.click(x_value, y_value)

        return f"Successfully clicked at {item}, that was located at {x_value}x, {y_value}y"

    def move_cursor_to(self, x, y):
        self.os_controller.move_cursor_to(x, y)

        return f"Successfully moved cursor to {x}x, {y}y"

    def move_cursor_to_item(self, item: str):
        """
        Move the cursor to an item (known by the item parameter) on the screen, by first taking a screenshot, then giving the screenshot to the DVAI, then asking it to give coordinates for the item location on the screen and, then moving the cursor to those coordinates

        Dev note: The DVAI (GPT-4-with-Vision) currently cannot know the coordinates of what it is seeing,
        because of this we should add a coordinate map image over the screen when the screenshot is taken so that the DVAI can then know at what coordinates its item is.
        """

        location = self.screenshot(
            f"Where on the provided screenshot is {item}? Provide the location in x and y coordinates. For example: 500x 200y"
        )
        x_value, y_value = self.extract_coordinates(location)

        self.move_cursor_to(x_value, y_value)

        return f"Successfully moved cursor to {item}, that was located at {x_value}x, {y_value}y"

    def keyboard(self, string: str):
        self.os_controller.keyboard(string)

        return f'Successfully typed "{string}"'

    def screenshot(self, need: str):
        """
        Take a screenshot and ask the DVAI what you need to know (need parameter) about the screenshot, and return the DVAI's response to it
        """

        screenshot_savepath = Path(
            f'DAIA/Screenshots/screenshot{"".join([str(e + randint(1, 9)) for e in range(10)])}.png'
        )
        self.os_controller.screenshot(screenshot_savepath)

        dvai = DVAI(self.api_key)
        response = dvai.gpt_with_vision_by_base64(screenshot_savepath, need)

        return response

    def wait(self, seconds: str):
        sleep(int(seconds))

        return f"Successfully waited {seconds} seconds"

    def extract_coordinates(self, message: str):
        """
        Extract the coordinates present in the message, for example: 500x and 200y
        """

        # Define a regular expression pattern to match x and y values
        pattern = re.compile(r"(\d+)x.*?(\d+)y")

        # Find all matches in the given message
        match = pattern.search(message)

        # Initialize x and y values
        x_value = None
        y_value = None

        # Extract x and y values from the match
        if match:
            x_value = int(match.group(1))
            y_value = int(match.group(2))

        return x_value, y_value

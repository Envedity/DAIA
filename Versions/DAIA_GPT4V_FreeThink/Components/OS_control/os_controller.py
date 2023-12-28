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

import pyautogui
import platform


class OSController:
    """
    Control the OS using pyautogui, and get its data with the platform library
    """

    def __init__(self):
        self.x = pyautogui.position()[0]
        self.y = pyautogui.position()[1]

    def click(self, x, y):
        pyautogui.click(int(x), int(y))

    def move_cursor_to(self, x, y):
        pyautogui.moveTo(int(x), int(y), duration=0.2)

    def keyboard(self, string):
        pyautogui.typewrite(string)

    def scroll(self, direction, amount):
        if direction == "up":
            pyautogui.scroll(-amount)
        elif direction == "down":
            pyautogui.scroll(amount)

    def screenshot(self, path):
        screenshot = pyautogui.screenshot()
        screenshot.save(path)

    def get_system_info(self):
        return {
            "OS": platform.system(),
            "Version": platform.release(),
            "Architecture": platform.processor(),
            "Hostname": platform.node(),
        }

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

import sys
import time


class ProgressIndicator:
    def __init__(self, prefix="Thinking", suffix="Complete"):
        self.prefix = prefix
        self.suffix = suffix
        self.start_time = time.time()

    def update(self, iteration):
        progress_indicator = self.get_spinner(iteration)

        sys.stdout.write("\r%s %s" % (self.prefix, progress_indicator))
        sys.stdout.flush()

    def get_spinner(self, iteration):
        spinners = ["-", "\\", "|", "/"]
        return spinners[iteration % len(spinners)]


total_iterations = 100
progress_indicator = ProgressIndicator(prefix="Thinking", suffix="Complete")

for i in range(total_iterations + 1):
    time.sleep(0.1)
    progress_indicator.update(i)

sys.stdout.flush()

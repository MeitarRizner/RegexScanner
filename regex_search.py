import argparse
import json
import re
import sys
from abc import ABC, abstractmethod


"""
The code follows the Strategy design pattern,
which encapsulates different output formats and makes them interchangeable at runtime based command-line arguments.
"""

"""
Abstract base class for output formatters.
"""


class OutputFormatter(ABC):
    """
    This function formats the output based on the output formatter's strategy.
    Parameters:
    - file_name (str): The name of the file being processed.
    - line (str): The line from the file being processed.
    - line_no (int): The line number of the line being processed.
    - matches (iterator): An iterator of match objects found in the line.
    """

    @abstractmethod
    def format(self, file_name, line, line_no, matches):
        pass


"""
Output formatter that formats the matched line as "file name, line number, matched_text".
"""


class DefaultFormatter(OutputFormatter):
    def format(self, file_name, line, line_no, matches):
        for match in matches:
            print(
                f"file name: {file_name}, line: {line_no}, matched_text: {match.group()}"
            )


"""
Output formatter that formats the matched line with '^' characters under the matched text.
"""


class UnderscoreFormatter(OutputFormatter):
    def format(self, file_name, line, line_no, matches):
        last_index = 0
        output = ""
        for match in matches:
            output += " " * (match.start() - last_index) + "^" * (
                match.end() - match.start()
            )
            last_index = match.end()
        print(line)
        print(output)


"""
Output formatter that formats the matched text with highlight it in red.
"""


class ColorFormatter(OutputFormatter):
    def format(self, file_name, line, line_no, matches):
        last_index = 0
        output = ""
        for match in matches:
            output += line[last_index : match.start()] + "\033[91m{}\033[00m".format(
                line[match.start() : match.end()]
            )
            last_index = match.end()
        print(output, end="")
        print(line[last_index:])


"""
Output formatter that generates machine readable output (json file) in the format "file_name:no_line:start_pos:matched_text".
"""


class MachineFormatter(OutputFormatter):
    def format(self, file_name, line, line_no, matches):
        data = []
        for match in matches:
            data.append(f"{file_name}:{line_no}:{match.start()}:{match.group()}")
        with open("json_output_file.json", "a") as file:
            json.dump(data, file, indent=4)


"""
Class that searches for lines matching a regular expression in a file or in stdin.
"""


class RegularExpressionFinder:
    """
    Compile the regular expression and checks if it's valid
    """

    def __init__(self):
        (
            self.pattern,
            self.files,
            self.underscore,
            self.color,
            self.machine,
        ) = self.get_command_line_parameters()
        try:
            self.pattern = re.compile(self.pattern)
        except re.error:
            print("Invalid regular expression")
            exit()
        self.get_content()

    """
    Parses command line arguments and returns the values of the corresponding parameters.
    """

    def get_command_line_parameters(self):
        parser = argparse.ArgumentParser(
            description="Search for lines matching regular expression in file(s)."
        )
        parser.add_argument(
            "-r",
            "--regex",
            dest="regular_expression",
            help="Regular expression to search.",
            required=True,
        )
        parser.add_argument(
            "-f",
            "--files",
            dest="files",
            help="List of files to search in. If not provided, STDIN is used.",
            nargs="+",
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-u",
            "--underscore",
            dest="underscore",
            action="store_true",
            help='Print "^" under the matched text.',
        )
        group.add_argument(
            "-c",
            "--color",
            dest="color",
            action="store_true",
            help="Highlight the matched text.",
        )
        group.add_argument(
            "-m",
            "--machine",
            dest="machine",
            action="store_true",
            help="Generate machine readable output.",
        )
        try:
            args = parser.parse_args()
        except argparse.ArgumentError as exc:
            print(f"ArgumentError: {exc.argument_name} {exc.message} ")
            exit()
        return (
            args.regular_expression,
            args.files,
            args.underscore,
            args.color,
            args.machine,
        )

    """
    Reads in the content from files (or standard input)
    """

    def get_content(self):
        if self.files is not None:
            for file_name in self.files:
                try:
                    file = open(file_name, "r")
                except FileNotFoundError as exc:
                    print(f"File not found error: {exc.filename}")
                    exit()
                self.search_matches(file, file_name)
                file.close()
        else:
            print(
                "Enter text to searches for lines matching regular expression"
                "(Press CTRL+D (Unix) or CTRL+Z (Windows) to exit): "
            )
            self.search_matches(sys.stdin.readlines(), "STDIN")

    """
    Searches for matches of the regular expression in each line of a file.
    """

    def search_matches(self, file, file_name):
        for line_no, line in enumerate(file, 1):
            line = line.replace("\n", "")
            matches = self.pattern.finditer(line)
            self.output_formatted_data(file_name, line, line_no, matches)

    """
    This method takes in the file name, line, line number, and matches found in the line,
    and outputs the formatted data based on the selected formatter specified through the command-line arguments.
    """

    def output_formatted_data(self, file_name, line, line_no, matches):
        formatters = {
            "default": DefaultFormatter(),
            "underscore": UnderscoreFormatter(),
            "color": ColorFormatter(),
            "machine": MachineFormatter(),
        }
        if self.underscore:
            formatter = formatters["underscore"]
        elif self.color:
            formatter = formatters["color"]
        elif self.machine:
            formatter = formatters["machine"]
        else:
            formatter = formatters["default"]
        formatter.format(file_name, line, line_no, matches)


def main():
    RegularExpressionFinder()


if __name__ == "__main__":
    main()

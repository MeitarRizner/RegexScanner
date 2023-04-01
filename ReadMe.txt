How to use the script:
1. Open a command prompt or terminal window.
2. Navigate to the directory where the script is located.
3. Type "python regex_search.py" followed by the command-line arguments you want to use.
4. The available command-line arguments are:
     "-r" or "--regex": The regular expression pattern to search for (required).
     "-f" or "--file": The name of the file to search in (optional).
      If not provided, the script will read from standard input.
     "-u" or "--underscore": Use underscore formatting for output (optional).
     "-c" or "--color": Use color formatting for output (optional).
     "-m" or "--machine": Use machine-readable formatting for output (optional).
     "-h" or "--help": Display help message and exit (optional).
5. Press enter to execute the command.
6. If the "-f" or "--file" argument is used,
   the script will search for the regular expression pattern in each line of the specified file.
   If it is not used, the script will read from standard input.
7. The script will output the matches found using the appropriate formatter based on the command-line arguments.
   If no formatting option is selected, the default formatter will be used.
   
sample command: python regex_search.py -r ab* -f sample_file.txt -c

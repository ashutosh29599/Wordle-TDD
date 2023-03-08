# Wordle-TDD

## Software Design (COSC 6353 -- Spring 2023)
## Dr. Venkat Subramaniam

To run: 
1) Set up a Python virtual environment.
2) Activate the venv. For Mac, run the command "source venv/bin/activate".
3) Run the command "pip3 install -r /path/to/requirements.txt".
4) a) To run all the unit tests, use the command "paver".
   b) To run the ui (or play the game), use the command "paver ui".

Caveat: This program uses an api provided by the instructor to get the 
target word. There is also an external dependency that is used to check 
the spelling of the user input / guessed word.

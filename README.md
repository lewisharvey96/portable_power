#### Portable Power

This app showcases an example analysis into a battery and generator hybrid system. The goal is to show:
- How to size a generator
- How we can model a hybrid system
- How we could optimize a hybrid system sizing

#### Run the app
This application uses ```uv``` to manage the virtual environment. Once ```uv``` is installed:

- `uv sync` will install the dependencies

`Poe the Poet` is used as a task runner:

- `poe run` will run the streamlit app

#### Development
To maintain code quality some basic linting and type checking has been applied using `ruff` and `mypy`.
These checks can be run using the `poe lint` task.

#### Analysis
Some initial analysis and data cleaning has been done in a Jupyter notebook.
The notebook can be launched via the `poe jupy` command.
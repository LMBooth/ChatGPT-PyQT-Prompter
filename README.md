```markdown
# GPT Turbo Prompter

GPT Turbo Prompter is a desktop application built with PyQt5 that allows users to interact with various OpenAI models. Users can provide prompts to the models and receive generated responses. The application supports setting an API key, choosing different models, maintaining a history of prompts, and displaying the models' responses.

## Features

- Set the OpenAI API Key interactively.
- Choose between different GPT models (e.g., gpt-3.5-turbo, gpt-4).
- Enter prompts and send them to the chosen model.
- View the generated response from the AI model.
- Keep a history of past prompts for easy re-use.


## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- PyQt5 library installed
- openai library installed (for making requests to the OpenAI API)

## Installation
To use the GPT Turbo Prompter, clone the repository to your local machine and install the dependencies if you haven't already by running the following commands:

```bash
git clone https://github.com/LMBooth/ChatGPT-pyqt-prompter.git
cd gpt-turbo-prompter
pip install PyQt5
pip install openai
```

## Usage
To start using the GPT Turbo Prompter, follow these steps:

1. Set your OpenAI API Key.
    - You can do this by clicking the "Set API Key" button within the application.
    - The key can also be provided through an environment variable named `OPENAI_API_KEY`.
2. Choose the desired model from the dropdown menu.
3. Input your prompt into the provided text area.
4. Click the "Send" button to get the response from the AI.
5. View the response text in the read-only text area below the send button.
6. Re-use prompts from your history by selecting them from the history dropdown.

## Running the Application
To run the application, navigate to the application's directory and execute:

```bash
python main.py
```
(This assumes that `main.py` is the main program file.)

## Contributing
Contributions to the GPT Turbo Prompter are welcome. If you have a suggestion that would make this better, please fork the repo and create a pull request.

## License
Please ensure that you comply with the OpenAI API License Agreement when using this application.

## Acknowledgements
- This project utilizes the OpenAI API; make sure to adhere to their usage policies.
- Thanks to the PyQt5 community for the excellent tools that make such applications possible.


> Note: This README assumes that the application's main file is `main.py`, please adjust the `Running the Application` section according to the real entry point of your application.
```

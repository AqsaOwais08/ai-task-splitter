#AI Task Splitter

Paste a client project brief and get back a structured task breakdown: main tasks, sub-tasks, priorities, and time estimates.


## Why I built this

This project focuses on turning the client's brief into four important categories i.e. main tasks, subtasks, priorities and time estimates.
I build this tool to aid in tasks you don't understand where to start from. so just paste a brief, and the tool will tell you the proper breakdown of the complete work process.

## Features

- Turns a plain-text project brief into main tasks and sub-tasks
- Assigns a priority and a time estimate to each task
- Uses structured output, so the results come back in a consistent format every time
- Simple web interface built with Streamlit

## Built with

- Python
- Google Gemini API
- Pydantic (defines the structure of the output)
- Streamlit (the web interface)

## How to run it

1. Clone the repo
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-task-splitter.git
   cd ai-task-splitter
   ```
2. Install the packages
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gemini API key: copy `.env.example` to `.env` and put your key in it
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Start the app
   ```bash
   streamlit run app.py
   ```

Requires Python 3.10+.

## What I learned

I actually started this project with Openai in mind. But then I switched to Gemini. And because of these API errors, I actually learnt how to tackle them.

## Possible improvements

- Making a export tool in file format.
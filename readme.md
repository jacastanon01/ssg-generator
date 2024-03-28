# Markdown Static Site Generator

## Project Overview

This program takes a directory, converts the Markdown files to HTML and generates static pages on the server to serve to the client. The pages to convert are located in the `content` folder in the root directory and each sub-directory is treated as a new route.

### What I Learned

This project was my first larger project using Python and I enjoyed the learning curves that came with it. I am more comfortable using node to manage projects and learning how Python modules operate was an excellent exploration outside my comfort zone!
I prefer my projects to be organized into separate modules and quickly learned that Python treats each file as a module that can be instantiated once imported. This is why the conditonal `if __name__ == "__main__":` is commonly used. This prevents the module from being executed in unexpected places by explicitly checking where it was run. This was also my first foray with Python's standard `unittest` library and it made me be conscious of testing each piece before moving to the next task.

## How It Works

When you run `./main.sh`, a `generate_pages_recursive` function is called which copies files and sub-directories from the static directory into a new directory. If a Markdown file is found in the static directory, it is converted to an HTML page with all the matching nodes. The bulk of this logic is contained in [src/block_markdown.py](https://github.com/jacastanon01/ssg-generator/blob/main/src/block_markdown.py) where each 'block' of Markdown is converted according to its type and the text inside the block is handled seperately for inline text nodes.

## Unit Testing

Since this project contained many intertwined and moving parts, it was imperative to create tests for each specific task to ensure the expected output was being generated.

## Getting Started

This project uses Python version 3.12.1

### Clone the Repo

`git clone https://github.com/jacastanon01/ssg-generator.git`

### Running locally

Since this project only requires Python's standard library, no extra dependencies need to be added. To run locally, run `./main.sh` in the root directory to start the server at http://localhost:8888 and see the files from the `content` folder in the browser. You can add new routes by adding a sub-directory to the `content` folder and adding a Markdown file with the information you want displayed.

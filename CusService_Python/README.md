# Project: Customer Support System: Use ChatGPT to build a web-based system that can answer questions about a website.
[Week 2 HW1 - CS589 - Khoi Duong - 19610.pdf](https://github.com/MynameisKoi/CS589/blob/main/CusService_Python/Week%202%20HW%201%20-%20CS589%20-%20Khoi%20Duong%20-%2019610.pdf)

## Step 1: Implementation
### Step 1.1: Command Line Solution
Please follow this OpenAI document - Website Q&A with Embeddings to build an AI that can answer questions about a website.
#### 1.1.1 : Make it work on Jupyter Notebook
After this step, asking ChatGPT questions about the website will be hardcoded in Python programs running on Jupyter Notebook.
#### Step 1.1.2 : Make it work on your local machine.
Export the Python code from Jupyter Notebook and prove that it also works on your local machine, which is the final "Command Line Solution".

**Note:**
The following steps are to enhance the "Command Line Solution" to let users ask ChatGPT questions about the website through a web-based user interface running on Ubuntu.
### Step 1.2: Web-based Solution (Python Flask webserver)
Enhance the result of Step 1.1 to allow users to ask questions about the website using a browser. - Python based
#### Step 1.2.1: Study how to use Python to create a web-based interface to ChatGPT
**Note:**
The Python program should be run on Ubuntu
#### Step 1.2.2: Integrate the Python code created in Step 1.1 and Step 1.2.1 to a create a web-based interface to let the users ask ChatGPT questions about the website using a browser.
**Note:**
*There are 3 approaches for customers to use your system*
- Customers need to install your software
    - Command-based (i.e., Step 1.1)
    - GUI-based
- Customers does not need to install your software
    - Web-based (i.e., Step 1.2.2)
- Step 1.1 represents command-based python code, Step 1.2.1 represents web-based python code. What we want is to move the result of Step 1.1 to Step 1.2.1. There are two ways to do that
    - Move the code slowly
      - You move line by line from one python code (i.e. the one that is command-based) to the target python code (i.e., the one that is web-based). If a line works, then move to another line.
    - Move the code faster
      - Comparing one python code (i.e. the one that is command-based) with the target python code (i.e., the one that is web-based) and then determine how to improve the target code to have the behavior of the command-based Python code.

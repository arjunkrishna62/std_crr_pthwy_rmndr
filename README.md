# Student Career Pathway Recommender (LLM + Prompting) - assignment-2

This project helps students discover career paths based on their interests and academic strengths using language models and semantic search.

## It will do

1.Asks users about their interests and strong subjects.
2.Recommends 3 careers that match them.
3.Supports both OpenAI-based LLM and offline fallback logic.
4.Lets users explore more career options interactively.

# setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/std_crr_pthwy_rcmndr.git
cd std_crr_pthwy_rcmndr
## setup virtual enviroment
python -m venv venv
source venv/bin/activate  # mac/linux
venv\Scripts\activate     # for windows

## 3.install dpenedencies
pip install requirements.txt

## 4. Environment Variables
If you want to use OpenAI's LLM and Embeddings, create a .env file in the root folder
OPENAI_API_KEY=your_openai_api_key_here

## 5. make sure your setup is intact run the file assignment.py

### Example

Hi! I'm here to help you find career paths that match your interests and strengths. Let's get started!
What are some activities, subjects, or hobbies that you really enjoy? coding, doing math problems   
Great! Now, what subjects do you feel you excel in or enjoy the most at school? maths, cs, physics

Based on what you shared, here are some career paths you might enjoy:

 Software Developer: A career as a Software Developer fits your interests in coding, doing math problems and strengths in maths, cs, physics.
 Graphic Designer: A career as a Graphic Designer fits your interests in coding, doing math problems and strengths in maths, cs, physics.
 Writer: A career as a Writer fits your interests in coding, doing math problems and strengths in maths, cs, physics.

Would you like to learn more about any of these careers, or explore other options?
Type 1 to learn more about a career, 2 to explore more options, or 3 to exit: 1
Which career are you curious about? Type the career name: software developer

Here's more about Software Developer: They often work in fields involving coding, programming, technology, computers, and are strong in math, computer science.

Would you like to learn more about any of these careers, or explore other options?
Type 1 to learn more about a career, 2 to explore more options, or 3 to exit: 3
Thanks for using the career advisor. Goodbye!
(base) arjunkrishna@MacBook-Air std_crr_pthwy_rcmndr % 

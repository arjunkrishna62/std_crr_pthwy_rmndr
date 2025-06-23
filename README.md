# Student Career Pathway Recommender (LLM + Prompting) - assignment-2

This project helps students discover career paths based on their interests and academic strengths using language models and semantic search.

##� It will do

- Asks users about their **interests** and **strong subjects**.
- Recommends **3 careers** that match them.
- Supports both **OpenAI-based LLM** and **offline fallback logic**.
- Lets users explore **more career options** interactively.

---

## setup

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

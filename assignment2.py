import re
import os
import openai
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
load_dotenv()

from transformers import pipeline

from sentence_transformers import util

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

api_key = os.getenv("OPENAI_API_KEY")
# use_llm = False
use_llm = bool(api_key)
llm = OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY")) if use_llm else None


career_data = [
    {"career": "Software Developer", "keywords": ["coding", "programming", "technology", "computers"], "strengths": ["math", "computer science"]},
    {"career": "Graphic Designer", "keywords": ["art", "design", "creativity", "visual"], "strengths": ["art", "design"]},
    {"career": "Sports Coach", "keywords": ["sports", "coaching", "teamwork", "leadership"], "strengths": ["physical education", "psychology"]},
    {"career": "Environmental Scientist", "keywords": ["science", "nature", "experiments", "environment"], "strengths": ["science", "biology"]},
    {"career": "Writer", "keywords": ["writing", "stories", "creativity", "literature"], "strengths": ["english", "literature"]}
]
# embeddings = OpenAIEmbeddings()
embeddings = OpenAIEmbeddings(openai_api_key=api_key) if use_llm else None
career_texts = [" ".join(c["keywords"]) for c in career_data]
career_embeddings = model.encode(career_texts, convert_to_tensor=True)

# vector stoer
# vector_store = FAISS.from_texts(career_texts, embeddings)
if use_llm:
    vector_store = FAISS.from_texts(career_texts, embeddings)
else:
    vector_store = None

INTEREST_PROMPT = "Extract the main interests from the following response: {response}"
STRENGTH_PROMPT = "Extract the academic subjects the user is strong in from the following response: {response}"
EXPLANATION_PROMPT = "Explain why a career as a {career} might be a good fit for someone interested in {interests} and strong in {strengths}."

FALLBACK_INTEREST = "Can you tell me more about what you enjoy? For example, do you like solving problems, creating art, or maybe working with people?"
FALLBACK_STRENGTH = "Are there any subjects where you consistently do well or find interesting?"

def extract_info(prompt, response):
    if use_llm and llm:
        chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt))
        result = chain.run(response)
        return [word.strip().lower() for word in result.split(",") if word.strip()]
    else:
        return [word.strip().lower() for word in response.split(",") if word.strip()]


def mock_llm_response(career, interests, strengths):
    return f"A career as a {career} fits your interests in {', '.join(interests)} and strengths in {', '.join(strengths)}."

def llm_response(career, interests, strengths):
    if not use_llm:
        return mock_llm_response(career, interests, strengths)
    prompt = PromptTemplate.from_template(EXPLANATION_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(career=career, interests=", ".join(interests), strengths=", ".join(strengths))


# def extract_info(prompt, response):
#     chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template(prompt))
#     result = chain.run(response)
#     return result.split(", ") if result else []

#     career_scores = {}
#     for doc in interest_matches:
#         career_index = career_texts.index(doc.page_content)
#         career = career_data[career_index]
#         score = 0
#         score += len(set(career["keywords"]) & set(interests))
#         score += len(set(career["strengths"]) & set(strengths))
#         career_scores[career["career"]] = score
    

#     top_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)[:3]
#     # return [career_data[career_texts.index(" ".join(next(c["keywords"] for c in career_data if c["career"] == career)))] for career, _ in top_careers]
#     return [word.strip() for word in response.split(",")]

def recommendations(interests, strengths):
    if not use_llm or not vector_store:
        query = " ".join(interests)
        query_embedding = model.encode(query, convert_to_tensor=True)
        similarities = util.pytorch_cos_sim(query_embedding, career_embeddings)[0]
        top_k = similarities.topk(3)
        top_careers = [career_data[idx] for idx in top_k.indices]
        return top_careers
    

    interest_query = " ".join(interests)
    interest_matches = vector_store.similarity_search(interest_query, k=5)

    career_scores = {}
    for doc in interest_matches:
        career_index = career_texts.index(doc.page_content)
        career = career_data[career_index]
        score = 0
        # intrst mathc
        score += len(set(career["keywords"]) & set(interests))
        # strngth match
        score += len(set(career["strengths"]) & set(strengths))
        career_scores[career["career"]] = score
    
    top_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    return [career_data[career_texts.index(" ".join(next(c["keywords"] for c in career_data if c["career"] == career)))] for career, _ in top_careers]


# def recommendations(interests, strengths):
#     query = " ".join(interests)
#     query_embedding = model.encode(query, convert_to_tensor=True)

#     similarities = util.pytorch_cos_sim(query_embedding, career_embeddings)[0]
#     top_k = similarities.topk(3)

#     top_careers = []
#     for idx in top_k.indices:
#         career = career_data[idx]
#         top_careers.append(career)

#     return top_careers

# crr agent

def career_agent():
    print("Hi! I'm here to help you find career paths that match your interests and strengths. Let's get started!")
    
    interest_response = input("What are some activities, subjects, or hobbies that you really enjoy? ")
    interests = extract_info(INTEREST_PROMPT, interest_response)
    if not interests or len(interests) == 1 and not interests[0]:
        print(FALLBACK_INTEREST)
        interest_response = input()
        interests = extract_info(INTEREST_PROMPT, interest_response)
    
    strength_response = input("Great! Now, what subjects do you feel you excel in or enjoy the most at school? ")
    strengths = extract_info(STRENGTH_PROMPT, strength_response)
    if not strengths or len(strengths) == 1 and not strengths[0]:
        print(FALLBACK_STRENGTH)
        strength_response = input()
        strengths = extract_info(STRENGTH_PROMPT, strength_response)
    
    recommended_careers = recommendations(interests, strengths)
    # print("\nBased on what you've shared, here are three career paths that might be perfect for you:")
    # for career in recommended_careers:
    #     explanation = llm(EXPLANATION_PROMPT.format(career=career["career"], interests=", ".join(interests), strengths=", ".join(strengths)))
    #     print(f"- **{career['career']}**: {explanation}")
    print("\nBased on what you shared, here are some career paths you might enjoy:\n")
    for rec in recommended_careers:
        explanation = llm_response(rec["career"], interests, strengths)
        print(f" {rec['career']}: {explanation}")

    # print("\nWould you like to explore more paths?")

    
    # print("\nWould you like to learn more about any of these careers, or perhaps explore other options?")

    # followup = input("Type 1 to learn more about a career, 2 to explore more options, or 3 to exit: ")

    # if followup == "1":
    #     print("Which career are you curious about?")
    # elif followup == "2":
    #     print("Sure, let’s find more careers based on your expanded interests.")
    # else:
    #     print("Thanks for using the career advisor. Goodbye!")
    while True:
        print("\nWould you like to learn more about any of these careers, or explore other options?")
        followup = input("Type 1 to learn more about a career, 2 to explore more options, or 3 to exit: ")

        if followup == "1":
            choice = input("Which career are you curious about? Type the career name: ").strip().lower()
            found = False
            for rec in recommended_careers:
                if rec["career"].lower() == choice:
                    print(f"\nHere's more about {rec['career']}: They often work in fields involving {', '.join(rec['keywords'])}, and are strong in {', '.join(rec['strengths'])}.")
                    found = True
            if not found:
                print("Sorry, I couldn't find that career. Please try again.")
        elif followup == "2":
            print("Sure, let's go again!\n")
            return career_agent()
        elif followup == "3":
            print("Thanks for using the career advisor. Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    career_agent()
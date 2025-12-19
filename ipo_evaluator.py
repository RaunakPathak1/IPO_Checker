from Utilities.utils import dhrp_doc_collection
from Utilities.parameter_utils import eval_parameters,eval_questions
from tools.query_vector_database_tool import rag_pipeline
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

open_router_key = os.getenv("OPENROUTER_API_KEY", "")
if not open_router_key :
    print('OpenRouter key not found.')
else:
    print('OpenRouter key found.')

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-3-flash-preview"
openrouter = OpenAI(api_key=open_router_key, base_url=BASE_URL)

# open_router_key = os.getenv("OPENROUTER_API_KEY", "")
# if not open_router_key:
#     raise ValueError("OPENROUTER_API_KEY environment variable is not set.")
# BASE_URL = "https://openrouter.ai/api/v1"
# MODEL = "google/gemini-3-flash-preview"
# openrouter = OpenAI(api_key=open_router_key, base_url=BASE_URL)

def call_llm(MODEL, system_message, user_message):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    response = openrouter.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content


def ipo_rag_answerer(parameters,vector_collection = dhrp_doc_collection):
    results = []
    results.append(rag_pipeline(parameters, vector_collection))
    return results


def ipo_evaluator(company_questions, ideal_answers):

    results = []

    for i in range(len(company_questions)):

        topics = list(company_questions[i].keys())
        # questions = company_questions[i].values()

        company_answer = ipo_rag_answerer([company_questions[i]])[0].values()

        for topic, company_answer in zip(topics, company_answer):
            # print(f"Topic: {topic}, Answer: {company_answer}")
            results.append({topic: company_answer})


        ideal_answer = ideal_answers[i]
        print(ideal_answer)
        results.append({"ideal_answer": ideal_answer})

        ipo_expert_prompt = '''You are an expert IPO analyst.
                        Evaluate the company answer against the ideal answer and provide a score from 1 to 10, where 10 indicates a perfect match.  
                        Consider accuracy, completeness, relevance, clarity, and depth of analysis in your evaluation.
                        Provide only score and nothing else. 
                        '''
        
        evaluation_prompt = f'''Evaluate the following company answer against the ideal answer.\n\n
                            Topic: {topic}\n\n
                            Company Answer: {company_answer}\n\n
                            Ideal Answer: {ideal_answer}\n\n
                            Understand the Company Answer and give the result a score from 1 to 10.
                            Only provide the score as a number from 1 to 10.'''
        
        evaluation = call_llm(MODEL, ipo_expert_prompt, evaluation_prompt)
        results.append({"evaluation_score": evaluation})
    return results


def avg_score(evaluation_result):
    total_score = 0
    count = 0

    for item in evaluation_result:
        if "evaluation_score" in item:
            try:
                score = int(item["evaluation_score"])
                total_score += score
                count += 1
            except ValueError:
                print(f"Invalid score format: {item['evaluation_score']}")

    average = total_score / count if count > 0 else 0
    return average  


def ipo_result(ipo_name):
    evaluation_result = ipo_evaluator(eval_questions, eval_parameters)
    average_score = avg_score(evaluation_result)
    result_summary = {
        "IPO Name": ipo_name,
        "Average Evaluation Score": average_score,
        "Detailed Evaluation": evaluation_result
    }
    return result_summary


print(ipo_result('KSH'))

from Utilities.utils import dhrp_doc_collection,call_llm,MODEL
from Utilities.parameter_utils import eval_parameters,eval_questions
from tools.query_vector_database_tool import rag_pipeline
from openai import OpenAI
import os
from dotenv import load_dotenv


#dict implementation

def ipo_evaluator(company_questions, ideal_answers,vector_collection = dhrp_doc_collection):
    """
    Evaluates RAG performance. 
    company_questions: List of dicts e.g., [{"risk": "What are the risks?"}]
    ideal_answers: List of strings/dicts corresponding to the questions
    """
    final_report = []

    company_answers = rag_pipeline(company_questions,vector_collection)
    
    for key,value in ideal_answers.items():
        ideal_answer = ideal_answers[key]
        # print(ideal_answer)
        company_answer = company_answers[key]
        # print(company_answer)

        #  Preparing Evaluation Prompt
        ipo_expert_prompt = '''You are an expert IPO analyst.
                        Evaluate the company answer against the ideal answer and provide a score from 1 to 10, where 10 indicates a perfect match.  
                        Consider accuracy, completeness, relevance, clarity, and depth of analysis in your evaluation.
                        Provide only score and nothing else. 
                        '''
            
        evaluation_prompt = f"""
            Topic: {key}
            Actual Answer: {company_answer}
            Ideal Answer: {ideal_answer}
            Score the Actual Answer against the Ideal Answer (1-10).
            Only provide the score as a number from 1 to 10.
            """
        
        score_raw = call_llm(MODEL, ipo_expert_prompt, evaluation_prompt)

        # 3. Store Results
        final_report.append({
                "topic": key,
                "rag_answer": company_answer,
                "ideal_answer": ideal_answer,
                "score": score_raw.strip()
            })
            
    return final_report


def avg_score(evaluation_result):
    total_score = 0
    count = 0

    for item in evaluation_result:
        if "score" in item:
            try:
                score = int(item["score"])
                total_score += score
                count += 1
            except ValueError:
                print(f"Invalid score format: {item['score']}")

    average = total_score / count if count > 0 else 0
    return average 


# --- Gradio UI Wrapper ---
def run_ui_eval(ipo_name):
    # This is a placeholder for how you'd trigger it in the UI
    # In a real scenario, you'd fetch 'eval_questions' based on the ipo_name
    results = ipo_evaluator(eval_questions, eval_parameters,dhrp_doc_collection)
    avg = avg_score(results)
    return {"Average Score": avg, "Details": results}

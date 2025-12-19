import json
from Utilities.utils import embedding_model, dhrp_doc_collection, MODEL, call_llm


def get_relevant_docs(question, collection, top_k=5):
    print('reteriving sentence documents for company...')

    embedded_question = embedding_model.encode(question)
    print(f"Embedded question:")

    results = dhrp_doc_collection.query(
            query_embeddings=[embedded_question],
            n_results=top_k
            )
        # display(f"Top {top_k} relevant documents for question '{question}':{results}\n")
    return results


def build_context_json(documents):
    print('building context in JSON...')

    docs = documents.get("documents", [[]])[0]      
    metadatas = documents.get("metadatas", [[]])[0]

    context_list = []

    for doc, meta in zip(docs, metadatas):
        entry = {
            "source": meta.get("source", "unknown_source.txt").replace(".txt", ""),
            "page": meta.get("page", "Unknown page"),
            "content": doc.strip()
        }
        context_list.append(entry)

    return json.dumps({"context_results": context_list}, indent=4, ensure_ascii=False)

def rag_pipeline(parameters, collection):

    answers = {}
    for questions in parameters :

        for key, question in questions.items() :
            documents = get_relevant_docs(question, collection)
            context_json = build_context_json(documents)
        

            system_message = f'''You are a Senior IPO Investment Analyst and SEBI-registered Research Analyst equivalent. 
                Use Indian IPO Draft Red Herring Prospectus (DRHP) documents to answer the questions accurately.
                
                Use the following context to answer the questions.\n\nContext:\n
                {context_json}'''
          
            # print(f'system_message prepared.{system_message}')

            answer = call_llm(MODEL,system_message,question)
            print('llm answers')
            answers[key] =answer

    return answers

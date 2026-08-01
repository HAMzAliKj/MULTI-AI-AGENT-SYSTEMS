from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
import json
from apify_client import ApifyClient
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

client = ApifyClient("PASTE YOUR API KEY HERE")
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash ", api_key="PASTE YOUR API KEY HERE ")

class Global_Variable(TypedDict):
    read_pdf : str
    titles : list
    job : str
    result : str

def get_cv_text(state : Global_Variable):
    read_pdf = PyPDFLoader("hamza cv pdf.pdf").load()
    state["read_pdf"] = str(read_pdf[0])

    prompt = """
You are an expert AI Recruiter and LinkedIn Job Search Specialist.

Your task is to read the candidate's CV and determine which LinkedIn jobs best match their profile.

CV:
{cv_text}

Analyze:

• Technical skills
• Programming languages
• AI frameworks
• Cloud tools
• Databases
• Projects
• Years of experience (estimate if not explicitly stated)
• Seniority level
• Strongest domains

Then generate LinkedIn search job titles.

Rules:
- Use real LinkedIn job titles.
- Include both broad and specific titles.
- Rank titles from best match to least match.
- Do not include titles requiring skills absent from the CV.
- Maximum 15 titles.
- Return JSON only.

Return exactly:

{{
  "titleSearch": []
}}

give titleSearch 4 to 6 keyword

give that in json format
"""

    template = PromptTemplate(
        input_variables=["cv_text"],
        template=prompt,
    )

    chain = template | model 
    result = chain.invoke({"cv_text":read_pdf[0]}).content
    # Your LLM response
    text = result.strip()

    # Remove markdown fences
    text = text.replace("```json", "").replace("```", "").strip()

    # Convert JSON string to Python dict
    result = json.loads(text)

    # Now this works
    titles = result["titleSearch"]



    print(titles)
    state["titles"] = titles
    return state

# %%
def search_job(state : Global_Variable):
    run_input = {
        "timeRange": "7d",
        "limit": 20,
        # "removeAgency": True,
        "titleSearch": state["titles"],
        "locationSearch": [],
        "excludeATSDuplicate": True,
        # "populateAiRemoteLocation": True,
        # "populateAiRemoteLocationDerived": True,
    }

    run = client.actor("vIGxjRrHqDTPuE6M4").call(run_input=run_input)
    dataset = client.dataset(run.default_dataset_id)
    jobs = []

    for item in dataset.iterate_items():
        jobs.append({
            "title": item.get("title"),
            "date_posted": item.get("date_posted"),
            "organization": item.get("organization"),
            "company": item.get("organization"),
            "experience": item.get("ai_experience_level"),
            "remote": item.get("ai_work_arrangement"),
            "skills": item.get("ai_key_skills"),
            "requirements": item.get("ai_requirements_summary"),
            "url": item.get("url"),
            "ai_key_skills": item.get("ai_key_skills"),
        })
    print(jobs)   

    state["job"] = jobs
    return state

# %%
def llm_suggest(state : Global_Variable):
    prompt_of_job = """
You are an expert AI Career Advisor and LinkedIn Job Search Specialist.

Your goal is to help the candidate quickly decide WHICH jobs to apply for.

You will receive:

1. Candidate CV
2. A list of LinkedIn jobs

CV:
{cv_text}

Jobs:
{jobs}

-------------------------------------------------
TASK
-------------------------------------------------

Read the CV first.

Compare EVERY job against the CV.

Do NOT stop after finding only 2 or 3 matches.

Go through ALL jobs.

Return EVERY reasonably relevant job (maximum 20).

Sort from BEST MATCH to LOWEST MATCH.

-------------------------------------------------
IMPORTANT
-------------------------------------------------

Think like a human recruiter.

Prioritize:

• Skills match
• Projects match
• Technologies match
• Experience level
• Remote/Hybrid
• Entry-level or Junior roles

Do NOT reject a job only because it asks for 2-3 years experience if the candidate's projects strongly compensate.

Ignore jobs that are clearly unrelated.

-------------------------------------------------
FORMAT
-------------------------------------------------

For EVERY selected job use EXACTLY this format.


1. 🟢 Job Title — Company

📍 Location | Remote/Hybrid/On-site | Posted: <date>

💼 Experience: <experience>

🔗 Apply: <url>

⭐ Match Score: XX%

Why it matches:

Write ONLY 3-6 short sentences.

Mention the EXACT skills that match.

Example:

• LangChain ✅
• LangGraph ✅
• RAG ✅
• Python ✅
• FastAPI ✅
• Vector Databases (FAISS/Pinecone/Qdrant) ✅
• OpenAI APIs ✅

Mention candidate projects if relevant.

Finish with ONE recommendation sentence.

Examples:

"This should be one of your first applications."

"Excellent match."

"Worth applying even if experience is slightly higher."

"Good stretch opportunity."

-------------------------------------------------
RULES
-------------------------------------------------

❌ Don't write an introduction.

❌ Don't summarize the CV.

❌ Don't explain your reasoning.

❌ Don't write career advice.

❌ Don't write a conclusion.

ONLY output the ranked jobs.

Return as many matching jobs as possible (up to 20).
"""

    template_of_job = PromptTemplate(
        input_variables=["cv_text", "jobs"],
        template=prompt_of_job,
    )

    new_chain = template_of_job | model

    res = new_chain.invoke({"cv_text":state["read_pdf"],"jobs":state["job"]}).content
    state["result"] = res

    return state

# %%
workflow = StateGraph(Global_Variable)

# %%
workflow.add_node("get_cv_text",get_cv_text)
workflow.add_node("search_job",search_job)
workflow.add_node("llm_suggest",llm_suggest)

workflow.add_edge(START,"get_cv_text")
workflow.add_edge("get_cv_text","search_job")
workflow.add_edge("search_job","llm_suggest")
workflow.add_edge("llm_suggest",END)

# %%
graph = workflow.compile()


# %%
result = graph.invoke({"input":""})

# %%
# result['result']

from IPython.display import display , Markdown

display(Markdown(result['result']))


from flask import Flask, render_template, request, jsonify
import os
import json

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

from apify_client import ApifyClient

from langgraph.graph import StateGraph, START, END
from typing import TypedDict


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


client = ApifyClient("PASTE YOUR API")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key="paste your api key "
)


uploaded_pdf_path = None
uploaded_cv_text = None


class Global_Variable(TypedDict):

    read_pdf: str

    titles: list

    job: str

    result: str

# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_pdf():

    global uploaded_pdf_path
    global uploaded_cv_text

    if "pdf" not in request.files:
        return jsonify({
            "success": False,
            "message": "No PDF uploaded."
        })

    pdf = request.files["pdf"]

    if pdf.filename == "":
        return jsonify({
            "success": False,
            "message": "Please select a PDF."
        })

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        pdf.filename
    )

    pdf.save(save_path)

    uploaded_pdf_path = save_path

    loader = PyPDFLoader(uploaded_pdf_path)

    pages = loader.load()

    uploaded_cv_text = "\n".join(
        page.page_content for page in pages
    )

    return jsonify({

        "success": True,

        "message": "CV uploaded successfully.",

        "cv_text": uploaded_cv_text

    })


def get_cv_text(state: Global_Variable):

    global uploaded_pdf_path
    global uploaded_cv_text

    if uploaded_pdf_path is None:
        raise Exception("No CV uploaded.")

    read_pdf = PyPDFLoader(uploaded_pdf_path).load()

    state["read_pdf"] = uploaded_cv_text

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

give titleSearch 4 to 6 keyword just 5 to 6 keyword not lenghy 

give that in json format
"""

    template = PromptTemplate(
        input_variables=["cv_text"],
        template=prompt,
    )

    chain = template | model

    result = chain.invoke({
        "cv_text": uploaded_cv_text
    }).content

    text = result.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    result = json.loads(text)

    titles = result["titleSearch"]

    print("Generated Titles:")
    print(titles)

    state["titles"] = titles

    return state


# =====================================================
# SEARCH JOBS
# =====================================================

def search_job(state: Global_Variable):

    run_input = {

        "timeRange": "7d",

        "limit": 20,

        "titleSearch": state["titles"],

        "locationSearch": [],

        "excludeATSDuplicate": True,

    }
    run = client.actor("vIGxjRrHqDTPuE6M4").call(run_input=run_input)
    dataset = client.dataset(run.default_dataset_id)
    jobs = []

    # run = client.actor("vIGxjRrHqDTPuE6M4").call(
    #     run_input=run_input
    # )

    # dataset = client.dataset(run.default_dataset_id)

    # jobs = []

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

    print("Jobs Found:", len(jobs))

    state["job"] = jobs

    return state


# =====================================================
# GEMINI MATCHING
# =====================================================

def llm_suggest(state: Global_Variable):

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

Read the CV first.

Compare EVERY job against the CV.

Return EVERY reasonably relevant job (maximum 20).

Sort from BEST MATCH to LOWEST MATCH.

For EVERY selected job use EXACTLY this format.

1. 🟢 Job Title — Company

📍 Location | Remote/Hybrid | Posted: <date>

💼 Experience: <experience>

🔗 Apply: <url>

⭐ Match Score: XX%

Why it matches:

Write ONLY 3-6 short sentences.

Mention exact matching skills.

Finish with one recommendation sentence.

ONLY output ranked jobs.

No introduction.

No conclusion.
"""

    template = PromptTemplate(

        input_variables=["cv_text", "jobs"],

        template=prompt_of_job,

    )

    chain = template | model

    response = chain.invoke({

        "cv_text": state["read_pdf"],

        "jobs": state["job"]

    }).content

    state["result"] = response

    return state


# =====================================================
# LANGGRAPH
# =====================================================

workflow = StateGraph(Global_Variable)

workflow.add_node("get_cv_text", get_cv_text)

workflow.add_node("search_job", search_job)

workflow.add_node("llm_suggest", llm_suggest)

workflow.add_edge(START, "get_cv_text")

workflow.add_edge("get_cv_text", "search_job")

workflow.add_edge("search_job", "llm_suggest")

workflow.add_edge("llm_suggest", END)

graph = workflow.compile()

# =====================================================
# SEARCH ROUTE
# =====================================================

@app.route("/search", methods=["POST"])
def search():

    global uploaded_pdf_path

    if uploaded_pdf_path is None:

        return jsonify({
            "success": False,
            "message": "Please upload a CV first."
        })

    try:

        result = graph.invoke({

            "read_pdf": "",
            "titles": [],
            "job": [],
            "result": ""

        })

        return jsonify({

            "success": True,

            "result": result["result"]

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        })


# =====================================================
# RUN FLASK
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )

    

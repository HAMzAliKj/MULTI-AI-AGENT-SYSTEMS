I built something that actually saves time while job hunting 👇

𝗟𝗶𝗻𝗸𝗲𝗱𝗜𝗻 𝗔𝗜 𝗝𝗼𝗯 𝗥𝗲𝘀𝗲𝗮𝗿𝗰𝗵𝗲𝗿 — upload your CV, and it finds + ranks the best LinkedIn jobs for you automatically.

<img width="671" height="440" alt="image" src="https://github.com/user-attachments/assets/e90637ad-97cb-4d4e-914a-c655b6901a40" />
<img width="131" height="432" alt="image" src="https://github.com/user-attachments/assets/46524a79-0ade-4322-9bd9-a349b61bf892" />



Here's what's running under the hood:

🔷 LangGraph — orchestrates the whole pipeline as a state graph (3 nodes, clean flow)
🔷 Gemini 2.5 Flash — reads your CV, extracts your skills, and generates the exact job titles to search
🔷 Apify — scrapes real LinkedIn job listings live
🔷 Gemini again — compares every job against your profile and ranks them with a match score + reason why

The whole thing is one Streamlit app. Upload PDF → AI thinks → jobs appear. No manual searching.

Stack:
→ Python
→ LangChain + LangGraph
→ Gemini 2.5 Flash (via langchain-google-genai)
→ Apify Linke

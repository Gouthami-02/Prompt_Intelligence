import os
import json

from django.shortcuts import render
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def home(request):

    result = {}

    if request.method == "POST":

        prompt = request.POST.get("prompt")

        try:

            response = model.generate_content(f"""
You are an expert Prompt Engineer.

Analyze the following prompt.

Prompt:
{prompt}

Return ONLY valid JSON.

Example:

{{
    "optimized_prompt":"Write a detailed Python program...",
    "quality_score":85,
    "category":"Coding",
    "suggestions":[
        "Add input format",
        "Mention output",
        "Specify constraints",
        "Provide an example"
    ]
}}

Return ONLY JSON.
""")

            result = json.loads(response.text)

        except Exception as e:

            result = {
                "optimized_prompt": "Error",
                "quality_score": 0,
                "category": "Error",
                "suggestions": [str(e)]
            }

    return render(request, "home.html", {"result": result})

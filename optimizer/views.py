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

            Score the prompt using these rules:

            90-100 = Excellent (Very detailed, clear, specific)
            70-89 = Good (Mostly clear but missing a few details)
            50-69 = Average (Basic prompt with some missing information)
            30-49 = Poor (Very vague)
            0-29 = Very Poor (Almost no information)

            Return ONLY valid JSON in this format:

            {{
               "optimized_prompt": "",
               "quality_score": 85,
               "category": "",
               "suggestions": [
                  "Suggestion 1",
                  "Suggestion 2",
                  "Suggestion 3",
                  "Suggestion 4"
                ]
            }}

             Return ONLY JSON. Do not include markdown (```json) or explanations.
             """)

            print(response.text)
            
            clean_text = response.text.strip()

            if clean_text.startswith("```json"):
             clean_text = clean_text.replace("```json", "", 1)

            if clean_text.endswith("```"):
              clean_text = clean_text[:-3]

            clean_text = clean_text.strip()

            result = json.loads(clean_text)
        except Exception as e:

            result = {
                "optimized_prompt": "Error",
                "quality_score": 0,
                "category": "Error",
                "suggestions": [str(e)]
            }

    return render(request, "home.html", {"result": result})

import os

from django.shortcuts import render

from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-2.5-flash")


def home(request):

    optimized_prompt = ""

    if request.method == "POST":

        prompt = request.POST.get("prompt")

        try:
            response = model.generate_content(
              f"""
               You are an AI Prompt Engineer.

                Analyze the following prompt.

                Prompt:
                  {prompt}

                 Return the result in this format:

                 Optimized Prompt:
                 ...

                 Quality Score:
                 /100

                 Category:
                   ...

                 Suggestions:
                 1.
                 2.
                 3.
                 4.

                 """
                 )

            optimized_prompt = response.text

        except Exception as e:
            optimized_prompt = f"Error: {e}"

    return render(
        request,
        "home.html",
        {"optimized_prompt": optimized_prompt},
    )

import os
import json

from django.shortcuts import render,redirect
from .models import PromptHistory
from dotenv import load_dotenv
import google.generativeai as genai
from django.db.models import Avg,Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .pdf_utils import create_pdf


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

@login_required
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
            PromptHistory.objects.create(
               user= request.user,
               original_prompt=prompt,
               optimized_prompt=result["optimized_prompt"],
               quality_score=result["quality_score"],
               category=result["category"]
            )
        except Exception as e:

            result = {
                "optimized_prompt": "Error",
                "quality_score": 0,
                "category": "Error",
                "suggestions": [str(e)]
            }

    return render(request, "home.html", {"result": result})
@login_required
def history(request):

    search = request.GET.get("search")

    prompts = PromptHistory.objects.filter(user=request.user)

    if search:
        prompts = prompts.filter(
            original_prompt__icontains=search
        )

    prompts = prompts.order_by("-created_at")

    return render(
        request,
        "history.html",
        {
            "prompts": prompts,
            "search": search
        }
    )


@login_required
def dashboard(request):

    prompts = PromptHistory.objects.filter(user=request.user)

    total_prompts = prompts.count()

    average_score = prompts.aggregate(
        Avg("quality_score")
    )["quality_score__avg"]

    total_categories = prompts.values(
        "category"
    ).distinct().count()

    recent_prompts = prompts.order_by("-created_at")[:5]

    context = {
        "total_prompts": total_prompts,
        "average_score": round(average_score or 0),
        "total_categories": total_categories,
        "recent_prompts": recent_prompts,
    }

    return render(request, "dashboard.html", context)
@login_required
def export_pdf(request):

    latest = PromptHistory.objects.filter(
        user=request.user
    ).last()

    if not latest:
        return HttpResponse("No prompt found.")

    filepath = "prompt_report.pdf"

    data = {
        "original_prompt": latest.original_prompt,
        "optimized_prompt": latest.optimized_prompt,
        "quality_score": latest.quality_score,
        "category": latest.category,
        "suggestions": [
            "Review the optimized prompt.",
            "Add more context if needed.",
            "Use examples for better results.",
            "Test the prompt with AI."
        ]
    }

    create_pdf(filepath, data)

    with open(filepath, "rb") as pdf:
        response = HttpResponse(
            pdf.read(),
            content_type="application/pdf"
        )
        response["Content-Disposition"] = 'attachment; filename="Prompt_Report.pdf"'
        return response
    
@login_required
def delete_prompt(request, id):

    prompt = PromptHistory.objects.get(id=id, user=request.user)

    prompt.delete()

    return redirect("history")



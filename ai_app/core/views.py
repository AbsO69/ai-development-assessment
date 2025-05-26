import requests
from django.conf import settings
from django.shortcuts import render
import json

def home(request):
    ai_response = ""
    full_api_response = ""
    request_payload = ""

    if request.method == "POST":
        user_idea = request.POST.get("prompt")

        prompt = (
            "You are a startup mentor evaluating a new idea. "
            "Here is the idea:\n"
            f"{user_idea}\n\n"
            "Evaluate the idea based on the following:\n"
            "- Does it solve a real problem?\n"
            "- Is it scalable or innovative?\n"
            "- Is it clearly explained?\n\n"
            "Reply with:\n"
            "Verdict: ✅ Promising or ❌ Needs Work\n"
            "Explanation: (1–2 bullet points)\n"
            "Suggestion (optional): One suggestion for improvement."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={settings.GOOGLE_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        request_payload = json.dumps(payload, indent=2)
        print("Gemini Request Payload:", request_payload)

        try:
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            full_api_response = json.dumps(data, indent=2)
            print("Gemini API Response:", full_api_response)

            if "candidates" in data and data["candidates"]:
                parts = data['candidates'][0].get('content', {}).get('parts', [])
                for part in parts:
                    if 'text' in part:
                        ai_response += part['text'] + "\n"
            else:
                ai_response = f"❌ Error from Gemini API: {data.get('error', {}).get('message', 'Unknown error')}"

        except Exception as e:
            ai_response = f"❌ Exception: {str(e)}"

    return render(request, "home.html", {
        "ai_response": ai_response.strip(),
        "full_api_response": full_api_response,
        "request_payload": request_payload,
    })


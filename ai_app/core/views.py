import requests
from django.conf import settings
from django.shortcuts import render

def home(request):
    ai_response = ""
    image_url = ""

    if request.method == "POST":
        prompt = request.POST.get("prompt")

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

        response = requests.post(url, headers=headers, json=payload)
        try:
            parts = response.json()['candidates'][0]['content']['parts']
            for part in parts:
                if 'text' in part:
                    ai_response += part['text'] + "\n"
                elif 'inlineData' in part and 'mimeType' in part and part['mimeType'].startswith("image/"):
                    image_url = f"data:{part['mimeType']};base64,{part['inlineData']['data']}"
        except Exception as e:
            ai_response = f"Error: {str(e)}"

    return render(request, "home.html", {
        "ai_response": ai_response.strip(),
        "image_url": image_url
    })

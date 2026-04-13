import json
from django.http import JsonResponse
from django.conf import settings
from books.models import Book
import google.generativeai as genai


genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-flash-latest")


def chat_with_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip().lower()

            if not user_message:
                return JsonResponse({"reply": "Please enter a message."})

            # 📚 DB SEARCH FIRST
            books = Book.objects.filter(
                title__icontains=user_message
            ) | Book.objects.filter(
                author__icontains=user_message
            ) | Book.objects.filter(
                category__name__icontains=user_message
            )

            books = list({b.id: b for b in books}.values())[:5]

            if books:
                reply = "\n".join([f"📖 {b.title} - ₹{b.price}" for b in books])
                return JsonResponse({"reply": f"📚 Found books:\n\n{reply}"})

            # 🤖 AI RESPONSE
            prompt = f"""
You are a bookstore assistant.

Rules:
- Only answer book-related questions
- Keep answers short and simple

User: {user_message}
"""

            response = model.generate_content(prompt)

            return JsonResponse({"reply": response.text})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request"})
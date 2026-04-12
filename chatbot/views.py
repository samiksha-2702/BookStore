import json
from django.http import JsonResponse
from books.models import Book
from django.conf import settings


def chat_with_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip().lower()

            if not user_message:
                return JsonResponse({"reply": "Please enter a message."})

            # 📚 SEARCH BOOKS
            books = Book.objects.filter(
                title__icontains=user_message
            ) | Book.objects.filter(
                author__icontains=user_message
            ) | Book.objects.filter(
                category__name__icontains=user_message
            )

            books = list({b.id: b for b in books}.values())[:5]

            if books:
                reply = "\n".join(
                    [f"📖 {b.title} - ₹{b.price}" for b in books]
                )
                return JsonResponse({"reply": f"📚 Found books:\n\n{reply}"})

            # 🤖 AI RESPONSE (NEW SDK)
            from google import genai

            client = genai.Client(api_key=settings.GEMINI_API_KEY)

            response = client.models.generate_content(
                model="gemini-1.5-pro",
                contents=f"""
You are a bookstore assistant for BiblioCart.

Only answer book-related queries.

User: {user_message}
"""
            )

            return JsonResponse({"reply": response.text})

        except Exception as e:
            print("CHATBOT ERROR:", e)
            return JsonResponse({"reply": f"⚠️ Error: {str(e)}"})

    return JsonResponse({"reply": "Invalid request"})
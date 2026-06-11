import json
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Count
from rest_framework import response

from books.models import Book
from google import genai

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

# 🧠 INTENT DETECTION

def get_intent(message):
    message = message.lower().strip()

    if any(word in message for word in ["hello", "hi", "hey"]):
        return "greeting"

    if any(word in message for word in ["thanks", "thank you", "thankyou"]):
        return "thanks"

    if any(word in message for word in ["bye", "goodbye", "see you"]):
        return "bye"

    if any(word in message for word in ["price", "cheap", "low", "budget"]): 
        return "low_price"

    if any(word in message for word in ["recommend", "suggest", "best"]):
        return "recommend"

    if any(word in message for word in ["similar", "more like", "like this","more like this"]):
        return "similar"

    return "general"



# 🤖 CHAT VIEW

def chat_with_bot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "Please enter a message."})

            intent = get_intent(user_message)

            
            # 💾 CHAT MEMORY (SESSION)
            
            chat_history = request.session.get("chat_history", [])
            chat_history.append({"user": user_message})
            chat_history = chat_history[-5:]
            request.session["chat_history"] = chat_history

            context = "\n".join([f"User: {m['user']}" for m in chat_history])

            
            # 👋 GREETING
            
            if intent == "greeting":
                return JsonResponse({
                    "reply": "👋 Hi! I can help you find books, recommendations, and authors."
                })

            
            # 🙏 THANK YOU
            
            if intent == "thanks":
                return JsonResponse({
                    "reply": "😊 You're welcome! Happy reading 📚"
                })

            
            # 👋 BYE
            
            if intent == "bye":
                return JsonResponse({
                    "reply": "👋 Bye! Come back anytime for book recommendations 📚"
                })

            
            # 💰 LOW PRICE BOOKS
            
            if intent == "low_price":
                books = Book.objects.all().order_by("price")[:5]

                reply = "\n".join([
                    f"📖 {b.title} - ₹{b.price}" for b in books
                ])

                return JsonResponse({
                    "reply": f"💰 Cheapest Books:\n\n{reply}"
                })

            
            # 🔁 SIMILAR BOOKS FEATURE
            
            if intent == "similar":
                books = Book.objects.all()[:1]

                if books:
                    book = books[0]

                    similar = Book.objects.filter(
                        category=book.category
                    ).exclude(id=book.id)[:5]

                    reply = "\n".join([
                        f"📖 {b.title} - ₹{b.price}" for b in similar
                    ])

                    return JsonResponse({
                        "reply": f"📚 Similar Books to {book.title}:\n\n{reply}"
                    })

            
            # 📚 DB SEARCH
            
            books = Book.objects.filter(
                title__icontains=user_message
            ) | Book.objects.filter(
                author__icontains=user_message
            ) | Book.objects.filter(
                category__name__icontains=user_message
            )

            books = list({b.id: b for b in books}.values())[:5]

            if books:
                reply = "\n".join([
                    f"📖 {b.title} - ₹{b.price}" for b in books
                ])

                return JsonResponse({
                    "reply": f"📚 Found Books:\n\n{reply}"
                })

            
            # 📊 SMART RECOMMENDATION (FALLBACK)
            
            if intent == "recommend":
                popular_books = Book.objects.annotate(
                    order_count=Count("orderitem")
                ).order_by("-order_count")[:5]

                reply = "\n".join([
                    f"📖 {b.title} - ₹{b.price}" for b in popular_books
                ])

                return JsonResponse({
                    "reply": f"🔥 Recommended Books:\n\n{reply}"
                })

            
            # 🤖 AI FALLBACK (ONLY IF NEEDED)
            
            prompt = f"""
You are BiblioCart AI bookstore assistant.

Conversation:
{context}

Current User Question:
{user_message}

RULES:
- Only answer book-related questions.
- If the question is unrelated to books, politely refuse.
- Keep answers short (2–3 lines).
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return JsonResponse({
                "reply": response.text
            })

        except Exception as e:
            return JsonResponse({
                "reply": f"⚠️ Error: {str(e)}"
            })

    return JsonResponse({"reply": "Invalid request"})
from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Book, Category

def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    # 🔍 Search
    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query)

    # 🏷️ Category filter
    category = request.GET.get('category')
    if category:
        books = books.filter(category_id=category)

    # 🔽 Sort
    sort = request.GET.get('sort')
    if sort == 'low':
        books = books.order_by('price')
    elif sort == 'high':
        books = books.order_by('-price')

    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories
    })

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_detail.html', {'book': book})
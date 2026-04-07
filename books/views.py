from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, Category

def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    query = request.GET.get('q')
    if query:
        books = books.filter(title__icontains=query)

    category = request.GET.get('category')
    if category:
        books = books.filter(category_id=category)

    sort = request.GET.get('sort')
    if sort == 'low':
        books = books.order_by('price')
    elif sort == 'high':
        books = books.order_by('-price')

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'books': page_obj,
        'categories': categories
    })

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books/book_detail.html', {'book': book})

def bestsellers(request):
    books = Book.objects.filter(is_bestseller=True)
    return render(request, 'books/bestseller.html', {'books': books})
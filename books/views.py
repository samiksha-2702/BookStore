from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, Category
from django.db.models import Q
from orders.models import OrderItem

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


    user = request.user

    if user.is_authenticated:
        ordered_books = OrderItem.objects.filter(
            order__user=user
        ).values_list('book_id', flat=True)

        categories_bought = Book.objects.filter(
            id__in=ordered_books
        ).values_list('category_id', flat=True)

        recommended_books = Book.objects.filter(
            Q(category_id__in=categories_bought) |
            Q(is_bestseller=True) |
            Q(new_arrival=True)
        ).exclude(id__in=ordered_books).distinct()[:8]

    else:
        recommended_books = Book.objects.filter(
            Q(is_bestseller=True) | Q(new_arrival=True)
        )[:8]

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_list.html', {
        'books': page_obj,
        'categories': categories,
        'recommended_books': recommended_books   
    })


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    user = request.user

    # STEP 1: user history (safe check)
    if user.is_authenticated:
        ordered_books = OrderItem.objects.filter(
            order__user=user
        ).values_list('book_id', flat=True)
    else:
        ordered_books = []


    # STEP 2: recommendation logic (FIXED)
    recommended_books = Book.objects.filter(
        Q(category_id=book.category_id) |
        Q(is_bestseller=True) |
        Q(new_arrival=True)
    ).exclude(
        id__in=ordered_books
    ).exclude(
        id=book.id
    ).distinct()[:6]

    print("Recommended:", recommended_books)

    return render(request, 'books/book_detail.html', {
        'book': book,
        'recommended_books': recommended_books
    })


def bestsellers(request):
    books = Book.objects.filter(is_bestseller=True)
    return render(request, 'books/bestseller.html', {'books': books})

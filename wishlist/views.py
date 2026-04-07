from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem
from books.models import Book
from django.http import JsonResponse   # ADD THIS IMPORT

@login_required(login_url='login/')
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        book=book
    )

    return redirect('book_detail', id=book.id)


@login_required
def remove_from_wishlist(request, book_id):
    wishlist = Wishlist.objects.get(user=request.user)
    book = get_object_or_404(Book, id=book_id)

    WishlistItem.objects.filter(wishlist=wishlist, book=book).delete()

    return redirect('wishlist')


@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.all()

    return render(request, 'wishlist/wishlist.html', {'items': items})

@login_required
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    item = WishlistItem.objects.filter(wishlist=wishlist, book=book)

    if item.exists():
        item.delete()
        return JsonResponse({'status': 'removed'})
    else:
        WishlistItem.objects.create(wishlist=wishlist, book=book)
        return JsonResponse({'status': 'added'})
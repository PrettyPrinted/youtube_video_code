from django.shortcuts import render
from django.core.paginator import Paginator 

from .models import Book

def index(request):
    books = Book.objects.all()

    book_paginator = Paginator(books, 20)

    page_num = request.GET.get('page')

    page = book_paginator.get_page(page_num)

    context = {
        'count' : book_paginator.count,
        'page' : page
    }
    return render(request, 'books/index.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from waganeko.models import Book, Explanation
import json
from django.db.models import Prefetch
# from waganeko.models import


@login_required
def mypage_top(request):
    user = request.user
    profile = user.profile

    explanation_list = list(Explanation.objects.select_related('post_for_book').filter(iine_nums__gt=0))

    book_id_list = []
    for explanation in explanation_list:
        book_id = explanation.post_for_book.id
        book_id_list.append(book_id)

    books = []
    for book_id in book_id_list:
        book = Book.objects.get(id=book_id)
        books.append(book)
    books = set(books)
    books = list(books)

    return render(request, 'waganeko/mypage.html', {'profile':profile, 'books':books}) #'assessments':myassessments

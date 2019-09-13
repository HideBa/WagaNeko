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
    print(explanation_list)
    print('hhhhhhhhhhh')

    book_id_list = []
    for explanation in explanation_list:
        book_id = explanation.post_for_book.id
        print(book_id)
        book_id_list.append(book_id)
    print('00000000')
    print(book_id_list)

    books = []
    print(type(books))
    for book_id in book_id_list:
        book = Book.objects.get(id=book_id)
        books.append(book)
    print(books)
    books = set(books)
    print(books)
    books = list(books)
    print(books)
    print("ここまでOK")


    # mylogs = ScoreLog.objects.filter(profile_id=profile.id)
    # myrooms = RentRoom.objects.filter(owner_id=profile.id)

    return render(request, 'waganeko/mypage.html', {'profile':profile, 'books':books}) #'assessments':myassessments
    # return render(request, 'iekari/mypage.html', {'profile':profile,'logs':mylogs,'rooms':myrooms}) #'assessments':myassessments

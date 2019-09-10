from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required #追加！
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from waganeko.new_explanation_form import NewExplanationForm


from django.core.paginator import Paginator
from waganeko.models import Book, ScoreLog, Explanation

import random

form_invalid_message = '不正な入力が送信されました'
submit_successful_message = 'ツイートされました。！'
message_rate_created = '評価が登録されました！'
message_rate_updated = '評価が更新されました！'

def list_search_view(request):
    var = request.GET
    search_str = var.get('search')
    # if Book.objects.filter(Q(book_name__icontains=search_str) | Q(book_name_hiragana__icontains=search_str) | Q(author.first_name__icontains=search_str)).exists():
    #     searched_book_list = Book.objects.filter(Q(book_name__icontains=search_str) | Q(book_name_hiragana__icontains=search_str) | Q(author.first_name__icontains=search_str))
    #     message = ""
    # if Book.objects.filter(Q(book_name__icontains=search_str)).exists():
    #     searched_book_list = Book.objects.filter(Q(book_name__icontains=search_str))
    #     message = ""
    if Book.objects.filter(Q(book_name__icontains=search_str) | Q(book_name_hiragana__icontains=search_str)).exists():
        searched_book_list = Book.objects.filter(Q(book_name__icontains=search_str) | Q(book_name_hiragana__icontains=search_str))
        message = ""
    else:
        searched_book_list = []
        message = "検索結果はありません"

    paginator = Paginator(searched_book_list, 20)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    books = paginator.get_page(page)
    return render(request, 'waganeko/book_list.html', {'books': books, 'page': page, 'last_page': paginator.num_pages, 'message': message})

def list_view(request):
    var = request.POST
    sort_str = var.get('sort')

    if sort_str == "ID順":
        book_list = Book.objects.all().order_by('-id')

    elif sort_str == "閲覧数順":
        book_list = Book.objects.all().order_by('view_nums').reverse()

    else:
        book_list = Book.objects.all().order_by('-id')

    paginator = Paginator(book_list, 20) # ページ当たり20個表示
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    # if request.method == 'POST':
    #     if 'book_id_list' in request.POST:
    #         book_list = Book.objects.all().order_by('-id')
    #     elif 'book_views_list' in request.POST:
    #         book_list = Book.objects.all().order_by('view_nums').reverse()
    # else:
    #     book_list = Book.objects.all().order_by('-id').reverse()
    # paginator = Paginator(book_list, 20) # ページ当たり20個表示

    # try:
    #     page = int(request.GET.get('page'))
    # except:
    #     page = 1

    books = paginator.get_page(page)
    return render(request, 'waganeko/book_list.html', {'books': books, 'page': page, 'last_page': paginator.num_pages})

#追加！
def detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.view_nums += 1
    book.save()
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    # self.form_view(request, book_id)


    # try:
    #     log = ScoreLog.objects.get(profile_id=request.user.profile.id, booook_id=book_id)
    #     current_score = log.score
    # except:
    #     current_score = -1

    # return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page, 'current_score':current_score })
    return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page})
    # return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page, 'form':form})

def form_view(request):
    form = NewExplanationForm()
    # return form
    return render(request, 'waganeko/explanation_new_post.html', {'form':form})

def new_explanation_post(request):
    form = NewExplanationForm(request.POST)
    print('aaaaaaaaaaaaa')
    if not form.is_valid():
        print("============================================")
        print("form invalid")
        print("============================================")
        messages.error(request, form_invalid_message)
        return redirect('waganeko:post_form')

    print("============================================")
    print("form valid")
    print("============================================")

    new_post = form.save(commit=False)
    print('#######################')
    print(request.user.profile.id) #check
    print(type(request.user.profile)) #check
    try:
        max_id = Explanation.objects.latest('id').id
    except ObjectDoesNotExist:
        max_id = 'E000000'

    explanation_id = 'E'+(str(int(max_id[1:])+1).zfill(5))
    new_post.id = explanation_id
    print(new_post.id) #check
    new_post.post_user = request.user.profile
    new_post.tweet = request.POST.get('tweet')
    new_post.save()
    print("----------")
    print("new post was saved")
    print("--------------------")
    messages.success(request, submit_successful_message)
    return redirect('waganeko:explanation_posts')

# ーーーーーー以下過去のモノーーーーーー
def explanation_posts(request):
    id_list = Explanation.objects.values_list('id', flat=True)
    explanation_posts_list = Explanation.objects.values_list('tweet', flat=True)
    explanations = zip(id_list, explanation_posts_list)
    explanations = list(explanations)

    f = {
        'explanations': explanations
    }
    return render(request, 'waganeko/explanation.html', f)


def delete(request, explanation_post_id):
    Explanation.objects.filter(id=explanation_post_id).delete()
    return redirect('waganeko:explanation_posts')

# def tweet_update(request, explanation_post_id):
#     var = request.POST
#     sort_str = var.get('sort')
#
#     new_explanation = NewExplanationForm(request.POST or None)
#     print(explanation_post_id)
#     print('-------------------------------------')
#     print(new_explanation)
#     if new_explanation.is_valid():
#         new_explanation = new_explanation.cleaned_data['tweet']
#         old_explanation = Explanation.objects.get(id=explanation_post_id)
#         old_explanation.tweet = new_explanation
#         old_explanation.save()
#         return redirect('waganeko:explanation_posts')
#     else:
#         new_explanation = new_explanation.as_table()
#         f = {
#         'new_explanation': new_explanation,
#         }
#         return render(request, 'waganeko/update.html', f)








# #追加！
# @login_required
# def rate(request, rentroom_id):
#     rentroom = get_object_or_404(RentRoom, id=rentroom_id)

#     log, created = ScoreLog.objects.update_or_create( \
#         defaults = {'score':request.POST.get('score')},
#         profile_id = request.user.profile.id,
#         rent_room_id = rentroom_id,
#     )

#     if created:
#         messages.success(request, message_rate_created)
#     else:
#         messages.success(request, message_rate_updated)

#     return redirect('iekari:rentroom_detail', rentroom_id=rentroom_id)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required #追加！
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from waganeko.new_explanation_form import NewExplanationForm


from django.core.paginator import Paginator
from waganeko.models import Book, ScoreLog, Explanation, Like, Dislike

import random

form_invalid_message = '不正な入力が送信されました'
submit_successful_message = '投稿されました。！'
message_rate_created = '評価が登録されました！'
message_rate_updated = '評価が更新されました！'

def list_search_view(request):
    print('hhhhhhhh')
    bar = request.GET
    search_str = bar.get('search')
    print('ooooooo')
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
    print('----')
    return render(request, 'waganeko/book_list.html', {'books': books, 'page': page, 'last_page': paginator.num_pages, 'message': message})
    print('hhhhhhhh')

def list_view(request):
    print('00000000000')
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
    # explanation = get_object_or_404(Explanation, )
    explanations = Explanation.objects.filter(post_for_book__id=book_id).order_by('total_nums').reverse()
    # explanations = Explanation.objects.filter(post_for_book__id=book_id)
    print('------------')
    # print(explanations)
    # print(type(explanations))
    return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page, 'explanations':explanations})

def detail_view2(request, book_id, explanation_id):
    book = get_object_or_404(Book, id=book_id)
    book.view_nums += 1
    book.save()
    # print('---------------------------------')
    # # ii_nums = Explanation.objects.values_list('iine_nums', flat=True)
    # # igi_nums = Explanation.objects.values_list('igiari_nums', flat=True)
    # # total = ii_nums + igi_nums
    # #
    # print('00000000000000')
    # print(str(explanation.iine_nums))
    # total = explanation.iine_nums + explanation.igiari_nums
    # print(total)
    # print(type(total))
    # print('00000000000')
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1

    explanations = Explanation.objects.filter(post_for_book__id=book_id).order_by('total_nums').reverse()
    print('------------')
    return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page, 'explanations':explanations})

@login_required
def form_view(request, book_id):
    form = NewExplanationForm()
    print(form)
    print(book_id)
    return render(request, 'waganeko/explanation_new_post.html', {'form':form, 'book_id':book_id})

@login_required
def new_explanation_post(request, book_id):
    form = NewExplanationForm(request.POST)
    if not form.is_valid():
        print("============================================")
        print("form invalid")
        print("============================================")
        messages.error(request, form_invalid_message)
        return redirect('waganeko:book_detail')

    print("============================================")
    print("form valid")
    print("============================================")

    new_post = form.save(commit=False)
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
    new_post.post_for_book = Book.objects.get(id=book_id)
    new_post.tweet = request.POST.get('tweet')
    new_post.save()
    print("new post was saved")
    messages.success(request, submit_successful_message)
    return redirect('waganeko:book_detail', book_id = book_id)


@login_required
def delete(request, explanation_post_id, book_id):
    Explanation.objects.filter(id=explanation_post_id).delete()
    print('delete=========')
    return redirect('waganeko:book_detail', book_id = book_id)

@login_required
def like(request, explanation_post_id, book_id):
    explanation = Explanation.objects.get(id=explanation_post_id)
    is_like = Like.objects.filter(user=request.user.profile).filter(explanation=explanation).count()
 # unlike
    if is_like > 0:
        liking = Like.objects.get(explanation__id=explanation_post_id, user=request.user.profile)
        liking.delete()
        explanation.iine_nums -= 1
        explanation.total_nums = explanation.iine_nums + explanation.igiari_nums
        explanation.save()
        messages.warning(request, 'なるほど～を取り消しました')
        return redirect('waganeko:book_detail2', book_id, explanation_post_id)
    # like
    print(explanation.iine_nums)
    print(type(explanation.iine_nums))
    explanation.iine_nums += 1
    explanation.total_nums = explanation.iine_nums + explanation.igiari_nums
    print('total:' + str(explanation.total_nums))
    explanation.save()
    like = Like()
    like.user = request.user.profile
    like.explanation = explanation
    like.save()
    messages.success(request, 'なるほど～しました')
    print('like==============')
    return redirect('waganeko:book_detail2', book_id, explanation_post_id)

@login_required
def dislike(request, explanation_post_id, book_id):
    explanation = Explanation.objects.get(id=explanation_post_id)
    is_dislike = Dislike.objects.filter(user=request.user.profile).filter(explanation=explanation).count()
 # unlike
    if is_dislike > 0:
        disliking = Dislike.objects.get(explanation__id=explanation_post_id, user=request.user.profile)
        disliking.delete()
        explanation.igiari_nums -= 1
        explanation.total_nums = explanation.iine_nums + explanation.igiari_nums
        explanation.save()
        messages.warning(request, '異議ありを取り消しました')
        return redirect('waganeko:book_detail2', book_id, explanation_post_id)
    # like
    explanation.igiari_nums += 1
    explanation.total_nums = explanation.iine_nums + explanation.igiari_nums
    print('total:' + str(explanation.total_nums))
    explanation.save()
    dislike = Dislike()
    dislike.user = request.user.profile
    dislike.explanation = explanation
    dislike.save()
    print('異議あり:' + str(explanation.igiari_nums))
    messages.success(request, '異議あり！しました')
    print('dislike===============')
    return redirect('waganeko:book_detail2', book_id, explanation_post_id)


# def tweet_update(request, explanation_post_id):
#     var = request.POST
#     sort_str = var.get('sort')
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

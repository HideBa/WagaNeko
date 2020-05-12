from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.decorators import login_required #追加！
from django.contrib import messages


from django.core.paginator import Paginator
from waganeko.models import Author, ScoreLog

import random

message_rate_created = '評価が登録されました！'
message_rate_updated = '評価が更新されました！'

def list_view(request):

    if request.method == 'POST':
        if 'author_id_list' in request.POST:
            author_list = Author.objects.all().order_by('-id')
        elif 'author_views_list' in request.POST:
            author_list = Author.objects.all().order_by('view_nums').reverse()
    else:
        author_list = Author.objects.all().order_by('-id')
    paginator = Paginator(author_list, 20) # ページ当たり20個表示

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    authors = paginator.get_page(page)
    return render(request, 'waganeko/author_list.html', {'authors': authors, 'page': page, 'last_page': paginator.num_pages})

#追加！
def detail_view(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    # author.view_nums += 1
    # author.save()
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1

    # try:
    #     log = ScoreLog.objects.get(profile_id=request.user.profile.id, booook_id=book_id)
    #     current_score = log.score
    # except:
    #     current_score = -1

    # return render(request, 'waganeko/book_detail.html', {'book': book, 'page': page, 'current_score':current_score })
    return render(request, 'waganeko/author_detail.html', {'author': author, 'page': page})


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

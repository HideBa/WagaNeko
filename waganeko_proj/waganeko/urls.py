from django.urls import path
from waganeko.views import hello, mypage, book, author, mypage
# ルーティングの設定

app_name = 'waganeko'
urlpatterns = [
    path('hello/', hello.hello, name='hello'),
    path('mypage', mypage.mypage_top, name='mypage_top'),#追加！
    path('book/<slug:book_id>', book.detail_view, name='book_detail'),
    path('book/<slug:book_id>/<slug:explanation_id>', book.detail_view2, name='book_detail2'),
    path('book/', book.list_view, name='book_list'),
    path('book/search', book.list_search_view, name='book_search_list'),
    path('author/', author.list_view, name='author_list'),
    path('author/<slug:author_id>', author.detail_view, name='author_detail'),
    path('newpost/<slug:book_id>', book.new_explanation_post, name='new_explanation_post'),
    # path('posts/', book.explanation_posts, name='explanation_posts'),
    path('form/<slug:book_id>', book.form_view, name='post_form'),
    path('delete/<slug:explanation_post_id>/<slug:book_id>', book.delete, name='delete'),
    path('like/<slug:explanation_post_id>/<slug:book_id>', book.like, name='like'),
    path('dislike/<slug:explanation_post_id>/<slug:book_id>', book.dislike, name='dislike'),
    # path('update/<slug:explanation_post_id>/', book.update, name='update'),
]

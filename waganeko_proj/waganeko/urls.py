from django.urls import path
from waganeko.views import hello, mypage, book, author
# ルーティングの設定 

app_name = 'waganeko'
urlpatterns = [ 
    path('hello/', hello.hello, name='hello'), 
    path('mypage', mypage.mypage_top, name='mypage_top'),#追加！
    path('book/<slug:book_id>', book.detail_view, name='book_detail'),
    path('book/', book.list_view, name='book_list'),
    path('book/search', book.list_search_view, name='book_search_list'),
    path('author/', author.list_view, name='author_list'),
    path('author/<slug:author_id>', author.detail_view, name='author_detail'),
]
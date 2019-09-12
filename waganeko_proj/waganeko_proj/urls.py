"""waganeko_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from waganeko.views.register import register_view, done_view
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from waganeko.models import Book
# from .index import index

def index(request):
    book_list = Book.objects.all().order_by('view_nums').reverse()[:6]
    # book_list = list(Book.objects.all().order_by('view_nums').reverse()[:6])
    print(book_list)
    print(type(book_list))
    print(book_list[0])
    return render(request,'index.html', {'book_list':book_list})

def test(request):
    return render(request, 'test.html')

urlpatterns = [
    path('test/', test, name='test'),
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('waganeko/', include('waganeko.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
    path('accounts/register/done', done_view, name='register_done'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

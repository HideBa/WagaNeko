from django.contrib import admin

# Register your models here.
from .models import Profile, Book, ScoreLog, Summary, Author, Publisher, Explanation

admin.site.register(Profile) 
admin.site.register(Book) 
admin.site.register(ScoreLog) 
admin.site.register(Summary) 
admin.site.register(Author) 
admin.site.register(Publisher) 
admin.site.register(Explanation) 
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
GENDER_LIST = ( (0, '男性'), (1, '女性') )
dict_gender_list = {0:'男性',1:'女性'}
book_category_list = ((0, '小説'), (1, '科学'))
dict_book_category_list = {0:'小説', 1:'科学'}


# class Followed(models.Model):
#     class Meta:
#         verbose_name = 'フォロワー名'
#         verbose_name_plural = 'フォロワー名'

#     id = models.CharField(max_length=6,primary_key=True)

class Profile(models.Model):
    class Meta:#Djangoの使用、インナークラスといい、Profileがどういう情報かを設定する
        verbose_name = 'ユーザー情報データ'
        verbose_name_plural = 'ユーザー情報データ'

    user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField('email', blank=False, unique=True)
    id = models.CharField(max_length=6,primary_key=True)
    #U00001から
    username = models.CharField('ユーザー名', max_length=30)
    age = models.IntegerField('年齢')
    gender = models.IntegerField('性別',choices=GENDER_LIST)
    prefer_book_category = models.IntegerField('好きな本のカテゴリ', choices=book_category_list, null=True)
    icon_img = models.ImageField(upload_to='image/', null=True)
    belong = models.CharField('所属', max_length=30, null=True)
    # follower = models.ManyToManyField(Followed, blank=True)


    def __str__(self):
        user_str = ''
        if self.user is not None:
            user_str = '(' + self.user.username + ')'
        #加筆ここまで

        return self.id+' '+str(self.age)+'歳 ' \
            +dict_gender_list.get(self.gender)+' ' \
            +user_str

#------------------------------------------------------------------------------------------------------


class Author(models.Model):
    class Meta:
        verbose_name = '著者データ'
        verbose_name_plural = '著者データ'

    id = models.CharField(max_length=6, primary_key=True)
    #A00001から
    last_name = models.CharField('著者苗字', max_length=30, null=True)
    first_name = models.CharField('著者名', max_length=30, null=True)
    last_name_hiragana = models.CharField('著者苗字ひらがな', max_length=30, null=True)
    first_name_hiragana = models.CharField('著者名ひらがな', max_length=30, null=True)
    born_year = models.CharField('生まれた年', max_length=20, null=True)
    pass_away_year = models.CharField('享年', max_length=20, null=True)
    detail = models.TextField('著者について詳細', null=True)
    author_img = models.ImageField(upload_to='image/', null=True)

    def __str__(self):
        if self.first_name:
            return self.id + ' ' + self.last_name + ' ' + self.first_name
        else:
            return self.id + ' ' + self.last_name
        # return self.id + ' ' + self.last_name + ' ' + self.first_name

class Publisher(models.Model):
    class Meta:
        verbose_name = '出版社'
        verbose_name_plural = '出版社'
    id = models.CharField(max_length=6, primary_key=True)
    #P00001から
    name = models.CharField('出版社名', max_length=30)
    other = models.TextField('詳細', null=True)


class Book(models.Model):
    class Meta:
        verbose_name = '本データ'
        verbose_name_plural = '本データ'

    id = models.CharField(max_length=6, primary_key=True)
    #I00001から
    book_name = models.CharField('本の名前', max_length=50)
    book_name_hiragana = models.CharField('本の名前（読み仮名）', max_length=50, null=True)
    author = models.ForeignKey(Author, verbose_name='著者',null=True, on_delete=models.CASCADE)
    # publisher = models.ForeignKey(Publisher, verbose_name='出版社', on_delete=models.CASCADE, null=True)
    first_published_year = models.CharField('出版年', max_length=5, null=True)
    text = models.TextField('本文', null=True)
    category = models.IntegerField('本のカテゴリ', choices=book_category_list, null=True)
    rate = models.IntegerField('評価', default=0, null=True)
    page_nums = models.IntegerField('ページ数', null=True)
    book_img = models.ImageField(upload_to='image/', null=True)
    view_nums = models.PositiveIntegerField('閲覧数', default=0)

    def __str__(self):
        return self.book_name + ' ' + self.author.id

class Summary(models.Model):
    class Meta:
        verbose_name = 'あらすじ'
        verbose_name_plural = 'あらすじ'

    id = models.CharField(max_length=6, primary_key=True)
    #S00001から
    post_user = models.ForeignKey(Profile, verbose_name='投稿者', on_delete=models.CASCADE)
    post_text = models.TextField('投稿', max_length=100)
    iine_nums = models.PositiveIntegerField('いいね数')
    category = models.PositiveIntegerField('カテゴリ', choices=book_category_list, null=True)
    posted_time = models.DateTimeField(auto_now_add=True)
    post_for_book = models.ForeignKey(Book, verbose_name='投稿先の本', on_delete=models.CASCADE)

class Explanation(models.Model):
    class Meta:
        verbose_name = '解説'
        verbose_name_plural = '解説'

    id = models.CharField(max_length=6, primary_key=True)
    #E00001から
    post_user = models.ForeignKey(Profile, verbose_name='投稿者', on_delete=models.CASCADE, null=True)
    # post_text = models.CharField('投稿内容', max_length=150)
    tweet = models.TextField('ツイート', default="")
    iine_nums = models.PositiveIntegerField('いいね数', default=0)
    igiari_nums = models.PositiveIntegerField('異議あり数', default=0)
    category = models.PositiveIntegerField('カテゴリ', choices=book_category_list, null=True)
    posted_time = models.DateTimeField(auto_now_add=True, null=True)
    total_nums = models.PositiveIntegerField('合計数', default=0)
    post_for_book = models.ForeignKey(Book, verbose_name='投稿先の本', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.post_user.id + ' ' + self.tweet + self.id

class Like(models.Model):
    class Meta:
        verbose_name = 'なるほど～'
        verbose_name_plural = 'なるほど～'

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='like_user')
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
    class Meta:
        verbose_name = '異議あり'
        verbose_name_plural = '異議あり'

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='dislike_user')
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class ScoreLog(models.Model):
    class Meta:
        verbose_name = '本評価データ'
        verbose_name = '本評価データ'

    profile = models.ForeignKey(Profile, verbose_name='ユーザー情報', on_delete=models.CASCADE)
    score = models.IntegerField('評価')                         # 1~5
    timestamp = models.DateTimeField('日時', auto_now_add=True)

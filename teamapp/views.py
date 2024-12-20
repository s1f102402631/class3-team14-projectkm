from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from teamapp.models import Article, Comment
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from teamapp.models import Like #新たなlike class

# Create your views here.
def index(request):
    if request.method == 'POST':
        article = Article(title=request.POST['title'], body=request.POST['text'])
        article.save()
        return redirect(detail, article.id)

    if ('sort' in request.GET):
        if request.GET['sort'] == 'like':
            articles = Article.objects.order_by('-like')
        else:
            articles = Article.objects.order_by('-posted_at')
    else:
        articles = Article.objects.order_by('-posted_at')

    context = {
        "articles": articles,
    }
    return render(request, 'teamapp/home_screen.html', context)

def detailscreen(request):
    if request.method == 'POST':
        article = Article(title=request.POST['title'], body=request.POST['text'])
        article.save()
        return redirect(detail, article.id)

    if ('sort' in request.GET):
        if request.GET['sort'] == 'like':
            articles = Article.objects.order_by('-like')
        else:
            articles = Article.objects.order_by('-posted_at')
    else:
        articles = Article.objects.order_by('-posted_at')

    context = {
        "articles": articles,
    }
    return render(request, 'teamapp/detailscreen.html', context)

def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    if request.method == 'POST':
        comment = Comment(article=article, text=request.POST['text'])
        comment.save()
    context = {
        'article': article,
        'comments': article.comments.order_by('-posted_at')
    }
    return render(request, 'teamapp/detail.html', context)

def update(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Http404:
        raise Http404("Article does not exist")
    if request.method == 'POST':
        article.title = request.POST['title']
        article.body = request.POST['text']
        article.save()
        return redirect(detail, article_id)
    context = {
        'article': article
    }
    return render(request, 'teamapp/edit.html', context)

def delete(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    article.delete()
    return redirect(index)

def like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")

    return redirect(detail, article_id)

def api_like(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        article.like += 1
        article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    result = {
        'id': article_id,
        'like': article.like
    }
    return JsonResponse(result)

def bio(request):
    return render(request, "teamapp/bio.html")

def detailscreen(request):
    return render(request, 'teamapp/detailscreen.html')
    
def home_page(request):
    return render(request, 'teamapp/home_screen.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ユーザー認証
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # ログイン成功
            login(request, user)
            return redirect('index')
        else:
            # ログイン失敗
            messages.error(request, 'ユーザー名またはパスワードが間違っています。')

    return render(request, 'teamapp/login_home.html')

#先ほどの下に追加
#新規アカウントの追加ページ
def user_create(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        try:
            # 新しいユーザーオブジェクトを作成し、ユーザー名とパスワードを設定
            user = User.objects.create_user(username=new_username, password=new_password)
        except Exception as e:
            # ユーザ作成失敗
            messages.error(request, 'アカウントの作成に失敗しました。エラー: {}'.format(str(e)))

    return render(request, 'teamapp/login_create.html')

#ユーザがいいねをすでにしているかどうかを確認
#@login_required ログイン機能追加後に記入
def toggle_like(request, posted_at):
    post = get_object_or_404(Post, posted_at)

    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created: #すでにいいねしているとき
        like.delete()
        liked = False
    else:
        liked = True

    likes_count = post.like_set.count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})


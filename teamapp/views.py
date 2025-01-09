from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from teamapp.models import Article, Comment, Like, Profile, Notification
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from teamapp.models import CustomUser
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from teamapp.forms import ProfileForm


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

@login_required()
def bio(request):
    try:
        profile = Profile.objects.get(user=request.user)
        context = {
            'profile': profile,
            'username': request.user.username,
            'studentid': request.user.studentid
        }
        return render(request, "teamapp/bio.html", context)
    except Profile.DoesNotExist:
        return redirect('bio_edit')

@login_required
def detailscreen(request):
    return render(request, 'teamapp/detailscreen.html')
    
def home_page(request):
    return render(request, 'teamapp/home_screen.html')

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        studentid = request.POST.get('studentid')

        # カスタムバックエンドを使ったユーザー認証
        user = authenticate(request, username=username, password=password, studentid=studentid)

        if user is not None:
            # ログイン成功
            login(request, user)
            messages.success(request, 'ログインに成功しました！')
            context = {
                'username': username,
                'studentid': studentid,
            }
            return render(request, 'teamapp/login_home.html', context)
        else:
            # ログイン失敗
            messages.error(request, '正しい情報を入力してください。')

    context = {
        'username': request.POST.get('username', ''),
        'studentid': request.POST.get('studentid', ''),
    }

    return render(request, 'teamapp/login_home.html', context)

def user_create(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        new_password = request.POST.get('new_password')
        new_studentid = request.POST.get('new_studentid')
        try:
            # 新しいユーザーオブジェクトを作成
            user = CustomUser.objects.create_user(username=new_username, password=new_password, studentid=new_studentid)
            messages.success(request, 'アカウントの作成に成功しました！')
            user.save()
            return render(request, 'teamapp/login_home.html')
        except Exception as e:
            # ユーザー作成失敗
            messages.error(request, 'アカウントの作成に失敗しました。エラー: {}'.format(str(e)))
    return render(request, 'teamapp/login_create.html')

#@login_required 
def toggle_like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        like, created = Like.objects.get_or_create(user=user, article=article)
        
        if created:
            liked = True
        else:
            like.delete()
            liked = False

        likes_count = article.likes.count()

        return JsonResponse({'liked': liked, 'likes_count': likes_count})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def bio_edit(request):
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('bio')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'teamapp/bio_edit.html', {'form': form})

def some_view(request):
    articles = Article.objects.all()
    for article in articles:
        article.is_liked_by_student = request.studentid in article.likes.values_list('studentid', flat=True)
    context = {
        'articles': articles,
        'user': request.user,
        # 他のコンテキスト追加可能
    }
    return render(request, 'home_screen.html', context)

@login_required
def configuration_view(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            user.delete()
            return redirect('create')
    return render(request, 'teamapp/configuration.html')

def create_comment_notification(user, article, comment):
    message = f"{user.username} commented on your article."
    Notification.objects.create(user=article.user, notification_type='comment', message=message)

def create_like_notification(user, post):
    message = f"{user.username} liked your post."
    Notification.objects.create(user=post.user, notification_type='like', message=message)

def post_comment(request, article_id):
    article = article.objects.get(id=article_id)
    user = request.user
    comment_content = request.POST.get('comment')
    comment = Comment.objects.create(article=article, user=user, content=comment_content)
    create_comment_notification(user, article, comment)
    return HttpResponse('Comment posted successfully!')

def notification_list(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-created_at')
    return render(request, 'teamapp/notifications.html', {'notifications': notifications})

from django.shortcuts import get_object_or_404
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    return redirect('notifications')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required #기말고사
from django.utils import timezone
from .forms import PostForm, CommentForm
from .models import Post, Comment

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #기말고사
    return render(request, 'blog/post_detail.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})

@login_required #기말고사
def post_new(request):
    if request.method == "POST": #기말고사
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) #기말고사 왜 False인가?
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) #기말고사
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required #기말고사
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #시험문제 왜 False인가? - DB에 바로 업로드 하는게 아닌 대기상태로 만드는것
            #대기상태, 유해성 검사 / author, published 체크
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required #기말고사
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required #기말고사
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

#시험문제 CSRF란 무엇인가?
#시험문제 CRUD란 무엇인가?
#Created - POST
#Read - GET
#Update - PUT
#Delete - DELETE

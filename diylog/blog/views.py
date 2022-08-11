from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, BlogComment
from django.contrib import messages


# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    allPosts = list(allPosts)
    allPosts.reverse()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug)[0]
    comments = BlogComment.objects.filter(post=post, parent=None).order_by("-timestamp") # - denotes descending
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)

    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
            
    context = {'post': post, 'comments': comments, 'replyDict':replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            comments = BlogComment(comment=comment, user=user, post=post)
            comments.save()
            messages.success(request, "Your comment has been posted successfully!")   
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comments = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comments.save()
            messages.success(request, "Your reply has been posted successfully!")   

    return redirect(f"/blog/{post.slug}")

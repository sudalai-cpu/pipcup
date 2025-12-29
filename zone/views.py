from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        Post.objects.create(title=title, content=content, image=image)
        return redirect('home')
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'zone/home.html', {'posts': posts})

def sale_page(request):
    return render(request, 'zone/sale.html')



from django.http import JsonResponse

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})

def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, content=content)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # Determine the author
        if request.user.is_authenticated:
            author = request.user
        else:
            author = User.objects.first() or User.objects.create(username='testuser')
            
        Post.objects.create(user=author, title=title, content=content, image=image)
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
def profile(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = User.objects.first()
        if not user:
            user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_bio = request.POST.get('bio')
        new_image = request.FILES.get('image')

        if new_username:
            user.username = new_username
            user.save()
        
        if new_bio is not None:
            profile.bio = new_bio
        
        if new_image:
            profile.image = new_image
        
        profile.save()
        return redirect('profile')

    return render(request, 'zone/profile.html', {'profile': profile})

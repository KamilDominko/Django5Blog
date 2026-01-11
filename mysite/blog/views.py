from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    post_list = Post.published.all()
    # Stronicowanie z 3 postami na stronę
    paginator = Paginator(post_list, 3)
    # Pobiera numer strony "page" z request, jeżeli nie ma to zwraca 1
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # Jeśli zmienna page_number jest poza zakresem, wyślij ostatnią stronę wyników
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # Jeśli page_number nie jest liczbą całkowitą zwróć pierwszą stronę
        posts = paginator.page(1)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})

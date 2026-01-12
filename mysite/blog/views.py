from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


def post_share(request, post_id):
    # Pobierz post według identyfikatora
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        # Formularz został przesłany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Pomyślnie zweryfikowano poprawność pól formularza
            cd = form.cleaned_data
            # ...wyślij email
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"post": post, "form": form})


class PostListView(ListView):
    """Alternatywny widok listy postów."""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


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

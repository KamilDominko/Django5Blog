from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


class FeaturedPostListView(ListView):
    queryset = Post.objects.filter(featured=True)
    template_name = "blog/post/featured.html"
    context_object_name = "featured"
    paginate_by = 2


def featured_posts(request):
    featured_list = Post.objects.filter(featured=True)
    paginator = Paginator(featured_list, 3)
    page_number = request.GET.get("page", 1)
    featured = paginator.get_page(page_number)
    # try:
    #     featured = paginator.page(page_number)
    # except EmptyPage:
    #     featured = paginator.page(paginator.num_pages)
    # except PageNotAnInteger:
    #     featured = paginator.page(1)
    return render(request, "blog/post/featured.html", {"featured": featured})


def post_share(request, post_id):
    # Pobierz post według identyfikatora
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # Formularz został przesłany
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Pomyślnie zweryfikowano poprawność pól formularza
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd["name"]} {cd["email"]} " f"poleca Ci przeczytanie {post.title}"
            )
            message = (
                f"Przeczytaj {post.title} pod adresem {post_url}\n\n"
                f"komentarze {cd["name"]}: {cd["comments"]}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


class PostListView(ListView):
    """Alternatywny widok listy postów."""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # Zwiększenie licznika wyświetleń posta
    post.viewed += 1
    post.save()
    # Lista aktywnych komentarzy do tego posta
    comments = post.comments.filter(active=True)
    # Formularz do wprowadzenia komentarzy użytkowników
    form = CommentForm()
    # Lista podobnych postów
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # Opublikowany komentarz
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Utwórz obiekt Comments bez zapisywania go w bazie danych
        comment = form.save(commit=False)
        # Przypisz post do komentarza
        comment.post = post
        # Zapisz komentarz do bazy danych
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


def post_archive(request):
    years = Post.published.dates("publish", "year", "DESC")
    return render(request, "blog/post/archive.html", {"years": years})


def post_archive_year(request, year):
    posts = Post.published.filter(publish__year=year)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(
        request, "blog/post/archive_year.html", {"posts": posts, "year": year}
    )

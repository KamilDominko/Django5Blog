from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # list_display dodaje w oknie panelu administratora dodatkowe informacje na temat każdego posta
    list_display = ["title", "slug", "author", "publish", "status"]

    # list_filetr dodaje filtrowanie postów pod kątm podanych pól
    list_filter = ["status", "created", "publish", "author"]

    # lista pól do przeszukiwania postów - poasek wyszukiwania szuka frazy w podanych polach postów
    search_fields = ["title", "body"]

    # automatycznie tworzy slug z podanego tytułu
    prepopulated_fields = {"slug": ("title",)}

    # okienkowy widget do łatwiejszego dodawania autorów
    raw_id_fields = ["author"]

    # dzieli posty na hierarchie dat
    date_hierarchy = "publish"

    # domyślnie sortuje posty po tych polach
    ordering = ["status", "publish"]

    # pokazuje przy na pasku filtrów, ile jest postów zawierajacych każdy aspekt
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]

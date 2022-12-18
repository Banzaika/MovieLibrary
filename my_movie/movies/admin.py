from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from.models import *
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'





class ReviewInline(TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ["name", "email"]
    
class MovieShotsInline(TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} wigth="100" height="110">')
    get_image.short_description = "Изображение"


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", )

@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ("id", "category", "title", "url", "draft")
    list_display_links = ("title", )
    list_filter = ("category", "year")
    search_fields = ("title", "category__name", "url")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ["draft", ]
    form = MovieAdminForm
    readonly_fields = ("get_image", )
    actions = ('publish', 'unpublish')
    fieldsets = (
        (None, { 
            "fields": (("title", "tagline"), )
            }),
        (None, { 
            "fields": (("description", "get_image"  ), )
            }),
        (None, { 
            "fields": (("year", "country"), )
            }),
        ("Actors", { 
            "classes": ("collapse", ),
            "fields": (("actors", "directors", "genres", "category", ), )
            }),
        (None, { 
            "fields": (("budget", "fees_in_usa", "fees_in_world"), )
            }),
        ("Options", { 
            "fields": (("url", "draft"), )
            }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} wigth="100" height="110">')
    
    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена.'
        else:
            message_bit = f'{row_update} записи были обновлены.' 
        self.message_user(request, message_bit)


    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись снята с публикации.'
        else:
            message_bit = f'{row_update} записи сняты с публикации.' 
        self.message_user(request, message_bit)

    publish.allowed_permissions = ("change", )
    publish.short_description = "Опубликовать"

    unpublish.allowed_permissions = ("change", )
    unpublish.short_description = "Снять с публикaции"

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewsAdmin(ModelAdmin):
    list_display = ("name", "movie", "email", "parent")
    list_display_links = ("movie", "email", "parent") 
    readonly_fields = ("name", "email")


@admin.register(Actor)
class ActorAdmin(ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} wigth="50" height="60">')
    get_image.short_description = "Изображение"

@admin.register(Genre)
class GenreAdmin(ModelAdmin): 
    list_display = ("name", "url")

@admin.register(MovieShots)
class MovieShotsAdmin(ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image", )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} wigth="50" height="60">')
    get_image.short_description = "Изображение"

@admin.register(RatingStar)
class RatingStarAdmin(ModelAdmin):
    list_display = ("value", )

@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    list_display = ("ip", "movie")


#Banner Naming
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
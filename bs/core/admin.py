from django.contrib import admin
from .models import Academie, Bitcoin, Contact, CreateBlog, Category, Comment, Equipe, Immobilier, Informatique, Laboratoire, Production_Audio_Visuelle, Subscribers, MailMessage, Partenaire

# Register your models here.
admin.site.register(Category)


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'intro', 'slug', 'date_added')


admin.site.register(CreateBlog, BlogAdmin)


class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'fonction', 'email', 'github', 'tweeter', 'linkedin')

admin.site.register(Equipe, EquipeAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'email', 'date_added', 'date_added')


admin.site.register(Comment, CommentAdmin)

admin.site.register(Subscribers)
admin.site.register(MailMessage)
admin.site.register(Partenaire)
admin.site.register(Contact)
admin.site.register(Bitcoin)
admin.site.register(Laboratoire)
admin.site.register(Immobilier)
admin.site.register(Informatique)
admin.site.register(Academie)
admin.site.register(Production_Audio_Visuelle)


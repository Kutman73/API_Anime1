from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'original_anime_name': ('title_anime', )}


admin.site.register(Anime, ArticleAdmin)
admin.site.register(Genre)
admin.site.register(Theme)
admin.site.register(Producer)
admin.site.register(VoiceActing)
admin.site.register(AnimeEpisode)
admin.site.register(Review)
admin.site.register(AnimeMovie)
admin.site.register(AnimeSeason)
admin.site.register(StatusAnime)

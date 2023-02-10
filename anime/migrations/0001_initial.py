# Generated by Django 4.1.4 on 2023-02-10 10:42

import anime.fileschek
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_anime', models.CharField(max_length=255, unique=True)),
                ('original_anime_name', models.SlugField(unique=True)),
                ('cover_anime', models.ImageField(storage=anime.fileschek.OverWriteStorage(), upload_to=anime.fileschek.FilePath.get_path_to_cover_anime, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg']), anime.fileschek.FileCheck.check_file_anime_cover_size])),
                ('description_anime', models.TextField()),
                ('release_date_anime', models.DateField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatusAnime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_name', models.CharField(max_length=55, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VoiceActing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_acting', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('rating_for_anime', models.DecimalField(choices=[(Decimal('1.0'), '★☆☆☆☆☆☆☆☆☆ (1/10)'), (Decimal('2.0'), '★★☆☆☆☆☆☆☆☆ (2/10)'), (Decimal('3.0'), '★★★☆☆☆☆☆☆☆ (3/10)'), (Decimal('4.0'), '★★★★☆☆☆☆☆☆ (4/10)'), (Decimal('5.0'), '★★★★★☆☆☆☆☆ (5/10)'), (Decimal('6.0'), '★★★★★★☆☆☆☆ (6/10)'), (Decimal('7.0'), '★★★★★★★☆☆☆ (7/10)'), (Decimal('8.0'), '★★★★★★★★☆☆ (8/10)'), (Decimal('9.0'), '★★★★★★★★★☆ (9/10)'), (Decimal('10.0'), '★★★★★★★★★★ (10/10)')], decimal_places=1, default=5.0, max_digits=3)),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='anime.anime')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AnimeSeason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.PositiveIntegerField()),
                ('season_title', models.CharField(blank=True, max_length=100, null=True)),
                ('release_date_of_the_season', models.DateField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producer_of_the_season', models.ManyToManyField(to='anime.producer')),
                ('season_anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='anime.anime')),
                ('voiceover_of_the_season', models.ManyToManyField(to='anime.voiceacting')),
            ],
        ),
        migrations.CreateModel(
            name='AnimeMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_movie', models.CharField(max_length=255, unique=True)),
                ('anime_movie_video', models.FileField(storage=anime.fileschek.OverWriteStorage(), upload_to=anime.fileschek.FilePath.get_path_to_movie, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('movie_duration', models.DurationField()),
                ('movie_number', models.PositiveIntegerField(unique=True)),
                ('release_date_of_the_movie', models.DateField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('anime_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.anime')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producer_anime_of_the_movie', models.ManyToManyField(to='anime.producer')),
                ('voice_acting_anime_of_the_movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.voiceacting')),
            ],
        ),
        migrations.CreateModel(
            name='AnimeEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_episode', models.CharField(max_length=255)),
                ('anime_video', models.FileField(max_length=255, storage=anime.fileschek.OverWriteStorage(), upload_to=anime.fileschek.FilePath.get_path_to_episode, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('episode_duration', models.DurationField()),
                ('episode_number', models.PositiveIntegerField()),
                ('release_date_of_the_episode', models.DateField()),
                ('creation_date', models.DateField(auto_now=True)),
                ('number', models.PositiveSmallIntegerField(default=1)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.anime')),
                ('anime_season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='anime_season', to='anime.animeseason')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voice_acting_of_the_episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.voiceacting')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='genre_anime',
            field=models.ManyToManyField(to='anime.genre'),
        ),
        migrations.AddField(
            model_name='anime',
            name='producer_anime',
            field=models.ManyToManyField(to='anime.producer'),
        ),
        migrations.AddField(
            model_name='anime',
            name='status_anime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.statusanime'),
        ),
        migrations.AddField(
            model_name='anime',
            name='theme_anime',
            field=models.ManyToManyField(to='anime.theme'),
        ),
    ]

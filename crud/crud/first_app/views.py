from django.shortcuts import render
from first_app.models import Musician, Album
from first_app import forms
from django.db.models import Avg

# Create your views here.
def index(request):
    musician_list = Musician.objects.order_by('first_name')
    dict = {'title': "Home Page", 'musician_list': musician_list}
    return render(request, 'first_app/index.html', context=dict)

def album_list(request, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    album_list = Album.objects.filter(artist = artist_id)
    artist_rating = Album.objects.filter(artist = artist_id).aggregate(Avg('num_stars'))
    dict = {'title': "List of Albums", 'artist_info':artist_info, 'album_list':album_list, 'artist_rating':artist_rating}
    return render(request, 'first_app/album_list.html', context=dict)

def musician_form(request):
    form = forms.MusicianFrom()
    if request.method == 'POST':
        form = forms.MusicianFrom(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
    dict = {'title':"Add Musician", 'musician_form': form}
    return render(request, 'first_app/musician_form.html', context=dict)

def album_form(request):
    form = forms.AlbumForm()
    if request.method == "POST":
        form = forms.AlbumForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
    dict = {'title': "Add Album", 'album_form':form}
    return render(request, 'first_app/album_form.html', context=dict)

def edit_artist(request, artist_id):
    artist_info = Musician.objects.get(pk=artist_id)
    form = forms.MusicianFrom(instance=artist_info)

    if request.method == 'POST':
        form = forms.MusicianFrom(request.POST, instance=artist_info)
        if form.is_valid():
            form.save(commit=True)
            return album_list(request, artist_id)
    dict = {'edit_form': form}
    return render(request, 'first_app/edit_artist.html', context=dict)

def edit_album(request,album_id):
    album_info = Album.objects.get(pk=album_id)
    form = forms.AlbumForm(instance=album_info)
    dict={}

    if request.method == 'POST':
        form = forms.AlbumForm(request.POST,instance = album_info)

        if form.is_valid():
            form.save(commit=True)
            dict.update({'success_text':"Your Update is saved"})

    dict.update({'album_id': album_id})
    dict.update({'edit_form':form})
    return render(request, 'first_app/edit_album.html', context=dict)

def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id).delete()
    dict = {'delete_text': "Album Deleted Successfully"}
    return render(request, 'first_app/delete.html', context=dict)

def delete_artist(request, artist_id):
    artist = Musician.objects.get(pk=artist_id).delete()
    dict = {'delete_artist':"Artist Deleted Successfully"}
    return render(request, 'first_app/delete.html', context=dict)

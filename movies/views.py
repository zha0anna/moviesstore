from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, Vote
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
        {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
        {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def petition_list(request):
    petitions = Petition.objects.all()
    for petition in petitions:
        petition.user_voted = petition.votes.filter(petition = petition, user=request.user).exists()

    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petitions'] = petitions
    return render(request, 'movies/petition_list.html', {'template_data': template_data})

@login_required
def petition_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            petition = Petition()
            petition.title = title
            petition.description = description
            petition.user = request.user
            petition.save()
            return redirect('movies.petition_list')
    return render(request, 'movies/petition_create.html', {'template_data': {'title': 'Create Petition'}})

@login_required
def petition_vote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    vote, created = Vote.objects.get_or_create(petition=petition, user=request.user)
    if created:
        vote.vote_type = 'YES'
        vote.save()
    return redirect('movies.petition_list')

@login_required
def petition_deleteVote(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    Vote.objects.filter(petition=petition, user=request.user).delete()
    return redirect('movies.petition_list')
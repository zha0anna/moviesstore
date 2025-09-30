from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def yesVotes(self):
        return self.votes.filter(petition=self, vote_type='YES').count()
    
    def __str__(self):
        return str(self.id) + ' - ' + self.title
    
class Vote(models.Model):
    VOTE_TYPES = (
        ('YES', 'Yes'),
    )
    id = models.AutoField(primary_key=True)
    vote_type = models.CharField(max_length=3, choices=VOTE_TYPES)
    petition = models.ForeignKey(Petition, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('petition', 'user')
    
    def __str__(self):
        return str(self.id) + ' - ' + self.vote_type + ' - ' + self.petition.title
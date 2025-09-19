from django.conf import settings
from django.db import models

class Petition(models.Model):
    title = models.CharField(max_length=200)
    movie_title = models.CharField(max_length=200, help_text="Movie users want added")
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="petitions")
    created_at = models.DateTimeField(auto_now_add=True)

    def yes_count(self):
        return self.votes.filter(is_yes=True).count()

    def __str__(self):
        return f"{self.movie_title} (#{self.pk})"

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="petition_votes")
    is_yes = models.BooleanField(default=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("petition", "user")  # one vote per user per petition

    def __str__(self):
        return f"{self.user} -> {self.petition} : {'YES' if self.is_yes else 'NO'}"

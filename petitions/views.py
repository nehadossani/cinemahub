from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Petition, PetitionVote
from .forms import PetitionForm

@login_required
def petition_list_create(request):
    if request.method == "POST":
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            messages.success(request, "Petition created!")
            return redirect("petitions:detail", pk=petition.pk)
    else:
        form = PetitionForm()

    petitions = Petition.objects.all().order_by("-created_at")
    return render(request, "petitions/index.html", {"form": form, "petitions": petitions})

def petition_detail(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    user_has_voted = petition.votes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, "petitions/detail.html", {"petition": petition, "yes_count": petition.yes_count(), "user_has_voted": user_has_voted})

@login_required
def petition_vote(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    if request.method == "POST":
        try:
            PetitionVote.objects.create(petition=petition, user=request.user, is_yes=True)
            messages.success(request, "Vote recorded!")
        except IntegrityError:
            messages.info(request, "You already voted on this petition.")
    return redirect("petitions:detail", pk=pk)

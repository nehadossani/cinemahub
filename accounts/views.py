from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

@login_required
def subscription(request):
    # Sum all past orders for this user
    total_spent = request.user.order_set.aggregate(
        total=Sum("total")
    )["total"] or 0

    # Determine tier
    if total_spent < 15:
        subscription_level = "Basic"
        next_threshold = 15
    elif total_spent <= 30:
        subscription_level = "Medium"
        next_threshold = 30
    else:
        subscription_level = "Premium"
        next_threshold = None

    # Progress info (optional, for progress bar)
    progress = None
    remaining = None
    if next_threshold is not None:
        remaining = next_threshold - total_spent
        if subscription_level == "Basic":
            progress = int((total_spent / 15) * 100)
        elif subscription_level == "Medium":
            progress = int(((total_spent - 15) / 15) * 100)

    template_data = {
        "title": "My Subscription",
        "subscription_level": subscription_level,
        "total_spent": total_spent,
        "next_threshold": next_threshold,
        "remaining": remaining,
        "progress": progress,
    }
    return render(request, "accounts/subscription.html", template_data)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})
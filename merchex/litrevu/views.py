from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from litrevu.models import Ticket, Review, UserFollows
from litrevu.forms import TicketForm, ReviewForm, UserFollowsForm
from authentication.models import User

@login_required
def home(request):
    return render(request, 'litrevu/home.html')

@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'litrevu/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, id):
    ticket =  Ticket.objects.get(id=id)
    return render(request,
                  'litrevu/ticket_detail.html',
                  {'ticket': ticket})

@login_required
def ticket_create(request):
    print(request.method)
    if request.method == 'POST':
        print("POST: ", request.POST)
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            print("FILES: ", request.FILES)
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket-detail', ticket.id)
        else:
            print("ERROR: ", form.errors)
    else:
        form = TicketForm()
    return render(request,
                'litrevu/ticket_create.html',
                {'form': form})

@login_required
def ticket_update(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('ticket-detail', ticket.id)
        else:
            print("ERROR: ", form.errors)
    else:
        form = TicketForm(instance=ticket)
    return render(request,
                'litrevu/ticket_update.html',
                {'form': form})

@login_required
def ticket_delete(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket-list')
    return render(request, 
                  'litrevu/ticket_delete.html', 
                  {'ticket': ticket})


@login_required
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'litrevu/review_list.html', {'reviews': reviews})

@login_required
def review_detail(request, id):
    review =  Review.objects.get(id=id)
    return render(request,
                  'litrevu/review_detail.html',
                  {'review': review})

@login_required
def review_create(request):
    print(request.method)
    print(request.POST)
    print()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('review-detail', review.id)
        else:
            print("ERROR: ", form.errors)
    else:
        form = ReviewForm()
    return render(request,
                'litrevu/review_create.html',
                {'form': form})

@login_required
def review_update(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('review-detail', review.id)
        else:
            print("ERROR: ", form.errors)
    else:
        form = ReviewForm(instance=review)
    return render(request,
                'litrevu/review_update.html',
                {'form': form})

@login_required
def review_delete(request, id):
    review = Review.objects.get(id=id)
    if request.method == 'POST':
        review.delete()
        return redirect('review-list')
    return render(request, 
                  'litrevu/review_delete.html', 
                  {'review': review})


@login_required
def user_follows_list(request):
    user_list = User.objects.filter(username__icontains='Cléa')
    user_follows_list = UserFollows.objects.all()
    if request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            user_follows = form.save(commit=False)
            user_follows.user = request.user
            user_follows.save()

            return render(request, 'litrevu/user_follows_list.html', 
                 {'user_follows_list': user_follows_list, 
                  'user_list': user_list, 
                  'form': form,}
                 )
    else:
        form = UserFollowsForm()
        return render(request, 'litrevu/user_follows_list.html', 
                    {'user_follows_list': user_follows_list, 
                    'user_list': user_list, 
                    'form': form,}
                    )

@login_required
def user_follows_create(request):
    print(request.method)
    print(request.POST)
    print()
    if request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            user_follows = form.save(commit=False)
            user_follows.user = request.user
            user_follows.save()
            return redirect('user_follows-detail', user_follows.id)
        else:
            print("ERROR: ", form.errors)
    else:
        form = ReviewForm()
    return render(request,
                'litrevu/user_follows_create.html',
                {'form': form})

@login_required
def user_follows_delete(request, id):
    user_follows = UserFollowsForm.objects.get(id=id)
    if request.method == 'POST':
        user_follows.delete()
        return redirect('user_follows-list')
    return render(request, 
                  'litrevu/user_follows_delete.html', 
                  {'user_follows': user_follows})
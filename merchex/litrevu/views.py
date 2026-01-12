from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, CharField, Value
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from litrevu.models import Ticket, Review, UserFollows
from litrevu.forms import TicketForm, ReviewForm, SubscriptionForm

@login_required
def home(request):
    print(request.user)
    followed_users = UserFollows.objects.filter(
        user=request.user).values_list('followed_user', flat=True)
    
    reviews = Review.objects.filter(
        (Q(user=request.user) | Q(user__in=followed_users)))
    # reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets_user = Ticket.objects.filter(user=request.user)
    reviews_from_ticket_user = Review.objects.filter(
        ticket__in=tickets_user).exclude(pk__in=reviews)

    tickets = Ticket.objects.filter(user__in=followed_users)
    
    merge_tickets = chain(tickets, tickets_user)
    merge_tickets_and_reviews = chain(merge_tickets, reviews)
    merge_tickets_and_reviews = chain(
        merge_tickets_and_reviews, reviews_from_ticket_user)
    
    posts = sorted(
        merge_tickets_and_reviews,
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {
        'posts': posts,
    }
    for post in posts:
        print(post)
        
    return render(request, 'litrevu/home.html', context=context)

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
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
    reviews = Review.objects.filter(user=request.user)
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
def subscription(request):
    followed_users = UserFollows.objects.filter(user=request.user)
    subscriber_users = UserFollows.objects.filter(
        followed_user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.user, request.POST)
        if form.is_valid():
            messages.info(request,
                          'Utilisateur '
                          + request.POST.get('username') + ' ajouté')
    else:
        form = SubscriptionForm(request.user)
    context = {'followed_users': followed_users,
                'subscriber_users': subscriber_users} | {'form': form}
    return render(request, 
                 "litrevu/subscription.html",
                  context=context)

@login_required
def unsubscribe(request, id):
    """ remove the id user from the followed user """
    user = get_object_or_404(UserFollows, id=id)
    user.delete()
    return redirect('subscription')
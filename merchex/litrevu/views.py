from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Exists, OuterRef
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from litrevu.models import Ticket, Review, UserFollows, UserBlocks
from litrevu.forms import TicketForm, ReviewForm, SubscriptionForm, BlockingForm

@login_required
def home(request):
    print(request.user)
    followed_users = UserFollows.objects.filter(
        user=request.user).values_list('followed_user', flat=True)
    blocked_users = UserBlocks.objects.filter(
        user=request.user).values_list('blocked_user', flat=True)
    reviews = Review.objects.filter(
        (Q(user=request.user) | Q(user__in=followed_users)) & ~Q(user__in=blocked_users))
    
    user_has_review = Review.objects.filter(
        ticket=OuterRef("pk"),
        user=request.user
    )
    all_tickets = Ticket.objects.all().annotate(has_my_review=Exists(user_has_review))
    allow_map = {t.id: (not t.has_my_review) for t in all_tickets}

    tickets_user = Ticket.objects.filter(user=request.user)
    reviews_from_ticket_user = Review.objects.filter(
        ticket__in=tickets_user).exclude(pk__in=reviews)

    tickets = Ticket.objects.filter(
        (Q(user=request.user) | Q(user__in=followed_users)) & ~Q(user__in=blocked_users))
    
    # allow_map = {}
    merge_tickets_and_reviews = chain(tickets, reviews)
    merge_tickets_and_reviews = chain(
        merge_tickets_and_reviews, reviews_from_ticket_user)
    
    
    posts = sorted(
        merge_tickets_and_reviews,
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {
        'posts': posts,
        'allow_map': allow_map,
    }
        
    return render(request, 'litrevu/home.html', context=context)

@login_required
def posts(request):
    user_has_review = Review.objects.filter(
        ticket=OuterRef("pk"),
        user=request.user
    )
    tickets = Ticket.objects.filter(user=request.user).annotate(has_my_review=Exists(user_has_review))
    reviews = Review.objects.filter(user=request.user)
    allow_map = {t.id: (not t.has_my_review) for t in tickets}
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )
    context = {
        'posts': posts,
        'allow_map': allow_map
    }
    return render(request, 'litrevu/posts.html', context=context)

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'litrevu/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id, user=request.user)
    return render(request,
                  'litrevu/ticket_detail.html',
                  {'ticket': ticket})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            print("FILES: ", request.FILES)
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        else:
            print("ERROR: ", form.errors)
    else:
        form = TicketForm()
    return render(request,
                'litrevu/ticket_create.html',
                {'form': form})

@login_required
def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id, user=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            return redirect('posts')
        else:
            print("ERROR: ", form.errors)
    else:
        form = TicketForm(instance=ticket)
    return render(request,
                'litrevu/ticket_update.html',
                {'form': form})

@login_required
def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, 
                  'litrevu/ticket_delete.html', 
                  {'ticket': ticket})


@login_required
def review_list(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'litrevu/review_list.html', {'reviews': reviews})

@login_required
def review_detail(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)
    return render(request,
                  'litrevu/posts.html',
                  {'review': review})

@login_required
def review_create(request, ticket_id=-1):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home')
        else:
            print("ERROR review_create: ", form.errors)
    else:
        form = ReviewForm()
    return render(request,
                'litrevu/review_create.html',
                {'form': form,
                 'ticket': ticket,})

@login_required
def review_and_ticket_create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, prefix="reviews")
        ticket_form = TicketForm(request.POST, request.FILES, prefix="tickets")
        if ticket_form.is_valid():
            print("FILES: ", request.FILES)
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
        else:
            print("ERROR ticket_form.is_valid: ", ticket_form.errors)
        
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('home', review.id)
        else:
            print("ERROR review_form.is_valid: ", review_form.errors)
        
    else:
        review_form = ReviewForm(prefix="reviews")
        ticket_form = TicketForm(prefix="tickets")
    return render(request,
                'litrevu/review_and_ticket_create.html',
                {'review_form': review_form,
                 'ticket_form': ticket_form,
                 })


@login_required
def review_update(request, id):
    print("WOOAH")
    review = get_object_or_404(Review, id=id, user=request.user)
    ticket = review.ticket
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('posts')
        else:
            print("ERROR: ", form.errors)
    else:
        form = ReviewForm(instance=review)
    return render(request,
                'litrevu/review_update.html',
                {'form': form,
                 'ticket': ticket},)

@login_required
def review_delete(request, id):
    review = get_object_or_404(Review, id=id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, 
                  'litrevu/review_delete.html', 
                  {'review': review})


@login_required
def subscription(request):
    user_blocks = UserBlocks.objects.filter(user=request.user)
    blocked_users = UserBlocks.objects.filter(
        user=request.user).values_list('blocked_user', flat=True)
   
    user_follows = UserFollows.objects.filter(
        Q(user=request.user) & ~Q(followed_user__in=blocked_users))
    subscriber_users = UserFollows.objects.filter(
        Q(followed_user=request.user) & ~Q(followed_user__in=blocked_users))
    if request.method == 'POST':
        form = SubscriptionForm(request.user, request.POST)
        if form.is_valid():
            messages.info(request,
                          'Utilisateur '
                          + request.POST.get('username') + ' suivi')
    else:
        form = SubscriptionForm(request.user)
    context = { 'followed_users': user_follows,
                'subscriber_users': subscriber_users,
                'blocked_users': user_blocks} | {'form': form}
    return render(request, 
                 "litrevu/subscription.html",
                  context=context)

@login_required
def unsubscribe(request, id):
    """ remove the id user from the followed user """
    user = get_object_or_404(UserFollows, id=id)
    user.delete()
    return redirect('subscription')

@login_required
def block(request):
    user_blocks = UserBlocks.objects.filter(user=request.user)
    blocked_users = UserBlocks.objects.filter(
        user=request.user).values_list('blocked_user', flat=True)
   
    user_follows = UserFollows.objects.filter(
        Q(user=request.user) & ~Q(followed_user__in=blocked_users))
    subscriber_users = UserFollows.objects.filter(
        Q(followed_user=request.user) & ~Q(followed_user__in=blocked_users))
    if request.method == 'POST':
        form = BlockingForm(request.user, request.POST)
        if form.is_valid():
            messages.info(request,
                          'Utilisateur '
                          + request.POST.get('username') + ' bloqué')
    else:
        form = BlockingForm(request.user)
    context = { 'followed_users': user_follows,
                'subscriber_users': subscriber_users,
                'blocked_users': user_blocks, } | {'form': form}
    return render(request, 
                 "litrevu/subscription.html",
                  context=context)

@login_required
def unblock(request, id):
    """ remove the id user from the blocked user """
    user = get_object_or_404(UserBlocks, id=id)
    user.delete()
    return redirect('block')
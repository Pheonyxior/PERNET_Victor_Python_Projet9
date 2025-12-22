from django import forms

from litrevu.models import Ticket, Review, UserFollows

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
    #  fields = '__all__'
        exclude = ('user',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user',)

class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        exclude = ('user',)

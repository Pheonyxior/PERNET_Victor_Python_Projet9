from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError


from litrevu.models import Ticket, Review, UserFollows

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
    #  fields = '__all__'
        exclude = ('user',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user',)

class SubscriptionForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.widgets.TextInput(
            attrs={'placeholder': "Nom d'utilisateur"}))


    def __init__(self, user, *args, **kwargs):
        """ set the connected user """
        self.user = user
        # followed_users = UserFollows.objects.filter(user=self.user)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """ check
            -> if the connected user is not the user choice
            -> that the user choice exists
            -> that the user choice is not already in the followed list
        """
        user = self.cleaned_data['username']

        try:
            followed_user = User.objects.get(username=user)
            if followed_user == self.user:
                message = 'Vous ne pouvez pas vous suivre !'
                raise ValidationError(message)
            else:
                try:
                    user_follow = UserFollows.objects.create(
                        user=self.user, followed_user=followed_user)
                    user_follow.save()
                except IntegrityError:
                    message = 'Désolé: ' + followed_user.username\
                        + ' déjà suivi !'
                    raise ValidationError(message)
        except User.DoesNotExist:
            message = user + " n'est pas défini !"
            raise ValidationError(message)

        return user

    class Meta:
        model = UserFollows
        fields = ['username']

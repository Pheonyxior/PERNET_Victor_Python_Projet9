from django.contrib import admin
from litrevu.models import Review, Ticket, UserFollows

admin.site.register([Review, Ticket, UserFollows])
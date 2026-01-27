from django.contrib import admin
from litrevu.models import Review, Ticket, UserFollows, UserBlocks

admin.site.register([Review, Ticket, UserFollows, UserBlocks])
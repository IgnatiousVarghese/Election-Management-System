from django.contrib import admin
from .models import *

admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Election_Coordinator)


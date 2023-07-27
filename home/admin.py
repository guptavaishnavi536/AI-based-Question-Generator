from django.contrib import admin
from home.models import Queries
from home.models import Login
from home.models import Signup
from home.models import QnA



# Register your models here.
admin.site.register(Queries)
admin.site.register(Login)
admin.site.register(Signup)
admin.site.register(QnA)
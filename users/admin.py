from django.contrib import admin

from django.contrib import admin
from .models import *
from django.apps import apps


admin.site.register(ExtendUser)
app=apps.get_app_config('graphql_auth')
for models_name,model in app.models.items():
    admin.site.register(model)


admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post)


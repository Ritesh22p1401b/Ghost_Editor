from graphene_django.types import DjangoObjectType
from .models import *



class ExtendUserType(DjangoObjectType):
    class Meta:
        model = ExtendUser
        fields=["username","email","first_name","last_name"]



class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields='__all__'

class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields='__all__'

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields=("name",)
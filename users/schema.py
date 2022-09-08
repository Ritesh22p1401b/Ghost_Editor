import graphene
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from .types import *

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    pass


#/////......Querying Data........ ////

class Query(graphene.ObjectType):
    all_user=graphene.List(ExtendUserType)
    single_user=graphene.Field(ExtendUserType,id=graphene.Int())
    single_post = graphene.Field(PostType,id=graphene.Int())
    all_post=graphene.List(PostType)
    all_author=graphene.List(AuthorType)
    author= graphene.Field(AuthorType, id=graphene.Int())
    author_by_username = graphene.Field(AuthorType, id=graphene.Int())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
    

    def resolve_all_user(root,info,**kwargs):
        return ExtendUser.objects.all()

    def resolve_single_user(self,info,id):
        return ExtendUser.objects.get(pk=id)

    def resolve_single_post(self,info,id):
        return Post.objects.get(pk=id)

    def resolve_multiple_post(root,info,**kwargs):
        return Post.objects.all()

    def resolve_author(self,info,id):
        return Author.objects.get(pk=id)

    def resolve_all_author(root,info,**kwargs):
        return Author.objects.all()

    
    def resolve_all_post(root, info):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .all()
        )

    def resolve_author_by_username(root, info, id):
        return Author.objects.select_related("username").get(pk=id)

    def resolve_post_by_slug(root, info, slug):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__username__username=username)
        )

    def resolve_posts_by_tag(root, info, tag):
        return (
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

#////........ Mutation start Here........  /////

class CreateTag(graphene.Mutation):

    create_tag = graphene.Field(TagType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(root,info, name):
        name=Tag.objects.create(name=name)
        name.save()
        return CreateTag(create_tag=name) 


class CreateAuthor(graphene.Mutation):
    
    create_author = graphene.Field(AuthorType)
    
    class Arguments:
        id=graphene.Int()
        first_name = graphene.String()
        last_name = graphene.String()
        created_at = graphene.DateTime()
        bio=graphene.String()


    def mutate(self,info,id,first_name ,last_name,bio, **kwargs):
        
        user = ExtendUser.objects.get(pk=id)

        author_create = Author.objects.create(username=user,
            first_name=first_name,
            last_name=last_name,
            created_at=timezone.now(),
            bio=bio
        )
        author_create.save()

        return CreateAuthor(author_create)


class CreatePost(graphene.Mutation):
    
    create_post = graphene.Field(PostType)
    
    class Arguments:
        author_id=graphene.Int()
        # tags_id=graphene.Int()
        title=graphene.String()
        subtitle=graphene.String()
        slug=graphene.String()
        body=graphene.String()
        description=graphene.String()
        published_date = graphene.DateTime()
        published=graphene.Boolean()
        date_modified=graphene.DateTime()


    def mutate(self,info,author_id,title,subtitle,slug,body,description,published, **kwargs):
        
        author = Author.objects.get(pk=author_id)
        # tags=Tag.objects.get(pk=tags_id)

        post_create = Post.objects.create(author=author,
            title=title,
            subtitle=subtitle,
            slug=slug,
            body=body,
            description=description,
            published_date=timezone.now(),
            published=published,
            date_modified=timezone.now()
        )


        post_create.save()
        return CreatePost(post_create)



class Mutation(graphene.ObjectType):
    create_tag = CreateTag.Field()
    create_author = CreateAuthor.Field()
    create_post=CreatePost.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)

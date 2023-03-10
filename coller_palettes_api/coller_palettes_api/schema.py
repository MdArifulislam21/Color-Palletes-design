import graphene
from graphql_jwt.decorators import staff_member_required, superuser_required, login_required
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from graphene import ID, relay
from graphene_django import DjangoObjectType

from coller_pallates.models import *
from coller_pallates.schema import *

from django.contrib.auth.models import User





class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username', 'email']
        interfaces = (relay.Node,)





class UserRegister(relay.ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        
    user = graphene.Field(UserType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        username = input.get('username')
        email = input.get('email')
        password1 = input.get('password1')
        password2 = input.get('password2')
        
        if password1 != password2:
            raise Exception("Password didn't match")
        
        if len(password1) < 6:
            raise Exception("Password should be more then five carrecter")


        user = User.objects.create(username=username,  email= email)
        
        user.set_password(password1)
        
        status = user.status
        status.verified = True
        status.save()
        return UserRegister(user=user)


class Query(UserQuery,  MeQuery, graphene.ObjectType, CollerPalettesQuery):
    pass

class Mutation(graphene.ObjectType):
    login_token = mutations.ObtainJSONWebToken.Field()
    user_register = UserRegister.Field()
    


schema = graphene.Schema(query=Query, mutation=Mutation)


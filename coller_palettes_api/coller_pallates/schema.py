import graphene
from graphene import  relay
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

from .models import *


class ColorPaletteNode(DjangoObjectType):
    class Meta:
        model = ColorPalette
        filter_fields = ['name', 'dominant_color1', 'dominant_color2', 'accent_color1', 'accent_color2', 'accent_color3', 'accent_color4']
        interfaces = (relay.Node,)




class ColorPaletteeReivisionNode(DjangoObjectType):
    class Meta:
        model = ColorPaletteRevision
        filter_fields = ['changes', 'color_palette__name']
        interfaces = (relay.Node,)


class FavoriteNode(DjangoObjectType):
    class Meta:
        model = Favorite
        filter_fields = []
        interfaces = (relay.Node,)


class ColorPaletteCreate(relay.ClientIDMutation):
    message = graphene.String()

    class Input:
        # id = graphene.ID()
        name = graphene.String()
        dominant_color1 = graphene.String(required=True)
        dominant_color2 = graphene.String()
        accent_color1 = graphene.String(required=True)
        accent_color2 = graphene.String(required=True)
        accent_color3 = graphene.String()
        accent_color4  = graphene.String()
        is_public = graphene.Boolean(default_value=True)
        
    color_palette = graphene.Field(ColorPaletteNode)
    
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        # id = input.get()
        name = input.get('name')
        dominant_color1 = input.get("dominant_color1")
        dominant_color2 = input.get("dominant_color2")
        accent_color1 = input.get("accent_color1")
        accent_color2 =input.get("accent_color2")
        accent_color3 = input.get("accent_color3")
        accent_color4  =input.get("accent_color4")
        is_public = input.get("is_public")
        
        user = info.context.user
        coler_palatte = ColorPalette.objects.create(
                name = name,
                dominant_color1=dominant_color1,
                dominant_color2 = dominant_color2,
                accent_color1 =accent_color1,
                accent_color2 = accent_color2,
                accent_color3 =accent_color3,
                accent_color4 = accent_color4,
                is_public= is_public,
                created_by = user
                )
        
        ColorPaletteRevision.objects.create(
            coler_palatte = coler_palatte,
            changes = "created coller palate name " + coler_palatte.name
            )

        return ColorPaletteCreate(coler_palatte = coler_palatte)



class ColorPaletteUpdate(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(default_value = True)
        name = graphene.String()
        dominant_color1 = graphene.String()
        dominant_color2 = graphene.String()
        accent_color1 = graphene.String()
        accent_color2 = graphene.String()
        accent_color3 = graphene.String()
        accent_color4  = graphene.String()
        is_public = graphene.Boolean(default_value=None)
        
    color_palette = graphene.Field(ColorPaletteNode)
    
    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        id = input.get('id')
        name = input.get('name')
        dominant_color1 = input.get("dominant_color1")
        dominant_color2 = input.get("dominant_color2")
        accent_color1 = input.get("accent_color1")
        accent_color2 =input.get("accent_color2")
        accent_color3 = input.get("accent_color3")
        accent_color4  =input.get("accent_color4")
        is_public = input.get("is_public")
        
        id = from_global_id(id)[1]
        try:
            coler_palatte = ColorPalette.objects.get(id=id)
        except:
            raise Exception("coler palettes dosn't exist with this id")
        user = info.context.user
        if coler_palatte.created_by != user:
            raise Exception("Only the owner of this coler palettes can modify.")
        
        changes_list = []
        if name and name != coler_palatte.name:
            coler_palatte.name  = name
            changes_list.append('name chenges to ' + name)
        
        if dominant_color1 and dominant_color1 != coler_palatte.dominant_color1:
            coler_palatte.dominant_color1  = dominant_color1
            changes_list.append('dominant_color1 chenges to ' + dominant_color1)
        
        
        if dominant_color2 and dominant_color2 != coler_palatte.dominant_color2:
            coler_palatte.dominant_color2  = dominant_color2
            changes_list.append('dominant_color2 chenges to ' + dominant_color2)
        
        if accent_color1 and accent_color1 != coler_palatte.accent_color1:
            coler_palatte.accent_color1  = accent_color1
            changes_list.append('accent_color1 chenges to ' + accent_color1)
        
        
        if accent_color2 and accent_color2 != coler_palatte.accent_color2:
            coler_palatte.accent_color2  = accent_color2
            changes_list.append('accent_color2 chenges to ' + accent_color2)
            
        
        if accent_color3 and accent_color3 != coler_palatte.accent_color3:
            coler_palatte.accent_color3  = accent_color3
            changes_list.append('accent_color3 chenges to ' + accent_color3)
            
        
        if accent_color4 and accent_color4 != coler_palatte.accent_color4:
            coler_palatte.accent_color4  = accent_color4
            changes_list.append('accent_color4 chenges to ' + accent_color4)
        
        
        if is_public is not None and is_public != coler_palatte.is_public:
            coler_palatte.is_public  = is_public
            changes_list.append('is_public chenges to ' + is_public)
        
        coler_palatte.save()
        
        chenges = ' and '.join(changes_list)
        
        version = coler_palatte.revisions.last().version + 0.1
        coler_palatte_revision = ColorPaletteRevision.objects.create(
            version = version,
            coler_palatte = coler_palatte,
            changes = chenges
            )

        return ColorPaletteUpdate(coler_palatte = coler_palatte)


""" A user can delete only his coler palates"""
class DeleteColorPalette(graphene.Mutation):
    message = graphene.String()
    
    class Input:
        id = graphene.ID()

    color_palette = graphene.Field(ColorPaletteNode)

    @classmethod
    @login_required
    def mutate(cls, root, info, **input):
        id = input.get("id")
        message = "Something went wrong!"

        if id:
            id = from_global_id(id)[1]
            try:
                color_palette = ColorPalette.objects.get(id=id)
            except:
                raise Exception("Coler palettes does not exist.")
            
            user = info.context.user
            if user == color_palette.created_by:
                color_palette.delete()
                message = "Successfully deleted your object."
            else:
                raise Exception("Only the owner of this coler palettes can delete.")

        return cls(message=message)



""" A user can save others color palettes to his favorite."""
class AddToFavorite(graphene.Mutation):
    message = graphene.String()
    
    class Input:
        color_palate_id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **input):
        id = input.get("id")
        message = "Something went wrong!"

        if id:
            id = from_global_id(id)[1]
            try:
                color_palette = ColorPalette.objects.get(id=id)
            except:
                raise Exception("Coler palettes does not exist.")
            
            user = info.context.user
            if user == color_palette.created_by:
                raise Exception("Only others coler palates can be saved to favorites not owns.")
            else:
                try:
                    favorite = user.favorite
                except:
                    favorite = Favorite.objects.get(user = user)
                    favorite.color_paletes.add(color_palette)
                message = "Successfully added to your favorite."

        return cls(message=message)


class RemoveFromFavorite(graphene.Mutation):
    message = graphene.String()
    
    class Input:
        color_palate_id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate(cls, root, info, **input):
        id = input.get("id")
        message = "Something went wrong!"

        if id:
            id = from_global_id(id)[1]
            try:
                color_palette = ColorPalette.objects.get(id=id)
            except:
                raise Exception("Coler palettes doesn't exists.")
            
            user = info.context.user
            try:
                favorite = user.favorite
            except:
                favorite = Favorite.objects.get(user = user)
                favorite.color_paletes.remove(color_palette)
            message = "Successfully removed from your favorite."

        return cls(message=message)
    
    

class CollerPalettesQuery:
    # ===========================================================================
    coller_pallete = graphene.relay.Node.Field(ColorPaletteNode)
    public_coler_palletes = DjangoFilterConnectionField(ColorPaletteNode)

    def resolve_public_coler_palletes(self, info, **kwargs):
        return ColorPalette.objects.all().select_related('created_by')
    
    private_color_palettes = DjangoFilterConnectionField(ColorPaletteNode)
    @login_required
    def resolve_private_color_palettes(self, info, **kwargs):
        user = info.context.user
        return ColorPalette.objects.filter(user=user, is_public = False).select_related('created_by')
    
    owns_color_palettes = DjangoFilterConnectionField(ColorPaletteNode)
    @login_required
    def resolve_owns_color_palettes(self, info, **kwargs):
        user = info.context.user
        return ColorPalette.objects.filter(user=user).select_related('created_by')
    
    
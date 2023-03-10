from django.db import models
from django.contrib.auth.models import User
from django.db import models
# from django.contrib.postgres.fields import ArrayField



class ColorPalette(models.Model):
    name = models.CharField(max_length=255, unique=True)

    #In every ColorPalate there will at 1-2 dominant color, That means At least one dominanat color will exist.
    dominant_color1 =models.CharField(max_length=7)  # hex code for color , Ex: #FFFFFF
    dominant_color2 =models.CharField(max_length=7,  blank=True, null=True) 
    
    # In every ColorPalate there will at 2-4 accent color,  That means At least two accent color will exist.
    accent_color1 = models.CharField(max_length=7)  
    accent_color2 = models.CharField(max_length=7)  # hex code for color , Ex: #FFFFFF
    accent_color3 = models.CharField(max_length=7, blank=True, null=True)
    accent_color4 = models.CharField(max_length=7, blank=True, null=True)
    
    is_public = models.BooleanField(default=True) # This indicates If the coler palates is public or private
    created_by =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="color_palattes")
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
      

# ColorPaletteRevision  will keep history of every chenges 
class ColorPaletteRevision(models.Model):
    version = models.DecimalField(default=1.0, max_digits=4, decimal_places=1)
    color_palette = models.ForeignKey(ColorPalette, on_delete=models.CASCADE, related_name='revisions')
    changes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        

# Favorite store data of  every users favorite list of coler palettes
class Favorite(models.Model):
    color_paletes = models.ManyToManyField(ColorPalette, related_name='favorites')
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name="favorite")


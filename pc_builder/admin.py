from django.contrib import admin
from .models import Processor, VideoCard, Motherboard, ComputerBuild, UserFavorite

admin.site.register(Processor)
admin.site.register(VideoCard)
admin.site.register(Motherboard)
admin.site.register(ComputerBuild)
admin.site.register(UserFavorite)
from django.contrib import admin
from .models import Kaf
from .models import Group
from .models import Student
from .models import Cooper
from .models import Post
from .models import LikeDislike

admin.site.register(Kaf)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Cooper)
admin.site.register(Post)
admin.site.register(LikeDislike)

from django.contrib import admin
from .models import Kaf
from .models import Group
from .models import Student
from .models import Cooper
from .models import Post
from .models import LikeDislike
from .models import Comment

admin.site.register(Kaf)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Cooper)
admin.site.register(Post)
admin.site.register(LikeDislike)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
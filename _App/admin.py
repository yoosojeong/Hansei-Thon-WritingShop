from django.contrib import admin
from .models import *

# ------------------------------------------------------------------
# TableName   : WritePostModel
# Description : 글귀 테이블
# ------------------------------------------------------------------
@admin.register(WritePostModel)
class WritePostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'images', 'content', 'tag_list']

    def get_queryset(self, request):
        return super(WritePostAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

# ------------------------------------------------------------------
# TableName   : LikeModel
# Description : 좋아요 테이블
# ------------------------------------------------------------------
@admin.register(LikeModel)
class LikeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in LikeModel._meta.fields]
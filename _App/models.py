from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator
from taggit.managers import TaggableManager

# ------------------------------------------------------------------
# TableName   : TimeStampedModel
# Description : 시간 테이블
# ------------------------------------------------------------------
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# ------------------------------------------------------------------
# TableName   : WritePostModel
# Description : 글귀 테이블
# ------------------------------------------------------------------
class WritePostModel(TimeStampedModel):
    class Meta:
        verbose_name_plural = "글귀 테이블"
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='유저')
    images = models.ImageField(null=True, blank=True, verbose_name='이미지')
    content = models.TextField(max_length=300, verbose_name='내용')
    tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
        return str(self.images)

# ------------------------------------------------------------------
# TableName   : LikeModel
# Description : 좋아요 테이블
# ------------------------------------------------------------------
class LikeModel(TimeStampedModel):
    class Meta:
        verbose_name_plural = "글귀별 좋아요 테이블"

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    writePost = models.ForeignKey(WritePostModel, on_delete=models.CASCADE, null=True, related_name='likes')

    def __str__(self):
        return '누른 이: {} - 게시물: {}'.format(self.creator.username, self.writePost.images) 

# ------------------------------------------------------------------
# TableName   : SearchModel
# Description : 검색 테이블
# ------------------------------------------------------------------
class SearchData(TimeStampedModel):

    word = models.CharField(max_length=80)
from django.db import models


# Create your models here.
class Activity(models.Model):
    topic = models.CharField(verbose_name="活动主题", max_length=32)
    detail = models.TextField(verbose_name="活动描述")
    date = models.DateField(verbose_name="活动日期")

    def __str__(self):
        return f'{self.topic}'


class Picture(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name="关联的活动")
    photo = models.ImageField(verbose_name="活动图片", upload_to="activity")
    description = models.TextField(verbose_name="图片描述")

    def __str__(self):
        return f'{self.description}'

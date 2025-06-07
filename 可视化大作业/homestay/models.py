from django.db import models

# Create your models here.

# 区域民宿数量统计
class AdsAreaCount(models.Model):
    district_name = models.CharField(max_length=64, null=True)
    count = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_area_count'


# 价格消费统计
class AdsCostUseCount(models.Model):
    price = models.CharField(max_length=64, null=True)
    consume_count = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_cost_use_count'


# 收藏使用统计
class AdsFavUseCount(models.Model):
    fav_count = models.IntegerField(null=True)
    consume_count = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_fav_use_count'


# 评分使用统计
class AdsRateUseCount(models.Model):
    star_rating = models.CharField(max_length=64, null=True)
    consume_count = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_rate_use_count'


# 标签映射统计
class AdsTagMapCount(models.Model):
    tag = models.CharField(max_length=64, null=True)
    count = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_tag_map_count'


# 类型统计
class AdsTypeCount(models.Model):
    layout_desc = models.CharField(max_length=64, null=True)
    count = models.BigIntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'ads_type_count'


# 城市信息
class CityCodeInfo(models.Model):
    city_code = models.CharField(primary_key=True, max_length=64)
    city_name = models.CharField(max_length=64, null=True)
    province_code = models.CharField(max_length=64, null=True)
    province_name = models.CharField(max_length=64, null=True)

    class Meta:
        managed = False
        db_table = 't_city_code_info'


# 评论信息
class CommentInfo(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=64)
    room_id = models.CharField(max_length=64, null=True)
    user_id = models.CharField(max_length=64, null=True)
    content = models.TextField(null=True)
    create_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 't_comment_info'


# 日志信息
class LogInfo(models.Model):
    log_id = models.CharField(primary_key=True, max_length=64)
    user_id = models.CharField(max_length=64, null=True)
    room_id = models.CharField(max_length=64, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    create_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 't_log_info'


# 用户信息
class UserInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=64)
    username = models.CharField(max_length=64, null=True)
    password = models.CharField(max_length=64, null=True)
    gender = models.CharField(max_length=8, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=64, null=True)
    create_time = models.DateTimeField(null=True)
    update_time = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 't_user_info'

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Kaf(models.Model):
    course = models.CharField(max_length=30, null=True)
    num = models.IntegerField(null=True)

class Group(models.Model):
    kaf = models.ForeignKey(Kaf, null=True, on_delete=models.SET_NULL)
    number = models.CharField(max_length=10, null=True)
    timetable = models.TextField(null=True)
    
class Student(models.Model):
    stud = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_UN_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    year_in_un = models.CharField(max_length=2, 
                                  choices=YEAR_IN_UN_CHOICES, 
                                  default=FRESHMAN, db_index=True)

    def is_upperclass(self):
        return self.year_in_un in (self.JUNIOR, self.SENIOR)
#
#    class Meta:
#        indexes = [['first_name', 'last_name'],]
#
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()

class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name= ("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name= ("Пользователь"), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()

class Cooper(models.Model):
    coop = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    kaf = models.ForeignKey(Kaf, db_index=True, null=True, on_delete=models.SET_NULL)

class Post(models.Model):
    author = models.ForeignKey(Cooper,  null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField('date created', auto_now=True)
    text = models.TextField(max_length=500, blank=True)
    votes = GenericRelation(LikeDislike, related_query_name='posts')
    class Meta:
        ordering = ['-created_at']
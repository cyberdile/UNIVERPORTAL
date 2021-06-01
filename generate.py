import django
django.setup()
from django.contrib.auth import get_user_model
from univer.models import Kaf, Group, Student, Cooper, Post
from django.utils import timezone
from datetime import datetime, date, time

UserModel = get_user_model()

for i in range(10, 15):
    k = str(i)
    user=UserModel.objects.create_user(username=k, first_name= 'name' + k, last_name = 'last' + k, password='bar')
    user.is_superuser=False
    user.is_staff=False
    user.save()

    kaf=Kaf(course = 'course' + k, num = k)
    kaf.save()

    group=Group(number= i, timetable = 'TIMETABLE')
    group.kaf = Kaf.objects.get(id=i+1)
    group.save()

    student=Student(birth_date=timezone.now(), bio= 'HELLO MY NAME IS ' + k)
    student.stud = UserModel.objects.get(username=k)
    student.group = Group.objects.get(id=i+1)
    student.save()
    
    cooper=Cooper()
    cooper.coop = UserModel.objects.get(username=k)
    cooper.kaf = Kaf.objects.get(id=i+1)
    cooper.save()

    post=Post(created_at=timezone.now(), text= 'HELLO, WORLD!', title='Very important post' + k)
    post.author = Cooper.objects.get(id=i+1)
    post.save()

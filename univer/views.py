import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from univer.models import Student, Post, Cooper, User, Kaf, Group, LikeDislike, Comment
from .forms import PostForm, KafForm, CommentForm, SignUpForm
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views import View
from rest_framework_swagger import renderers
from rest_framework.decorators import api_view, renderer_classes

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def index(request):
    return render(request, 'index.html')

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def hello(request):
    return render(request, 'univer/hello.html')

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # user_author = Cooper.objects.get(pk=request.user.id)
    # Список активных комментариев к этой записи
    comments = Comment.objects.filter(active=True, post=post_id)
    new_comment = None
    if request.method == 'POST':
        # Комментарий был опубликован
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создайте объект Comment, но пока не сохраняйте в базу данных
            new_comment = comment_form.save(commit=False)
            # Назначить текущий пост комментарию
            new_comment.post = post
            new_comment.name = request.user
            # Сохранить комментарий в базе данных
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render (
            request, 'posts/post_detail.html',
            {'posts': post,
             'comments': comments,
             'new_comment': new_comment,
             'comment_form': comment_form
             })

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(
            request, 'posts/post_list.html',
            {'posts': posts}
            )

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
# def next_posts(request, page_number):
#     posts = Post.objects.all().order_by('-created_at')
#     p = Paginator(posts, 5)
#     page = page_number
#     next = p.get_page(page)
#     return render(request, 'posts/next_posts.html',
#              {'posts':next})

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def save_post_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.instance.author = request.user
            form.save()
            data['form_is_valid'] = True
            posts = Post.objects.all().order_by('-created_at')
            data['html_post_list'] = render_to_string('posts/partial_post_list.html', {
                'posts': posts
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name,
        context,
        request=request
    )
    return JsonResponse(data)

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
    else:
        form = PostForm()
    return save_post_form(request, form, 'posts/partial_post_create.html')

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
    else:
        form = PostForm(instance=post)
    return save_post_form(request, form, 'posts/partial_post_update.html')

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def kaf_detail(request, kaf_id):
    kafs = Kaf.objects.filter(id = kaf_id)
    return render (
            request, 'univer/kaf_detail.html',
            {'kafs': kafs}
            )

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def kaf_list(request):
    kafs = Kaf.objects.order_by('num')
    return render (
            request, 'univer/kaf_list.html',
            {'kafs': kafs}
            )

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def save_kaf_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            kafs = Kaf.objects.all()
            data['html_kaf_list'] = render_to_string('univer/partial_kaf_list.html', {
                'kafs': kafs
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name,
        context,
        request=request
    )
    return JsonResponse(data)

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def kaf_create(request):
    if request.method == 'POST':
        form = KafForm(request.POST)
    else:
        form = KafForm()
    return save_kaf_form(request, form, 'univer/partial_kaf_create.html')

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def kaf_update(request, kaf_id):
    kaf = get_object_or_404(Kaf, id=kaf_id)
    if request.method == 'POST':
        form = KafForm(request.POST, instance=kaf)
    else:
        form = KafForm(instance=kaf)
    return save_kaf_form(request, form, 'univer/partial_kaf_update.html')

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def group_detail(request, group_id, kaf_id):
    groups = Group.objects.filter(id = group_id)
    groups1 = groups.filter(id = kaf_id)
    return render (
    request, 'univer/group_detail.html',
            {'groups': groups}
            )

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def group_list(request, kaf_id):
    groups = Group.objects.filter(kaf_id = kaf_id)
    return render (
            request, 'univer/group_list.html',
            {'groups': groups}
            )

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def student_detail(request, student_id, group_id, kaf_id):
    students = Student.objects.filter(id = student_id)
    students1 = students.filter(id = group_id)
    students2 = students1.filter(id = kaf_id)
    return render (
            request, 'univer/student_detail.html',
            {'students' :students}
            )

# @api_view(['GET'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def student_list(request, group_id):
    students = Student.objects.filter(group_id = group_id)
    return render (
            request, 'univer/student_list.html',
            {'students': students}
            )

# @api_view(['GET', 'POST'])
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def register(request):
    if request.method == 'POST':
        new_user = None
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_superuser = 0
            new_user.is_staff = 0
            new_user.is_active = 1
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('hello')
    else:
        form = SignUpForm()

    context = {'form' : form}
    return render(request, 'registration/register.html', context)


class VotesView(View):
    model = None    # Модель данных - Статьи или Комментарии
    vote_type = None # Тип комментария Like/Dislike

    # @api_view(['GET'])
    # @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
    def post(self, request, post_id):
        obj = self.model.objects.get(id=post_id)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

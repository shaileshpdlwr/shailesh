from django.shortcuts import render,get_object_or_404
from blog.models import Post,Comment
from blog.forms import EmailForm,CommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
#Create your views here.


def post_list_view(request, tag_slug=None):
    post_list = Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list,2)
    page_number = request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'post_list': post_list, 'tag':tag})

def post_detail(request,slug):
    post=Post.objects.get(slug=slug)
    post_tags_ids=post.tags.values_list('id',flat=True)
    
    similar_posts=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    comments=post.comments.filter(active=True)

   # print(comments[0])
    cform=CommentForm()
    if request.method=='POST':
        cform=CommentForm(request.POST)
        if cform.is_valid():
            new_comment=cform.save(commit=False)
            new_comment.post=post
            new_comment.save()

    return render(request,'blog/post_detail.html',{ 'post': post,'comments':comments,'cform':cform ,'similar_posts':similar_posts})
    
from django.views.generic import View,ListView
class PostListView(ListView):
    model=Post
    paginate_by=1

def mail_send_view(request,id):
    post=Post.objects.get(id=id)
    form=EmailForm()
    if request.method=="POST":
        form=EmailForm(request.POST)
        if form.is_valid():        
            cd=form.cleaned_data
            subject='{}({}) recommands you to read {}'.format(cd['name'],cd['email'],post.title)
            msg=cd['comment']
            sender='srp232020@gmail.com'
            receiver=[cd['to']]
            send_mail(subject,msg,sender,receiver,fail_silently=False)
    return render(request,'blog/sharebymail.html',{'form':form})

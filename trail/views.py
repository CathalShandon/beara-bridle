from django.shortcuts import render, get_object_or_404, reverse, redirect
from .forms import CommentForm, CreatePostForm, EditPostForm, DeletePostForm
from .forms import ProfileEditForm
from django.views import generic, View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Profile


class PostList(generic.ListView):
    """Displays Post List page"""
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):
    """Displays Post detail page."""

    def get(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
                request,
                "post_detail.html",
                {
                    "post": post,
                    "comments": comments,
                    "commented": False,
                    "liked": liked,
                    "comment_form": CommentForm()
                },
            )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
            else:
                comment_form = CommentForm()

            return render(
                request,
                "post_detail.html",
                {
                    "post": post,
                    "comments": comments,
                    "commented": True,
                    "liked": liked,
                    "comment_form": CommentForm()
                },
            )


class PostLike(View):

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


@login_required
def create_post(request):
    """ Diplays Create a Post page """
    create_post_form = CreatePostForm(request.POST or None, request.FILES)
    if create_post_form.is_valid():
        create_post_form.instance.author = request.user
        create_post_form.save()
        messages.success(
                    request,
                    'Your post is successfully submitted'
                    'and is awaiting for approval')
        return redirect('posts')
    return render(
                request,
                'post_create.html',
                context={'create_post_form': create_post_form}
                )


@login_required
def edit_post(request, slug):
    """ Edit requested post"""
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        raise Http404

    edit_post_form = EditPostForm(
                                data=(request.POST or None),
                                files=(request.FILES or None),
                                instance=post,
                                )
    if edit_post_form.is_valid():
        edit_post_form.save()
        messages.success(request, 'Your post is successfully updated')
        return redirect('trail')
    return render(
                request, 'post_edit.html',
                context={
                    'edit_post_form': edit_post_form,
                    'slug': slug},
                )


@login_required
def delete_post(request, slug):
    """Displays Delete post page"""
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        raise Http404
    delete_post_form = DeletePostForm(request.POST or None)
    if delete_post_form.is_valid():
        post.delete()
        messages.success(request, 'Your post is successfully deleted')
        return redirect('posts')
    return render(
                request,
                'post_delete.html',
                context={'delete_post_form': delete_post_form, }
            )


@login_required
def edit_profile(request):
    """ Display the user's profile to edit """
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(
                            request.POST or None,
                            request.FILES,
                            instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is successfully updated')
            return redirect('profile')
        else:
            messages.error(request,
                           ('Update failed. Please ensure'
                            'the form is valid.'))
    else:
        form = ProfileEditForm(instance=profile)
    template = 'profile_edit.html'
    context = {'form': form, }

    return render(request, template, context)


class ProfileList(LoginRequiredMixin, generic.ListView):
    """Displays the member list page"""
    model = Profile
    queryset = Profile.objects.all()
    template_name = "profile.html"
    paginate_by = 8


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    """Displays profile detail page"""
    model = Profile
    queryset = Profile.objects.all()
    template_name = 'profile_detail.html'

    def get_object(self):
        return get_object_or_404(
                                Profile,
                                user__username=self.kwargs['username'])


def Home(request):
    """
        Renders the home page 

    """
    return render(request, 'base.html')


def AboutUs(request):
    """
         Renders the about us page
        Args:
        request (object): HTTP request object.
        Returns:
        render about us page
    """
    return render(request, 'aboutus.html')

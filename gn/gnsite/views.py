from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from gnsite.models import Post
from django.contrib.auth.models import User
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from gnsite.forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login

class IndexView(generic.ListView):
    template_name = 'site/index.html'
    context_object_name = 'posts'
    latest = False

    def get_queryset(self):
        # filter(parent=None) gets posts which aren't comments
        if self.latest:
            return Post.objects.filter(parent=None).order_by('-dt_created')

        # sorted(.., lambda..) allows ordering via expensive scoring function...
        objects = Post.objects.filter(parent=None)
        objects = sorted(objects.all(), key=lambda x: x.get_score(), reverse=True)
        return objects

class DetailView(generic.edit.FormMixin, generic.DetailView):
    model = Post
    template_name = 'site/detail.html'
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=request.session['post'] if 'post' in request.session else {})
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if 'post' in request.session:
            del request.session['post']
            #request.session.modified = True
        return render(request, self.template_name, {'comment_form': form, 'post': post})

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'site/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.op = self.request.user
        form.instance.save()
        form.instance.votes.add(form.instance.op) # you always vote for your own
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = 'site/post_form.html'
    form_class = PostForm

    # this introduces a little display bug if non-op tries to edit
    # but it's cheap and works and hiding the links upfront should make 
    # this an edge case
    def test_func(self, user):
        return (user == self.get_object().op)

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('profile')
    template_name = 'site/post_confirm_delete.html'


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'site/comment_update_form.html'
    form_class = CommentForm

    def get_success_url(self):
        p = self.get_object()
        while p.parent:
            p = p.parent
        return reverse('detail', kwargs={'pk':p.id})

class ProfileView(generic.DetailView):
    model = User
    template_name = 'site/profile.html'
    context_object_name = 'profile'

    # hackish..
    def get(self, request, *args, **kwargs):
        if not self.get_object():
            return HttpResponseRedirect('/accounts/login/?next=/accounts/profile')
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_object(self):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
        else:
            username = self.request.user.username
        if not username:
            return None
        return User.objects.get(username=username)

def addcomment(request, pk):
    p = get_object_or_404(Post, pk=pk)
    if not request.user.is_authenticated():
        if request.method == "POST":
            request.session['post'] = request.POST
            print(request.session['post'])
        return redirect_to_login(request.path)
    else:
        if request.method == "POST":
            f = CommentForm(request.POST, request.FILES)
            if f.is_valid():
                comment = Post()
                comment.op = request.user
                comment.desc = f.cleaned_data['desc']
                comment.parent = p
                comment.save()
                comment.votes.add(comment.op)
            while p.parent: # traverse back to topmost post
                p = p.parent
    return HttpResponseRedirect(reverse('detail', kwargs={'pk':p.id}))

@login_required
def upvote(request, pk):
    p = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        p = get_object_or_404(Post, pk=pk)
        if request.user not in p.votes.all():
            p.votes.add(request.user)
            p.save()
            while p.parent:
                p = p.parent
    return HttpResponseRedirect(reverse('detail', kwargs={'pk':p.id}))

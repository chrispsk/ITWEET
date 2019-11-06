from django.shortcuts import render, redirect, get_object_or_404
from .models import Tweet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from .forms import TweetModelForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

############ CLASS BASED VIEW EXAMPLE
class TweetDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=kwargs['pk'])
        context = {'object': tweet}
        return render(request, 'tweets/detail_view.html', context)


class TweetListView(ListView):
    template_name = "tweets/list_view.html"
    queryset = Tweet.objects.all()

# FUNCTION BASED VIEWS

def tweet_detail_view(request, pk):
    # Metoda 1
    detail = get_object_or_404(Tweet, pk=pk)
    # Metoda 2
    # try:
    #     detail = Tweet.objects.get(pk=pk)
    # except:
    #     raise Http404()

    context = {
        "object": detail
    }
    return render(request, "tweets/detail_view.html", context)

def tweet_list_view(request):
    form = TweetModelForm(request.POST or None)
    #queryset = Tweet.objects.all().order_by('-pk') #-timestamp
    queryset = Tweet.objects.all()
    query = request.GET.get('q', None)
    if query is not None:
        qs = Tweet.objects.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )#.order_by('-pk')
        return render(request, "tweets/list_view.html", {'object_list':qs})
    context = {
        "object_list": queryset, "form": form
    }
    return render(request, "tweets/list_view.html", context)



@login_required(login_url='/admin')
def tweet_create_view(request):
    form = TweetModelForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect("list")
    context = {
        "form": form
    }
    return render(request, "tweets/create_view.html", context)


@login_required(login_url='/admin')
def tweet_update_view(request, pk):
    obj = get_object_or_404(Tweet, pk=pk)
    form = TweetModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        objd = form.save(commit=False)
        objd.save()
        form = TweetModelForm() # to clear the input
        return HttpResponseRedirect('/tweet/{num}'.format(num=objd.id))
    return render(request, 'tweets/update_view.html', {'form':form})

@login_required(login_url='/admin')
def delete_view(request, pk=None):
    obj = get_object_or_404(Tweet, pk=pk)
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect('/tweet/')
    return render(request, "tweets/delete_confirm.html", {'obj':obj})

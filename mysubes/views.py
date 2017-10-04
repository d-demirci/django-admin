from django.shortcuts import render

# Create your views here.
class SubeDetail(DetailView):
    model = Sube
    template_name = 'mysubes/sube_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SubeDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = SubeReview.RATING_CHOICES
        return context

class SubeCreate(LoginRequiredMixin, CreateView):
    model = Restaurant
    template_name = 'mysubes/form.html'
    form_class = SubeForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(SubeCreate, self).form_valid(form)

class APISubeList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    model = Sube
    queryset = Sube.objects.all()
    serializer_class = SubeSerializer

class APISubeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    model = Sube
    queryset = Sube.objects.all()
    serializer_class = SubeSerializer
        

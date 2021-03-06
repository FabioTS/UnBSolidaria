from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from .models import Noticia, FAQ, Trabalho
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.views import generic
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from .models import Noticia, FAQ
from django.template import RequestContext
from django.views import generic
from .forms import ContactForm, UserForm
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
    template_name = '../templates/index.html'
    context_object_name = {}

    def get_queryset(self):
        return Noticia.objects.all()


class UserFormView(View):
    form_class = UserForm
    template_name = '../templates/registration_form.html'

    # mostrar um form em branco
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # processar informacoes
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)  # cria um objeto, porem n coloca no banco ainda

            # normaliza
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returna objeto se esta tudo certo com as credenciais
            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:  # analisa se o usuario esta ativo, ou seja, n esta banido nem nada
                    login(request, user)
                    return redirect('../')

        return render(request, self.template_name,
                      {'form': form})  # se o usuario nao for valido, returna ele pro formulario de novo


def contato(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          ['rafaeltbt@gmail.com'])
                form = ContactForm()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        return render_to_response("contato/contato.html", {'form': form,
                                                           'mensagem': 'Email enviado com sucesso!'},
                                  context_instance=RequestContext(request))
    return render(request, "contato/contato.html", {'form': form})


def faq(request):
    faq_list = FAQ.objects.all()
    paginator = Paginator(faq_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        perguntas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        perguntas = paginator.page(paginator.num_pages)

    return render_to_response('faq/lista.html', {'perguntas': perguntas}, context_instance=RequestContext(request))


def noticias(request):
    noticias_list = Noticia.objects.all()
    paginator = Paginator(noticias_list, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        noticias = paginator.page(page)
    except (EmptyPage, InvalidPage):
        noticias = paginator.page(paginator.num_pages)

    return render_to_response('noticia/lista.html', {'noticias': noticias}, context_instance=RequestContext(request))


class TrabalhosView(generic.ListView):
    template_name = '../templates/trabalhos/listaTrabalhos.html'
    context_object_name = 'lista_trabalhos'
    paginate_by = 5

    def get_queryset(self):
        return Trabalho.objects.all()

class TrabalhoCreate(generic.CreateView):
    template_name = '../templates/trabalhos/criarTrabalho.html'
    model= Trabalho
    fields = ['titulo', 'descricao', 'vagas', 'data_inicio', 'data_fim', 'dias']
    success_url='/listaTrabalhos'

class TrabalhoUpdate(generic.UpdateView):
    template_name = '../templates/trabalhos/editarTrabalho.html'
    model = Trabalho
    fields = ['titulo', 'descricao', 'vagas', 'data_inicio', 'data_fim', 'dias']
    success_url='/listaTrabalhos'

class TrabalhoDelete(generic.DeleteView):
    template_name = '../templates/trabalhos/deletarTrabalho.html'
    model = Trabalho
    success_url = reverse_lazy('lista-trabalhos')

class TrabalhoDetailView(generic.DetailView):
    template_name = '../templates/trabalhos/visualizarTrabalho.html'
    model=Trabalho
    def get_context_data(self, **kwargs):
        context = super(TrabalhoDetailView, self).get_context_data(**kwargs)
        return context
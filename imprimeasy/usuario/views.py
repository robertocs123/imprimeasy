from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login as auth_login
from api.models import Usuario, Arquivo
from django.http import HttpResponseRedirect
from .forms import Login, Impressao
from api.forms import Aluno 
from django.contrib.auth.models import User
import PyPDF2
import requests



def index(request):
    mat= request.user.username
    if mat == 'admin':
        return redirect('login')
    matricula = request.user
    if not request.user.is_authenticated: #caso não tenha internet ou bug no suap
        return redirect('login')
    else:
        return render(request, 'aluno/main.html', {'matricula':matricula})

@csrf_exempt
def autenticar(request, matricula):
    users = Usuario.objects.all() # users = Todos os usuarios
    if not Usuario.objects.filter(matricula=matricula).exists():
        Usuario.objects.create(matricula=matricula)
    return HttpResponse("sucesso")

@csrf_exempt
def solicitar(request):
    mat= request.user.username
    if mat == 'admin':
        return redirect('login')
    matricula = request.user
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'aluno/solicitar.html',{'matricula': matricula})
        
@csrf_exempt
def login(request): 
    suapUrl='https://suap.ifrn.edu.br/api/v2/autenticacao/token/'
    matricula = ''
    senha=''
    if request.method =='POST':
        formularioLogin = Login(request.POST or None)

        if formularioLogin.is_valid():
            matricula = request.POST['matricula']
            senha = request.POST['senha']
            try:
                requisicao = requests.post(suapUrl,
                 data={'username': matricula, 'password': senha})
            except requests.exceptions.ConnectionError:
                return render(request, 'aluno/login.html', {'alerta2': 'Erro'})
            
            if 'token' in requisicao.text:
                
                users = Usuario.objects.all() # users = Todos os usuarios
                if not Usuario.objects.filter(matricula=matricula).exists():
                    Usuario.objects.create(matricula=matricula)
                    
                user = authenticate(request=request,username=matricula, password=senha)
                if user is not None:

                    auth_login(request, user)
                    return redirect('menu')
                    #return HttpResponse('Autenticado')
                else:
                    try:
                        user = User.objects.get(username = matricula)
                        if not user is None:
                            user.set_password(senha)
                            user.save()
                    except:
                        user = User.objects.create_user(username = matricula, password = senha)

                    
                    user = authenticate(request=request, username=matricula, password=senha)
                    if user is not None:
                        auth_login(request, user)
                        return redirect('menu')
                    else:
                        return render(request, 'aluno/login.html')

                    return redirect('menu')

                #if not User.objects.filter(username=matricula).exists():
                #    user = User.objects.create_user(matricula, senha)
 
            else:
                return render(request, 'aluno/login.html', {'alerta': 'Erro'})
    else:
        return render(request, 'aluno/login.html')

    

def enviarImprimir(request):
    if not request.user.is_authenticated:
        return redirect('login')

    
    if request.method =='POST':
        formularioImpressao = Impressao(request.POST, request.FILES)
        if formularioImpressao.is_valid():
            matricula = request.user
            nome = request.user.username
            if nome == 'admin':
                return render(request, 'aluno/login.html', {'alerta3': 'Erro'})

            cor = formularioImpressao.cleaned_data['cor']
            copias = formularioImpressao.cleaned_data['copias']
            obs = formularioImpressao.cleaned_data['obs']
            arquivo = request.FILES['arquivo']
            fs = FileSystemStorage()
            arq = fs.save(arquivo.name, arquivo )
            try:
                pag = PyPDF2.PdfFileReader(arquivo, 'rb')
                tpag = pag.getNumPages()
                if cor == 1:
                    valor = (tpag*0.5*copias)
                if cor ==0:
                    valor = (tpag*0.25*copias)
            except:
                return render(request, 'aluno/solicitar.html',{'alerta_envio3': 'ok','matricula': matricula} )
            if arquivo.size > 10485760: # 10 MB
                return render(request, 'aluno/main.html',{'alerta_envio5': '0', 'matricula': matricula})
            usuario = Usuario.objects.get(matricula=matricula)
            saldo = usuario.saldo
            if  saldo < valor:
                return render(request, 'aluno/solicitar.html',{'alerta_envio4': '0','valor':valor,'saldo':saldo,'matricula':matricula})
                
            Arquivo.objects.create(nome=arquivo.name, 
                arquivo=arquivo, valor=valor, copias=copias, obs= obs, cor=cor,
                usuario=Usuario.objects.get(matricula=matricula), url=fs.url(arq))

            
            


            return render(request, 'aluno/main.html',{'alerta_envio': 'ok', 'matricula':matricula, 'valor':valor})

        else: 
            return render(request, 'aluno/solicitar.html',{'alerta_envio2': '0','matricula':matricula})#se der qualquer erro
    else:
        return render (request, 'aluno/solicitar.html', 
            {'formularioImpressao':formularioImpressao, 'matricula':matricula})
    

def historico(request): 
    if not request.user.is_authenticated: 
        return redirect('login') 
        
    matricula = request.user.username
    if matricula == 'admin':
        return redirect('login')
    mat = request.user
    u = Usuario.objects.get(matricula=matricula)
    return render(request, 'aluno/historico.html', 
        {'arquivos': Arquivo.objects.filter(usuario=u), 'matricula':mat}) 
    

def saldo(request):
    mat= request.user.username
    if mat == 'admin':
        return redirect('login')
    matricula = request.user
    usuario = Usuario.objects.get(matricula=matricula)
    saldo = usuario.saldo
    return render(request, 'aluno/main.html', 
        {'verifica_saldo': 'OK', 'valor':saldo, 'matricula':matricula})

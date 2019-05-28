from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import Usuario, Arquivo
from .forms import Saldo, Aluno
import PyPDF2


@csrf_exempt
def index(request):#inicio, será passado as solicitações de impressão pendentes para o ADM
    if not request.user.is_authenticated:
        return redirect('loginGrafica')
    else:
        return render(request, 'api/main.html', 
            {'arquivos': Arquivo.objects.all().filter(status=Arquivo.AGUARDANDO)})

@csrf_exempt
def autenticar(request, matricula):#autentica os usuários no sistema
    users = Usuario.objects.all() # users = Todos os usuarios
    if not Usuario.objects.filter(matricula=matricula).exists():
        Usuario.objects.create(matricula=matricula)
    return HttpResponse("sucesso")


@csrf_exempt
def arquivo(request): # Função para receber arquivo do aplicativo kivy
    if request.method == 'POST' and request.FILES['arquivo']:
        matricula = request.POST['matricula']
        if not Usuario.objects.filter(matricula=matricula).exists():
            return HttpResponse("Tentando fazer upload sem logar")
        arquivo = request.FILES['arquivo']
         
        if arquivo.size > 10485760: # 10 MB
            return HttpResponse("Arquivo muito grande, máximo de 10 mb")
        fs = FileSystemStorage()
        arq = fs.save(arquivo.name, arquivo )
        pag = PyPDF2.PdfFileReader(arquivo, 'rb')
        tpag = pag.getNumPages()
        valor = (tpag*0.25)

        Arquivo.objects.create(nome=arquivo.name, valor=valor,
            usuario=Usuario.objects.get(matricula=matricula), url=fs.url(arq))
        return HttpResponse('Arquivo enviado com sucesso, aguarde a impressão, veja na página de status.')
    return HttpResponse("Error")

@csrf_exempt
def negar(request, negar_id): # Função para negar a impressão | Ele serve para mudar o STATUS do arquivo
    arquivo = get_object_or_404(Arquivo, pk=negar_id)
    arquivo.status = Arquivo.NEGADO
    arquivo.save()
    return redirect('main')

@csrf_exempt
def status(request, matricula):#esta função serve para a que o aplicativo possa pegar os status dos arquivos
    estudante = get_object_or_404(Usuario, matricula=matricula)
    arquivos = estudante.arquivo_set.order_by('-id')
    if len(arquivos) == 0:
        return HttpResponse(['Nenhum arquivo para mostrar'])
    todos_arquivos = []
    for arquivo in arquivos:
        todos_arquivos.append(arquivo.nome + ' - ' + arquivo.get_status_display()) 
    return HttpResponse(', '.join(todos_arquivos))

@csrf_exempt
def impresso(request, imp_id, matricula): # Função para diminuir o saldo automaticamente e mudar status de aguardando para impresso
    matricula = matricula
    usuario = Usuario.objects.get(matricula=matricula)
    saldo = usuario.saldo

    arquivo = get_object_or_404(Arquivo, pk=imp_id)
    valor = arquivo.valor
    if saldo < valor:
        return render(request,'api/main.html', 
                {'alerta2': 'Sucesso','saldo':saldo, 'matricula': matricula,
                 'arquivos': Arquivo.objects.all().filter(status=Arquivo.AGUARDANDO)})
    else:
        usuario.saldo -= valor
        usuario.save() 
        arquivo.status = Arquivo.IMPRESSO
        arquivo.save()
        return redirect('main')

@csrf_exempt
def saldo(request): #função que adiciona saldo na conta do aluno
    formulario = Saldo(request.POST or None)
    matricula = ''
    valor = ''
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method=='POST':
        
        if formulario.is_valid():
            matricula = formulario.cleaned_data['matricula']
            valor = formulario.cleaned_data['valor']
        
        if  Usuario.objects.filter(matricula=matricula).exists():
            usuario = Usuario.objects.get(matricula=matricula)
            usuario.saldo += int(valor)  # 
            usuario.save()
            if int(valor) == 1:
                return render(request,'api/main.html', 
                {'alerta3': 'Sucesso','valor':valor,'matricula':matricula,
                 'arquivos': Arquivo.objects.all().filter(status=Arquivo.AGUARDANDO)})

            return render(request,'api/main.html', 
                {'alerta1': 'Sucesso','valor':valor,'matricula':matricula,
                 'arquivos': Arquivo.objects.all().filter(status=Arquivo.AGUARDANDO)})
        else:
            return render(request, 'api/main.html', 
                {'alerta': 'A matricula não existe',
                'arquivos': Arquivo.objects.all().filter(status=Arquivo.AGUARDANDO)})
    else:
        return render(request, 'api/main.html', {'formulario': Saldo()})


@csrf_exempt
def todas_impressoes(request):#função que devolve todas as solicitações de impressão p/ o ADM
    return render(request, 'api/main.html', 
            {'arquivos': Arquivo.objects.all()})
    

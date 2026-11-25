from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory, askopenfile
from tkinter.messagebox import showerror, showinfo
import tkinter.font as tkFont
import os
import shutil
import os
from tela3 import Tela
from tela5 import Tela5
from db2 import DB

def backup():
    #obter banco de dados salvo ou indicado na string
    banco_original = database.db_nome
    banco_backup = f"{banco_original}_backup.db"
    if banco_original not in os.listdir():
        return
    #copiar banco de dados
    shutil.copyfile(banco_original, banco_backup)
def show_tela1():
    resetar_frame4_tela4_linha3()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela3_linha1()
    tela1.pack(fill=BOTH, expand=1)
    tela3.pack_forget()
    #coleta todas as empresas já registradas e as insere na combobox
    #deletar todos os itens do dicionário
    tela4.pack_forget()
    resetar_tela4_lado_direito()
def show_tela3():
    tela1.pack_forget()
    tela4.pack_forget()
    preencher_lista_empresas()
    tela3.pack(fill=BOTH, expand=1)
def show_tela4():
    tela1.pack_forget()
    tela3.pack_forget()
    tela4.empresacnpj_combobox["values"] = ("\0", )
    tela4.empresacnpj_combobox["values"] = preenche_empresa_cnpj()
    preencher_treeview_c_propostas()
    tela4.pack(expand=1, fill=BOTH)
def encerrar_tudo():
    #ao encerrar o programa, aperte o x, o banco de dados é desconectado também
    if database.retorna_connection():
        database.fechar_connection()
    root.destroy()

# print(os.path.dirname(os.path.realpath(__file__)))    
root = Tk()
root.geometry("1200x600+0+0")
root.protocol("WM_DELETE_WINDOW", encerrar_tudo)
root.configure(bg="black")
root.option_add('*TCombobox*Listbox.font', "Arial 18")
clientes = {}
combo_font = tkFont.Font(family="Arial", size=18)
root.state('zoomed')
database = DB()


###tela1############################################################################################################################################
def conecta_ao_db(abre_db_salvo = 0, abre_db_enter = 0):
    if(abre_db_salvo == 1) or (abre_db_enter == 1):
            #obter db salvo na memória
            nome_do_db = nome_do_db_entry.get().strip()
    else:
        #se string for incorreta, abrir caixa de diálogo para arquivo
        file_info = askopenfile(mode='r', filetypes=("Arquivo DB",), initialdir="C:\\")
        if file_info == None:
            return #operação de coleta de arquivo foi cancelada
        nome_do_db = file_info.name #caminho completo + extensão
        if not verifica_nome_db(nome_do_db):
            return
    #fechar conexão aberta
    if database.retorna_connection():
        database.fechar_connection()
    database.estabelecer_coneccao(nome_do_db)
    if (verifica_db_v2("Empresas_table") +
        verifica_db_v2("Contatos_table") +
        verifica_db_v2("Clientes_table") +
        verifica_db_v2("Propostas_table")) != 4:
            database.fechar_connection()
            #parte 1: desabilitar tela 3 e 4 enquanto uma conexão com o banco da dados não for efetuada 
            b1["state"] = DISABLED
            b2["state"] = DISABLED
            b3["state"] = DISABLED
            guardar_botao["state"] = DISABLED
            b1["bg"] = "red"
            b2["bg"] = "red"
            b3["bg"] = "red"
            guardar_botao["bg"] = "red"
            return 0
    #depois de estar ok com o banco de dados
    nome_do_db_entry.delete(0, END)
    nome_do_db_entry.insert(0, nome_do_db)
    habilita_botoes_tela1()
    resetar_lista_empresas()
    resetar_frame4_tela3_linha1()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela4_linha3()
def salvar_nome_db():
    nome_do_db_atual = nome_do_db_entry.get().strip()
    nome_do_db_conectado = database.db_nome
    if nome_do_db_atual != nome_do_db_conectado:
        nome_do_db_entry.delete(0, END)
        nome_do_db_entry.insert(0, nome_do_db_conectado)
    guardar_botao["state"] = DISABLED
    guardar_botao["bg"] = "red"
    with open("nome_do_db.txt", "w") as file:
         file.write(nome_do_db_conectado)
def abre_db_guardado():
    if not os.path.exists("nome_do_db.txt"):
        #cria o arquivo
        file = open("nome_do_db.txt", "w")
        file.close()
    with open("nome_do_db.txt", "r") as file:
        nome_do_db = file.read()
    #verifica se o que está no txt é uma frase (mais de uma palavra)
    if not verifica_nome_db(nome_do_db):
            return
    nome_do_db_entry.delete(0, END)
    nome_do_db_entry.insert(0, nome_do_db)
    conecta_ao_db(abre_db_salvo=1)
    guardar_botao["state"] = DISABLED
    guardar_botao["bg"] = "red"
def habilita_botoes_tela1():
    b1["state"] = NORMAL
    b2["state"] = NORMAL
    b3["state"] = NORMAL
    guardar_botao["state"] = NORMAL
    b1["bg"] = "green"
    b2["bg"] = "green"
    b3["bg"] = "green"
    guardar_botao["bg"] = "#203864"
    nome_do_db_button["bg"] = "#203864"
def verifica_nome_db(nome_do_db: str):
    #se o nome_do_db for absoluto, fazer:
    nome_do_db_iter = nome_do_db.split("/")
    nome_do_db = nome_do_db_iter[-1]
    if ".db" in nome_do_db and len(nome_do_db) > 3 and len(nome_do_db.split(" ")) == 1:
        return True
        #nome_do_db.split(" ") verifica se o nome do db é uma frase (mais de uma palavra)
    else:
        return False

def verifica_db(table: str) -> bool:
    #ou o db não existe, ou ele existe e está vazio, ou ele existe e está preenchido
    """
    se não existe (basta criar) ou está vazio(tudo ok), o db está aprovado.
    se ele existe mas está incorreto, será recusado

    usar> cur.execute('PRAGMA table_info(main)') 
    """
    return database.verifica_db(table)

def verifica_db_v2(table: str) -> bool:
    return database.verifica_db_v2(table)

tela1 = Frame(root, bg="black")
tela1.rowconfigure(0, weight=2, uniform="a")
tela1.rowconfigure((1,2,3,4), weight=1, uniform="a")
tela1.columnconfigure(0, weight=1, uniform="a")
img = PhotoImage(file='logotipo_up.png')
font_tela1 = ("Arial", 25 )
Label(tela1, image=img, background="#203864").grid(row=0, column=0, sticky="nsew") #width=1280, height=219
b1 = Button(tela1, text="Cadastrar",font=font_tela1, fg="white", width=50, command=show_tela3)
b1.grid(row=1, column=0, sticky="s")
b2 = Button(tela1, text="Propostas", font=font_tela1, fg="white", command=show_tela4, width=50)
b2.grid(row=2, column=0, sticky="ns")
b3 = Button(tela1, text="Backup", font=font_tela1, fg="white", command=backup, width=50)
b3.grid(row=3, column=0, sticky="n")
frame_generico_unico = Frame(tela1, width=50)
frame_generico_unico.grid(row=4, column=0, sticky="n")
nome_do_db_button = Button(frame_generico_unico, text="Conectar ao db", font=font_tela1, bg="green", fg="white", width=13, command=conecta_ao_db)
nome_do_db_button.pack(side=LEFT, fill=Y)
nome_do_db_entry = Entry(frame_generico_unico, font=font_tela1, bg="white", fg="black", width=25)
nome_do_db_entry.pack(side=LEFT, fill=Y)
nome_do_db_entry.bind('<Return>', lambda event: conecta_ao_db(abre_db_enter=1))
guardar_botao = Button(frame_generico_unico, text="Guardar",font=font_tela1, fg="white", width=12, command=salvar_nome_db)
guardar_botao.pack(side=LEFT, fill=Y)
#parte 1: desabilitar tela 3 e 4 enquanto uma conexão com o banco da dados não for efetuada 
b1["state"] = DISABLED
b2["state"] = DISABLED
b3["state"] = DISABLED
guardar_botao["state"] = DISABLED
b1["bg"] = "red"
b2["bg"] = "red"
b3["bg"] = "red"
guardar_botao["bg"] = "red"
#parte 2: desabilitar botão guardar quando clicado e após realizar seu comando. OBS, ele será habilidado quando nome_do_db_button for clicado
    #está no comando do botão guardar
#parte 3: ao iniciar o programa, se existir um banco de dados salvo, abrir uma conecção com ele
    #abre_db_guardado() no final do código, após show_tela1

###tela3############################################################################################################################################
def resetar_lista_empresas():
    tela3.frame2_lista.delete(0, END)
def resetar_frame4_tela3_linha1():
    tela3.frame4_empresa_entry.delete(0, END)
    tela3.frame4_cnpj_cbx.delete(0, END)
    #resetar
    tela3.cnpj_id = '\0'
    tela3.nome_id = '\0'
    tela3.frame4_cnpj_cbx["values"] = ()
def resetar_frame4_tela3_linha2():
    tela3.frame4_rua_entry.delete(0, END)
    tela3.frame4_bairro_entry.delete(0, END)
    tela3.frame4_numero_entry.delete(0, END)
    tela3.frame4_cidade_entry.delete(0, END)
    tela3.frame4_estado_entry.delete(0, END)
    tela3.frame3_lista.delete(0, END) #lista de contatos
    #correçao bug: falha minha
    cnpj_entry.delete(0, END)
def resetar_frame4_tela4_linha3():
    tela3.frame4_nome_entry.delete(0, END)
    tela3.frame4_telefone_entry.delete(0, END)
    tela3.frame4_email_entry.delete(0, END)
def preencher_lista_empresas():
    #empresas == [('Jundiai',)], ou seja, lista contendo tuplas
    empresas = database.selecionar_todas_empresa()
    #prevenção
    if len(empresas) == 0:
        return #não existem empresas cadastradas
    #preencher lista de empresas
    tela3.frame2_lista.delete(0, END)
    for empresa in empresas:
        tela3.frame2_lista.insert(END, empresa[0])
def preencher_empresa_cnpjs(event):
    #retorna uma tuple com o(s) elemento(s) selecionados. No meu caso sempre será de comprimento 1
    if len(tela3.frame2_lista.curselection()) == 0:
         return #correção ou gambiarra por causa de bug
    resetar_frame4_tela3_linha1()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela4_linha3()
    #retorna o index (linha) do item selecionado atualmente
    index = tela3.frame2_lista.curselection()[0]
    #retorna a string na linha indicada pelo index
    empresa = tela3.frame2_lista.get(index)
    #preencher empresa label
    tela3.frame4_empresa_entry.insert(0, empresa)
    #retorna uma lista de tuplas cujo elemento de cada é um cnpjs
    cnpjs = database.obter_cnpj_empresa_selecionada(empresa)
    #TODO 1052
    tela3.frame4_cnpj_cbx["values"] = [cnpj[0] for cnpj in cnpjs]
    cnpj = cnpjs[0][0]
    tela3.frame4_cnpj_cbx.set(cnpj)
    #TODO 1052
    #guardar caso o usuário queira atualizar
    tela3.cnpj_id = cnpj
    tela3.nome_id = '\0'
    #caso exclusivo (frescura)
    preencher_endereco_e_lista_clientes(cnpj)
def preencher_endereco(event):
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela4_linha3()
    #retorna o cnpj selecionado
    cnpj = tela3.frame4_cnpj_cbx.get()
    #guardar caso o usuário queira atualizar
    tela3.cnpj_id = cnpj
    tela3.nome_id = '\0'
    preencher_endereco_e_lista_clientes(cnpj)
def preencher_endereco_e_lista_clientes(cnpj):
    #retorna um tupla cujos itens são, nesse ordem, rua, bairro, numero, cidade, estado e cep
    #obs, lista de clientes na GUI é lista de contatos
    endereco = database.obter_endereco_cnpj_selecionado(cnpj)
    #preencher endereço
    tela3.frame4_rua_entry.insert(0, endereco[0])
    tela3.frame4_bairro_entry.insert(0, endereco[1])
    tela3.frame4_numero_entry.insert(0, endereco[2])
    tela3.frame4_cidade_entry.insert(0, endereco[3])
    tela3.frame4_estado_entry.insert(0, endereco[4])
    #correção de bug #TODO 1053
    if endereco[5] != None:
        cnpj_entry.insert(0, endereco[5])
    #retorna um array com os nomes dos contatos do cnpj enviado
    nomes = database.obter_contatos_cnpj_selecionado(cnpj)
    preencher_lista_contatos(nomes)
def preencher_lista_contatos(nomes):
    #preencher lista de contatos
    for nome in nomes:
        tela3.frame3_lista.insert(END, nome)
def formatar(event, pattern):
        if not pattern: return
        texto = tela3.frame4_cnpj_cbx.get()
        last_index = len(texto) - 1
        if len(texto) > 18:
            tela3.frame4_cnpj_cbx.delete(first=last_index, last=END)
            return
        if pattern[last_index] == 'X':
            return
        else:
            tela3.frame4_cnpj_cbx.insert(index=last_index, string = pattern[last_index])
def desformatar(pattern, separators):
    text = []
    for c in pattern:
        if c not in separators:
            text.append(c)
    return "".join(text)
def preencher_contato(event):
    #retorna uma tuple com o(s) elemento(s) selecionados. No meu caso sempre será de comprimento 1
    if len(tela3.frame3_lista.curselection()) == 0:
        return
    resetar_frame4_tela4_linha3()
    index = tela3.frame3_lista.curselection()[0]
    #retorna a string na linha passada (index)
    nome = tela3.frame3_lista.get(index)
    #retorna uma tupla de dois elementos, cujo primemiro é telefone, o segundo, email
    telefone_email = database.obter_telefone_email(nome)
    #preenchimento
    tela3.nome_id = nome
    tela3.frame4_nome_entry.insert(0, nome)
    tela3.frame4_telefone_entry.insert(0, telefone_email[0]) #TODO 1054
    tela3.frame4_email_entry.insert(0, telefone_email[1])
def pegar_dados_empresa():
    cnpj = tela3.frame4_cnpj_cbx.get()
    dados_empresa = (
                    tela3.frame4_empresa_entry.get(),
                    tela3.frame4_cnpj_cbx.get(),
                    tela3.frame4_rua_entry.get(),
                    tela3.frame4_bairro_entry.get(),
                    tela3.frame4_numero_entry.get(),
                    tela3.frame4_cidade_entry.get(),
                    tela3.frame4_estado_entry.get(),
                    cnpj_entry.get()
                    )
    if "" in dados_empresa:
        showerror("Erro ao inserir um cliente", "Esqueceu de preencher algum item da empresa")
        return
    nome = tela3.frame4_nome_entry.get()
    dados_contato = (
                    tela3.frame4_nome_entry.get(),
                    tela3.frame4_telefone_entry.get(),
                    tela3.frame4_email_entry.get()
                    )
    database.novo_cliente(dados_empresa, cnpj, dados_contato, nome)
    #Uma vez inserido o novo cliente, é hora de atualizar a lista de empresas e restar a tela3 inteira
    resetar_frame4_tela3_linha1()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela4_linha3()
    preencher_lista_empresas()
def pegar_dados_contato():
    cnpj = tela3.frame4_cnpj_cbx.get().strip()
    #verificar se existe a empresa
    if database.verificar_cliente_existe(cnpj) == False:
        showerror("Erro ao inserir contato", f"A empresa com o cnpj {cnpj} ainda não foi inserida.\nPor favor considere inserí-la primeiro")
        return
    #fim
    if cnpj == "":
        showerror("Erro ao inserir contato", "Você esqueceu de selecionar um cnpj")
        return
    nome = tela3.frame4_nome_entry.get()
    dados_contato = (
                    nome,
                    tela3.frame4_telefone_entry.get(),
                    tela3.frame4_email_entry.get()
                    )
    if "" in dados_contato:
        showerror("Erro ao inserir contato", "Esqueceu algum item do contato")
        return
    database.novo_contato(dados_contato, cnpj)
    #atualiza lista
    tela3.frame3_lista.insert(END, nome)
    tela3.nome_id = '\0'
    resetar_frame4_tela4_linha3()
def atualizar_dados_empresa():
    cnpj = tela3.cnpj_id
    if cnpj == '\0':
        showinfo("Aviso", "Não há o que atualizar")
        return
    dados_empresa = (
                    tela3.frame4_empresa_entry.get(),
                    tela3.frame4_cnpj_cbx.get(),
                    tela3.frame4_rua_entry.get(),
                    tela3.frame4_bairro_entry.get(),
                    tela3.frame4_numero_entry.get(),
                    tela3.frame4_cidade_entry.get(),
                    tela3.frame4_estado_entry.get(),
                    cnpj_entry.get(),
                    cnpj
                    )
    if "" in dados_empresa:
        showerror("Erro ao atualizar empresa", "Esqueceu de preecher algum item da empresa")
        return
    database.atualiza_empresa(dados_empresa)
    resetar_frame4_tela4_linha3()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela3_linha1()
    print(f"{cnpj} virou {tela3.frame4_cnpj_cbx.get()}")
    #...
def atualizar_dados_contato():
    nome = tela3.nome_id
    dados_contato = (
                    tela3.frame4_nome_entry.get(),
                    tela3.frame4_telefone_entry.get(),
                    tela3.frame4_email_entry.get(),
                    nome
                    )
    if "" in dados_contato:
        showerror("Erro ao atualizar contato", "Esqueceu de preencher algum item do contato")
        return
    database.atualiza_contato(dados_contato)
    resetar_frame4_tela4_linha3()
def deletar_cliente():
    cnpj = tela3.frame4_cnpj_cbx.get()
    if cnpj.strip() == '':
        showerror("Erro ao deletar empresa", "Você esqueceu de selecionar uma empresa cadastrada")
        return
    # retorna a empresa para eu poder apagá-la da lista
    empresa = database.deleta_cliente(cnpj)
    # retora uma tupla com todas as empresas listadas na listbox
    empresas = tela3.frame2_lista.get(0, END)
    index = empresas.index(empresa)
    tela3.frame2_lista.delete(index)
    resetar_frame4_tela3_linha1()
    resetar_frame4_tela3_linha2()
    resetar_frame4_tela4_linha3()
    tela3.cnpj_id = ""
    tela3.nome_id = ""
def deletar_contato():
    nome = tela3.frame4_nome_entry.get()
    if nome.strip() == '':
        showerror("Erro ao deletar um contato", "você esqueceu de selecionar um nome cadastrado")
        return
    database.deleta_contato(nome)
    # retora uma tupla com todas as empresas listadas na listbox
    nomes = tela3.frame3_lista.get(0, END)
    index = nomes.index(nome)
    tela3.frame3_lista.delete(index)
    resetar_frame4_tela4_linha3()
    tela3.nome_id = ""   
tela3 = Tela(root)
#falha minha
cnpj_lbl = Label(tela3.frame4, text="CEP", font="Arial 15 bold", relief="raised", borderwidth=5, width=10)
cnpj_lbl.place(x=11, y=190, width=140)

#TODO 1053
cnpj_entry = Entry(tela3.frame4, font="Arial 15", justify="center")
cnpj_entry.place(x=170, y=190, width=300, height=cnpj_entry.winfo_reqheight()+7)
#fim da falha
Button(tela3, text="voltar", font=("Times New Roman", 13), command=show_tela1).grid(row=0, column=0, columnspan=2, sticky="w")
#       parte 1: vou enviar para show_tela3
# preencher_lista_empresas()
tela3.frame2_lista.bind('<<ListboxSelect>>', preencher_empresa_cnpjs, add='+')
#       parte 2: preencher endereço e cnpj
tela3.frame4_cnpj_cbx.bind('<<ComboboxSelected>>', preencher_endereco, add='+')
#       entre partes: formatar texto para notação de cnpj
tela3.frame4_cnpj_cbx.bind("<KeyRelease>", lambda event: formatar(event, "XX.XXX.XXX/XXXX-XX"))
#       parte 3: preencher contato
tela3.frame3_lista.bind('<<ListboxSelect>>', preencher_contato)
#       parte 4: botão novo
tela3.cliente_novo.configure(command=pegar_dados_empresa)
tela3.contato_novo.configure(command=pegar_dados_contato)
#       parte 5: botão atualizar
tela3.cliente_atualizar.configure(command=atualizar_dados_empresa)
tela3.contato_atualizar.configure(command=atualizar_dados_contato)
#       parte 6: botão excluir ...
tela3.cliente_deletar.configure(command=deletar_cliente)
tela3.contato_deletar.configure(command=deletar_contato)

###tela4############################################################################################################################################
# operational system
def criar_proposta_os(nome_do_arq, extensao, caminho):
    nome_do_arq_completo = os.path.join(caminho, nome_do_arq+extensao)
    print(extensao)
    print(f"blankFile\\blankFile{extensao}")
    print(os.listdir("blankFile"))
    try:
        shutil.copy(f"blankFile\\blankFile{extensao}", nome_do_arq_completo)
    except FileNotFoundError:
        if not os.path.exists("blankFile"):
            os.mkdir("blankFile")
        caminho_desse_scrip_python = os.path.abspath(__file__)
        dir_desse_script_python = os.path.dirname(caminho_desse_scrip_python)
        caminho_blankfile = os.path.join(dir_desse_script_python, "blankFile")
        showerror("Erro de criação", f"Por favor insira um arquivo chamado blankFile{extensao} em\n{caminho_blankfile}\n")
    return
def atualizar_nome_proposta_os(nome_do_arq_completo_antigo, nome_do_arq_completo_novo):
    try:
        os.rename(nome_do_arq_completo_antigo, nome_do_arq_completo_novo)
    except FileExistsError: #arquivo source não existe
        pass
    except FileNotFoundError: #já existe um arquivo com o nome que você deseja colocar
        showerror("Erro ao atualizar dados da proposta", "Proposta sumiu.")

# not operational system
def identificar_nome_do_arquivo(arquivo: str) -> bool:
    if len(arquivo) != 18:
        return False
    if arquivo[0:4] == "PROP":
        try: 
            int(arquivo[5:9]) == int
            if arquivo[9] == "-":
                try: 
                    int(arquivo[10:12])
                    if arquivo[13:16] == "rev":
                        return True
                    else: return False 
                except ValueError: return False
            else: return False
        except ValueError: return False
    else: return False
def formatar_numero_proposta(numero_proposta: str):
    digitos_numero = len(numero_proposta)
    numero_zeros = 4 - digitos_numero
    if numero_zeros < 0:
        return
    numero_proposta = numero_zeros*"0" + numero_proposta
    if numero_zeros == 4:
        numero_proposta = 3*"0" + numero_proposta
    return numero_proposta
def criar_nome_do_arquivo(ano, numero, revisao):
    return f"PROP {numero}-{ano[2:]} rev {revisao}"
def preenche_empresa_cnpj():
    empresas_cnpjs = database.obter_empresas_cnpjs()
    arr = []
    for empresa_cnpj in empresas_cnpjs:
        # [Jundiai/74839230-1]
        arr += [f"{empresa_cnpj[0]} / {empresa_cnpj[1]}"]
    return tuple(arr)
def preencher_treeview_c_propostas(ano = "2019"):
    dict_propostas = database.obter_todas_propostas()
    #deletar todo o conteúdo
    for proposta_iid in tela4.propostas_treeview.get_children():
        tela4.propostas_treeview.delete(proposta_iid)
    #verificar se existe alguma proposta para esse ano
    if ano not in dict_propostas.keys():
        return
    #preencher conteúdo do ano especificado
    for proposta in dict_propostas[ano]:
        tela4.propostas_treeview.insert(parent="", index=END, values=proposta)
def carregar_proposta():
    #arquivo já existe
    dados = []
    diretorio_escolhido = askdirectory(parent=tela4, initialdir="/", title="Selecione uma pasta")
    
    diretorio_escolhido = diretorio_escolhido.replace("/", "\\")
    if not diretorio_escolhido:
        return
    if os.path.split(diretorio_escolhido)[1] not in [str(ano) for ano in range(2019, 2030)]:
        showerror("ERRO!", "O nome da pasta deve ser um ano\ndentro do intervalo 2019 à 2030 incluindo os dois")
        return
    for arquivo in os.listdir(diretorio_escolhido):
        if os.path.isdir(arquivo):
            continue
        if identificar_nome_do_arquivo(os.path.splitext(arquivo)[0]):
            # ano = os.path.split(diretorio_escolhido)[1]
            ano = "20"+os.path.splitext(arquivo)[0][10:12]
            numero = os.path.splitext(arquivo)[0][5:9]
            revisao = os.path.splitext(arquivo)[0][17]
            extensao = os.path.splitext(arquivo)[1]
            caminho = diretorio_escolhido
            nome_completo = os.path.join(diretorio_escolhido, arquivo)
            dados.append((ano, numero, revisao, extensao, caminho, nome_completo))
    database.inserir_multiplas_propostas(dados)
    preencher_treeview_c_propostas()
    return
def inserir_proposta(): 
    #diferente de carregar propostas, aqui o arquivo não existe
    ano = tela4.ano_spinbox_dir.get().strip()
    if ano == "ANO": ano = ""
    numero = tela4.numero_entry.get().strip()
    if numero == "NÚMERO": numero = ""
    empresacnpj = tela4.empresacnpj_combobox.get().strip()
    if empresacnpj == "EMPRESA/CNPJ": empresacnpj = ""
    revisao = tela4.revisao_entry.get().strip()
    if revisao == "REVISÃO": revisao = ""
    extensao = tela4.extensao_combobox.get().strip()
    if extensao == "EXTENSÃO": extensao = ""
    descricao = tela4.descricao_text.get("1.0", END).strip()
    if descricao == "DESCRIÇÃO": descricao = ""
    caminho = tela4.caminho_entry.get().strip()
    if caminho == "CAMINHO": caminho = ""

    if any( tmp == "" or tmp == "None" for tmp in [ano, numero, empresacnpj, revisao, extensao, descricao, caminho]):
        showerror("Erro no preenchimento", "Você esqueceu de preencher um ou mais campos.\nPor favor, preencha-os.")
        return
    if extensao[0] != ".":
        showerror("Erro na extensão do arquivo", "Você esqueceu de adicionar um . no início da extensão.\nPor favor, insira o ponto")
        return

    nome_do_arquivo = criar_nome_do_arquivo(ano, formatar_numero_proposta(numero), revisao)
    nome_completo = os.path.join(caminho, nome_do_arquivo+extensao) #único

    #verificar arquivo repetido
    proposta_iid = tela4.propostas_treeview.focus()
    if proposta_iid != '':
        nome_completo_proposta_selecionada = tela4.propostas_treeview.set(proposta_iid, column="nome_do_arq")
        if nome_completo == nome_completo_proposta_selecionada:
            return #a proposta já existe

    #inserir proposta no banco de dados
    dados = (ano, formatar_numero_proposta(numero), empresacnpj, revisao, extensao, descricao, caminho, nome_completo)
    database.inserir_proposta(dados)

    #criação do arquivo
    criar_proposta_os(criar_nome_do_arquivo(ano, formatar_numero_proposta(numero), revisao), extensao, caminho)
            # print(criar_nome_do_arquivo(ano, formatar_numero_proposta(numero), revisao))

    #atualiza a treeview de propostas
    tela4.propostas_treeview.insert(parent="", index=END, values=dados)
    
    #limpar entradas do usuário para notificar mudanças feitas com sucesso
    mudanca_feita_c_sucesso(f"A proposta {nome_do_arquivo+extensao} foi criada!")
    return
def selecionar_proposta(event):
    proposta_selecionada = tela4.propostas_treeview.focus() #iid
    if proposta_selecionada == '':
        return
    conteudo_proposta = tela4.propostas_treeview.item(proposta_selecionada, option="values")
    #preencher parte direita
    tela4.ano_spinbox_dir.config(state="normal")
    tela4.ano_spinbox_dir.delete(0, END)
    tela4.ano_spinbox_dir.insert(0, conteudo_proposta[0])
    tela4.ano_spinbox_dir.config(state="readonly")
    tela4.numero_entry.delete(0, END)
    tela4.numero_entry.insert(0, conteudo_proposta[1])
    tela4.empresacnpj_combobox.set(conteudo_proposta[2])
    tela4.revisao_entry.delete(0, END)
    tela4.revisao_entry.insert(0, conteudo_proposta[3])
    tela4.extensao_combobox.delete(0, END)
    tela4.extensao_combobox.insert(0, conteudo_proposta[4])
    tela4.descricao_text.delete("1.0", END)
    tela4.descricao_text.insert("1.0", conteudo_proposta[5])
    tela4.caminho_entry.delete(0, END)
    tela4.caminho_entry.insert(0, conteudo_proposta[6])
def resetar_tela4_lado_direito():
    tela4.resetar_lado_direito()
    #ano
    tela4.ano_spinbox_esq.config(state="normal")
    tela4.ano_spinbox_esq.delete(0, END)
    tela4.ano_spinbox_esq.insert(0, "2019")
    tela4.ano_spinbox_esq.config(state="readonly")
def atualizar_proposta():
    #verificar se alguma proposta foi selecionada
    proposta_iid = tela4.propostas_treeview.focus()
    if proposta_iid == '':
        showerror("Erro de atualização", "Para modificar uma proposta\nvocê deve selecionar alguma proposta.")
        return
    #verificar se todos os campos estão preenchidos
    ano = tela4.ano_spinbox_dir.get().strip()
    if ano == "ANO": ano = ""
    numero = tela4.numero_entry.get().strip()
    if numero == "NÚMERO": numero = ""
    empresacnpj = tela4.empresacnpj_combobox.get().strip()
    if empresacnpj == "EMPRESA/CNPJ": empresacnpj = ""
    revisao = tela4.revisao_entry.get().strip()
    if revisao == "REVISÃO": revisao = ""
    extensao = tela4.extensao_combobox.get().strip()
    if extensao == "EXTENSÃO": extensao = ""
    descricao = tela4.descricao_text.get("1.0", END).strip()
    if descricao == "DESCRIÇÃO": descricao = ""
    caminho = tela4.caminho_entry.get().strip()
    if caminho == "CAMINHO": caminho = ""

    if any( tmp == "" or tmp == "None" for tmp in [ano, numero, empresacnpj, revisao, extensao, descricao, caminho]):
        showerror("Erro de preenchimento", "Você esqueceu de preencher um ou mais campos.\nPor favor, preencha-os.")
        return
    if extensao[0] != ".":
        showerror("Erro na extensão do arquivo", "Você esqueceu de adicionar um . no início da extensão.\nPor favor, insira o ponto")
        return
    #obter caminho_completo_proposta_selecionada
    proposta_selecionada = tela4.propostas_treeview.item(proposta_iid, option="values")[-1]
    #Verificar mudança de ano.
    ano_antigo = tela4.propostas_treeview.item(proposta_iid, option="values")[0]
    if ano_antigo != ano:
        showerror("Erro ao atualizar dados da proposta", "Se for mudar ano, use o comando ""SALVAR COMO")
        return
    #Verificar mudança da path
    caminho_antigo = tela4.propostas_treeview.set(proposta_iid, column="caminho")
    if caminho_antigo != caminho:
        showerror("Erro ao atualizar dados da proposta", "Se for mudar o caminho, use o comando ""SALVAR COMO")
        return
    #atualizar dados
    dados = [ano, numero, empresacnpj, revisao, extensao, descricao, caminho]
    nome_arq = criar_nome_do_arquivo(ano, numero, revisao)
    nome_arq_completo = os.path.join(caminho, nome_arq + extensao)
    dados.append(nome_arq_completo)
    #atualizar banco de dados
    database.atualizar_proposta(dados, proposta_selecionada)
    #atualizar nome do arquivo (os)
    atualizar_nome_proposta_os(proposta_selecionada, dados[-1])
    #atualizar treeview
    tela4.propostas_treeview.item(proposta_iid, values=dados)
    #limpar entradas do usuário para notificar mudanças feitas com sucesso
    mudanca_feita_c_sucesso(f"Nova atualização feita: {nome_arq + extensao}")
    return
def deletar_proposta():
    #verificar se alguma proposta foi selecionada
    proposta_iid = tela4.propostas_treeview.focus()
    if proposta_iid == '':
        showerror("Erro ao deletar", "Para apagar uma proposta (DO BANCO DE DADOS)\nvocê deve selecionar alguma proposta.")
        return
    #obter caminho completo da proposta
    caminho_completo_proposta = tela4.propostas_treeview.set(proposta_iid, column="nome_do_arq")
    #deletar da treeview
    tela4.propostas_treeview.delete(proposta_iid)
    #deletar do banco de dados
    database.deletar_proposta(caminho_completo_proposta)
    #perguntar se vai deletar o arquivo (enviar para lixeira)
    anwser = askyesno(tela4, f"Você deseja enviar para lixeira o arquivo:\n{os.path.split(caminho_completo_proposta)[1]}")
    if anwser == True:
        try:
            os.remove(caminho_completo_proposta)
        except OSError:
            showerror("Erro ao deletar", "A proposta selecionada é um arquivo")
    #limpar entradas do usuário para notificar mudanças feitas com sucesso
    nome_arq = os.path.split(caminho_completo_proposta)[1]
    mudanca_feita_c_sucesso(f"A proposta {nome_arq} foi deletada!")
    return
def salvar_como_proposta():
    #verificar se alguma proposta foi selecionada
    proposta_iid = tela4.propostas_treeview.focus()
    if proposta_iid == '':
        showerror("Erro ao salvar como", "Para salvar como\nSelecione uma proposta")
        return
    #verificar se tudo foi preenchido
    ano = tela4.ano_spinbox_dir.get().strip()
    if ano == "ANO": ano = ""
    numero = tela4.numero_entry.get().strip()
    if numero == "NÚMERO": numero = ""
    empresacnpj = tela4.empresacnpj_combobox.get().strip()
    if empresacnpj == "EMPRESA/CNPJ": empresacnpj = ""
    revisao = tela4.revisao_entry.get().strip()
    if revisao == "REVISÃO": revisao = ""
    extensao = tela4.extensao_combobox.get().strip()
    if extensao == "EXTENSÃO": extensao = ""
    descricao = tela4.descricao_text.get("1.0", END).strip()
    if descricao == "DESCRIÇÃO": descricao = ""
    caminho = tela4.caminho_entry.get().strip()
    if caminho == "CAMINHO": caminho = ""

    if any( tmp == "" or tmp == "None" for tmp in [ano, numero, empresacnpj, revisao, extensao, descricao, caminho]):
        showerror("Erro no preenchimento", "Você esqueceu de preencher um ou mais campos.\nPor favor, preencha-os.")
        return
    #obter caminho completo da proposta selecionada
    caminho_completo_proposta_selecionada = tela4.propostas_treeview.set(proposta_iid, column="nome_do_arq")
    extensao_proposta_selecionada = tela4.propostas_treeview.set(proposta_iid, column="extensao")
    
    #Dar a opção do usuário selecionar onde quer copiar
    anwser = askyesno(tela4, f"Você deseja escolher um outro caminho para copiar?\nO destino atual é {caminho}")
    if anwser == True:
        diretorio_escolhido = askdirectory(parent=tela4, initialdir="/", title="Selecione uma pasta")
        caminho = diretorio_escolhido.replace("/", "\\")
        if os.path.split(caminho)[1] not in [str(ano) for ano in range(2019, 2030)]:
            showerror("ERRO!", "O nome da pasta deve ser um ano\ndentro do intervalo 2019 à 2030 (incluindo os dois)")
            return
    #Criar o nome completo da proposta
    nome_do_arquivo = criar_nome_do_arquivo(ano, formatar_numero_proposta(numero), revisao)
    caminho_completo = os.path.join(caminho, nome_do_arquivo+extensao_proposta_selecionada) #único
    #Verificar se a proposta selecionada é igual à outra
    if caminho_completo == caminho_completo_proposta_selecionada:
        return
    #Criar arquivo
    shutil.copyfile(caminho_completo_proposta_selecionada, caminho_completo)
    #inserir arquivo novo no banco de dados
    dados = (ano, formatar_numero_proposta(numero), empresacnpj, revisao, extensao, descricao, caminho, caminho_completo)
    database.inserir_proposta(dados)
    #atualizar treeview
    ano_proposta_selecionada = tela4.propostas_treeview.set(proposta_iid, column="ano")
    if ano == ano_proposta_selecionada:
        tela4.propostas_treeview.insert(parent='', index=END, values=dados)
    #limpar entradas do usuário para notificar mudanças feitas com sucesso
    mudanca_feita_c_sucesso(f"Uma cópia foi criada com sucesso!")
    return
def obter_proposta_outro_ano():
    ano = tela4.ano_spinbox_esq.get().strip()
    preencher_treeview_c_propostas(ano)
def abrir_proposta(event):
    x_coor = event.x
    y_coor = event.y
    region = tela4.propostas_treeview.identify_region(x_coor, y_coor)
    # print(f"x_coor: {x_coor}| y_coor: {y_coor}| region: {region}")
    if region != 'cell':
        return
    proposta_iid = tela4.propostas_treeview.focus()
    caminho_completo = tela4.propostas_treeview.set(proposta_iid, column="nome_do_arq")
    #abrir proposta
    if os.path.exists(caminho_completo):
        os.system(f'start "" "{caminho_completo}"')
    else:
        showerror("Erro ao abrir proposta", f"A proposta encontrada em\n{caminho_completo}\nnão existe")
def show_notification(parent, text, duration):
    # Obtendo as dimensões da janela principal
    parent.update_idletasks()
    parent_width = parent.winfo_width()
    parent_x = parent.winfo_x()
    
    # Definindo posição centralizada no eixo X e no topo
    notif_width = 400
    x = parent_x + (parent_width // 2) - (notif_width // 2)
    y = parent.winfo_y() + 10
    
    # Criando o frame da notificação
    notification = Toplevel(parent)
    notification.overrideredirect(True)  # Remove a barra de título
    notification.geometry(f"{notif_width}x80+{x}+{y}")
    notification.config(bg="#333")
    
    # Criando o container interno com cantos arredondados
    container = Frame(notification, bg="#444", bd=2, relief="ridge")
    container.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Label de texto
    label = Label(container, text=text, fg="white", bg="#444", font=("Arial", 10))
    label.pack(pady=(10, 5), padx=10)
    
    # Botão de fechar
    close_btn = Button(container, text="X", fg="white", bg="#a00", border=0,
                          font=("Arial", 10, "bold"), command=notification.destroy)
    close_btn.place(relx=1.0, rely=0.0, anchor="ne")
    
    # Barra de progresso
    progress = ttk.Progressbar(container, length=200, mode='determinate')
    progress.pack(pady=(0, 5), padx=10, fill="x")
    
    # Parte da animação da progressbar
    interval = int(duration/100)
    amount = 1.0 #linear
    # progress.start(interval=interval)

    def controla_tempo():
        id = notification.after(interval, controla_tempo)
        progress.step(amount=amount)
        if int(progress['value']) == 99:
            notification.after_cancel(id)
            notification.destroy()
    
    controla_tempo()
def mudanca_feita_c_sucesso(mensagem="Ação realizada com sucesso!"):
    resetar_tela4_lado_direito()
    show_notification(root, mensagem, 2000)
tela4 = Tela5(root)
tela4.ano_spinbox_esq.configure(command=obter_proposta_outro_ano)
tela4.voltar_button.configure(command=show_tela1)
tela4.carregar_button.configure(command=carregar_proposta)
tela4.inserir_button.configure(command=inserir_proposta)
tela4.atualizar_button.configure(command=atualizar_proposta)
tela4.deletar_button.configure(command=deletar_proposta)
tela4.saveas_button.configure(command=salvar_como_proposta)
tela4.propostas_treeview.bind("<<TreeviewSelect>>", selecionar_proposta)
tela4.propostas_treeview.bind("<Double-Button-1>", abrir_proposta)
###loop_janela############################################################################################################################################
show_tela1()
abre_db_guardado()
root.mainloop()
#Criar método para estilização

import tkinter as tk
from tkinter.constants import *
from tkinter import ttk
from custom_widgets import Entry_undo_redo
#Frame da tela 3
class Tela(tk.Frame):
    def __init__(self, master,**kargs) -> None:
        self.font = "Arial 15"
        super().__init__(master, **kargs)
        #configurando frame 1
        self.rowconfigure((0,1,2), weight=10, uniform='a')
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1), weight=1, uniform='a')
        self.columnconfigure(1, weight=7, uniform='a')
        #criando frame 2
        self.frame2 = tk.Frame(self)
        #criando frame 3
        self.frame3 = tk.Frame(self)
        #criando frame 4
        self.frame4 = tk.Frame(self, background="#565857")
        #configurando frame 4
        self.frame4.rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.frame4.columnconfigure((0,1,2,3,4,5,6), weight=1, uniform='a') 
        #layout dos frames
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame3.grid(row=2, column=0, sticky="nsew")
        self.frame4.grid(row=1, rowspan=2, column=1, sticky="nsew") 
        #adicionar widgets
        self.frame2_titulo = tk.Label(self.frame2, text="Clientes", font="Arial 12 bold", background="#565857", foreground="white")
        self.frame2_yscrollbar = tk.Scrollbar(self.frame2, orient="vertical")
        self.frame2_lista = tk.Listbox(self.frame2, font="Arial 13", selectmode=SINGLE, yscrollcommand=self.frame2_yscrollbar.set)
        self.frame2_yscrollbar['command'] = self.frame2_lista.yview

        self.frame3_titulo = tk.Label(self.frame3, text="Contatos", font="Arial 12 bold", background="#565857", foreground="white")
        self.frame3_yscrollbar = tk.Scrollbar(self.frame3, orient="vertical")
        self.frame3_lista = tk.Listbox(self.frame3, font="Arial 13", yscrollcommand=self.frame3_yscrollbar.set)
        self.frame3_yscrollbar['command'] = self.frame3_lista.yview

        self.frame4_empresa_lbl = tk.Label(self.frame4, text="Empresa", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_empresa_entry = Entry_undo_redo(self.frame4, font=self.font, justify="center")
        # self.frame4_empresa_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_cnpj_lbl = tk.Label(self.frame4, text="CNPJ", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_cnpj_cbx = ttk.Combobox(self.frame4, font=self.font, justify="center")

        self.frame4_rua_lbl = tk.Label(self.frame4, text="Rua", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_rua_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_bairro_lbl = tk.Label(self.frame4, text="Bairro", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_bairro_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_numero_lbl = tk.Label(self.frame4, text="Número", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_numero_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_cidade_lbl = tk.Label(self.frame4, text="Cidade", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_cidade_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_estado_lbl = tk.Label(self.frame4, text="Estado", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_estado_entry = tk.Entry(self.frame4, font=self.font, justify="center")

        self.frame4_nome_lbl = tk.Label(self.frame4, text="Nome", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_nome_entry = tk.Entry(self.frame4, font=self.font)

        self.frame4_telefone_lbl = tk.Label(self.frame4, text="Telefone", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_telefone_entry = tk.Entry(self.frame4, font=self.font)    

        self.frame4_email_lbl = tk.Label(self.frame4, text="Email", font="Arial 15 bold", relief="raised", borderwidth=5)
        self.frame4_email_entry = tk.Entry(self.frame4, font=self.font)

        # self.img_tela3 = tk.PhotoImage(file="img_tela3.png")
        # self.frame4_img = tk.Label(self.frame4, image=self.img_tela3,background="#565857")

        self.cliente_novo = tk.Button(self.frame4, text="Nova Empresa", font=self.font)
        self.cliente_atualizar = tk.Button(self.frame4, text="Atualizar Empresa", font=self.font)
        self.cliente_deletar = tk.Button(self.frame4, text="Deletar Empresa", font=self.font)

        self.contato_novo = tk.Button(self.frame4, text="Novo Contato", font=self.font)
        self.contato_atualizar = tk.Button(self.frame4, text="Atualizar Contato", font=self.font)
        self.contato_deletar = tk.Button(self.frame4, text="Deletar Contato", font=self.font)
        # valores_unicos:
        self.cnpj_id = "\0"
        self.nome_id = "\0"
        self.layout_frames()
    def layout_frames(self):
        self.frame2_titulo.pack(fill=X)
        self.frame2_yscrollbar.pack(fill=Y, side="left")
        self.frame2_lista.pack(fill=BOTH, expand=1)
        
        self.frame3_titulo.pack(fill=X)
        self.frame3_yscrollbar.pack(fill=Y, side="left")
        self.frame3_lista.pack(fill=BOTH, expand=1)

        self.frame4_empresa_lbl.grid(row=0, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_empresa_entry.grid(row=0, column=1, columnspan=2, sticky="nswe", padx=10, pady=35)

        self.frame4_cnpj_lbl.grid(row=0, column=3, sticky="nswe", padx=10, pady=35)
        self.frame4_cnpj_cbx.grid(row=0, column=4, columnspan=2,sticky="nswe", padx=10, pady=35)

        self.frame4_rua_lbl.grid(row=1, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_rua_entry.grid(row=1, column=1, columnspan=2, sticky="nswe", padx=10, pady=35)

        self.frame4_bairro_lbl.grid(row=1, column=3, sticky="nswe", padx=10, pady=35)
        self.frame4_bairro_entry.grid(row=1, column=4, columnspan=2, sticky="nswe", padx=10, pady=35)

        self.frame4_numero_lbl.grid(row=2, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_numero_entry.grid(row=2, column=1, sticky="nswe", padx=10, pady=35)

        self.frame4_cidade_lbl.grid(row=2, column=2, sticky="nswe", padx=10, pady=35)
        self.frame4_cidade_entry.grid(row=2, column=3, sticky="nswe", padx=10, pady=35)

        self.frame4_estado_lbl.grid(row=2, column=4, sticky="nswe", padx=10, pady=35)
        self.frame4_estado_entry.grid(row=2, column=5, sticky="nswe", padx=10, pady=35)

        self.frame4_nome_lbl.grid(row=3, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_nome_entry.grid(row=3, column=1, columnspan=4 ,sticky="nswe", padx=10, pady=35)

        self.frame4_telefone_lbl.grid(row=4, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_telefone_entry.grid(row=4, column=1, columnspan=3, sticky="nswe", padx=10, pady=35)

        self.frame4_email_lbl.grid(row=5, column=0, sticky="nswe", padx=10, pady=35)
        self.frame4_email_entry.grid(row=5, column=1, columnspan=2, sticky="nswe", padx=10, pady=35)
        
        self.cliente_novo.grid(row=0, column=6, sticky="swe")
        self.cliente_atualizar.grid(row=1, column=6, sticky="nswe")
        self.cliente_deletar.grid(row=2, column=6, sticky="nwe")

        self.contato_novo.grid(row=3, column=6, sticky="swe")
        self.contato_atualizar.grid(row=4, column=6, sticky="nswe")
        self.contato_deletar.grid(row=5, column=6, sticky="nwe")


    

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

class Tela5(tk.Frame):
    def __init__(self, master, **kargs):
        super().__init__(master)
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.rowconfigure(2, weight=3, uniform='a')
        self.font = ("Arial", "20")
        # self.treeview_content = {} #key é o parent (ano) e value são os values (dados)
        self.widgets_exibição()
        self.widgets_acao("#E97132", "white")
        self.widgets_layout()
        # self.testar_yscroll()
    def widgets_exibição(self):
        #Parte esquerda
        self.ano_spinbox_esq = tk.Spinbox(self, from_=2019, to=2025, font=self.font, state='readonly', justify="center",  wrap=True)
        self.propostas_treeview = ttk.Treeview(self, columns=("ano", "numero", "empresacnpj", "revisao", "extensao", "descricao", "caminho", "nome_do_arq"), displaycolumns=(0,1,3,4), selectmode="browse", show="headings") #
        self.propostas_treeview.heading("ano", text="Ano")
        self.propostas_treeview.heading("numero", text="Número")
        self.propostas_treeview.heading("revisao", text="Revisão")
        self.propostas_treeview.heading("extensao", text="Extensão")
        self.propostas_treeview.heading("nome_do_arq", text="Arquivo")
        self.propostas_treeview.column("ano", width=100)
        self.propostas_treeview.column("numero", width=100)
        self.propostas_treeview.column("revisao", width=75)
        self.propostas_treeview.column("extensao", width=150)
        self.propostas_treeview.column("nome_do_arq", width=200)
        # self.propostas_treeview.tag_configure("exp_arq_font", option=None, font=self.font)
        style_exp_arq = ttk.Style()
        style_exp_arq.configure("Treeview", rowheight=30, font=("Arial", 15))
        self.y_scrollbar = tk.Scrollbar(self, orient="vertical", command = self.propostas_treeview.yview)
        self.propostas_treeview.configure(yscrollcommand=self.y_scrollbar.set)
        # style_exp_arq.configure("Treeview.Heading", font=self.font)
        
        #Parte direita
        self.ano_spinbox_dir = tk.Spinbox(self, from_=2019, to=2025, font=self.font, justify="center",  wrap=True)
        self.ano_spinbox_dir.insert(0, "ANO")
        self.ano_spinbox_dir.delete(3, END)
        self.ano_spinbox_dir.configure(state='readonly')
        # self.ano_spinbox_dir.bind("<FocusIn>", self.selecionar_tudo)
        self.numero_entry = custom_entry(self, "NÚMERO", font=self.font, justify="center")
        self.numero_entry.limite_caracteres(4, "NÚMERO")
        self.empresacnpj_combobox = ttk.Combobox(self, font=self.font, justify="center")
        self.empresacnpj_combobox.set("EMPRESA/CNPJ")
        self.empresacnpj_combobox.state(('!disabled', 'readonly'))
        self.revisao_entry = custom_entry(self, "REVISÃO", font=self.font, width=10, justify="center", validate='key')
        controle_revisoesWRAP = self.revisao_entry.register(self.controlar_revisoes)
        self.revisao_entry["validatecommand"] = (controle_revisoesWRAP, '%S', '%d', '%s')
        self.extensao_combobox = ttk.Combobox(self, font=self.font, width=8, justify="center", values=(".txt", ".pdf", ".docx", ".xlsx"), validate='key')
        self.extensao_combobox.set(".xlsx")
        self.extensao_combobox.bind("<FocusIn>", self.selecionar_tudo)
        limitar_char = self.extensao_combobox.register(self.limitar_char_combobox)
        self.extensao_combobox.configure(validatecommand=(limitar_char, '%d'))
        self.descricao_text = tk.Text(self, font=self.font, width=40, height=9)
        self.descricao_text.insert('1.0', "DESCRIÇÃO")
        self.descricao_text.bind("<FocusIn>", self.evento_text, add='+')
        self.descricao_text.bind("<FocusOut>", self.evento_text, add="+")
        self.descricao_text.bind("<KeyPress>", self.limitar_char_Text)
        self.caminho_entry = custom_entry(self, "CAMINHO", font=self.font, justify="center")
    def widgets_acao(self, background, foreground):
        self.voltar_button = tk.Button(self, text="Voltar", font=self.font, bg=background, fg=foreground)
        self.carregar_button = tk.Button(self, text="Carregar", font=self.font, bg=background, fg=foreground)
        self.inserir_button = tk.Button(self, text="Inserir", font=self.font, bg=background, fg=foreground)
        self.atualizar_button = tk.Button(self, text="Atualizar", font=self.font, bg=background, fg=foreground)
        self.deletar_button = tk.Button(self, text="Deletar", font=self.font, bg=background, fg=foreground)
        self.saveas_button = tk.Button(self, text="Salvar como", font=self.font, bg=background, fg=foreground)
    def widgets_layout(self):
        #Parte esquerda
        self.ano_spinbox_esq.grid(column=1, row=0, padx=5, pady=5, sticky="nsw")
        self.propostas_treeview.grid(column=0, columnspan=2, row=1, rowspan=3, padx=5, pady=5, sticky="nswe")
        self.y_scrollbar.grid(column=1, row=1, rowspan=3, sticky="nse", padx=5, pady=5)
        self.voltar_button.grid(column=0, row=0, padx=5, pady=5, sticky="nsw")
        self.carregar_button.grid(column=0, row=0, padx=5, pady=5, sticky="nse")

        #Parte direita
        
        self.ano_spinbox_dir.grid(column=2, row=0, padx=5, pady=5, sticky="nswe")
        self.numero_entry.grid(column=3, row=0, padx=5, pady=5, sticky="nswe")
        self.empresacnpj_combobox.grid(column=2, row=1, padx=5, pady=5, sticky="nswe")
        self.revisao_entry.grid(column=3, row=1, padx=5, pady=5, sticky="wns")
        self.extensao_combobox.grid(column=3, row=1, padx=5, pady=5, sticky="ens")
        self.descricao_text.grid(column=2, columnspan=2, row=2, padx=5, pady=5, sticky="nswe")
        self.caminho_entry.grid(column=0, columnspan=4, row=4, padx=5, sticky="nswe")
        self.inserir_button.grid(column=2, row=3, padx=5, pady=5, sticky="nse")
        self.saveas_button.grid(column=2, row=3, padx=5, pady=5, sticky="nsw")
        self.atualizar_button.grid(column=3, row=3, pady=5, sticky="nsw")
        self.deletar_button.grid(column=3, row=3, padx=5, pady=5, sticky="nse")
    def testar_yscroll(self):
        for i in range(101):
            self.propostas_treeview.insert(parent="", values=(str(i),),index=END)
    def selecionar_tudo(self, event):
        widget = event.widget #tkspinbox ou ttkcombobox
        if widget.winfo_class() == "TCombobox":
            widget.select_range(0, END)
        elif widget.winfo_class() == "Spinbox":
            widget.selection('range', 0, END)
    def evento_text(self, event):
        text = event.widget
        null = text.get("1.0", END).strip()
        type_ = int(event.type)
        if type_ == 9: #FocusIn
            if null == "DESCRIÇÃO":
                text.delete("1.0", END)
        elif type_ == 10: #FocusOut
            if null == "":
                text.insert('1.0', "DESCRIÇÃO")
    def controlar_revisoes(self, key_input, validate, key_input_before):
        #É um código de ação: 0,1,-1 do tipo <class 'str>
        if validate == "1" and key_input != "REVISÃO": #1 significa inserção de letras
            if key_input_before != "":
                return False
            # print(key_input)
        return True
    def limitar_char_combobox(self, porque):
        texto = self.extensao_combobox.get()
        if len(texto) > 6 and porque == '1':
            return False
        return True
    def limitar_char_Text(self, event):
        Text = event.widget
        tecla_pressed = event.keysym
        if len(Text.get("1.0", "end-1c").strip()) > 250:
            Text.configure(state = DISABLED)
            if tecla_pressed == "BackSpace":
                Text.configure(state = NORMAL)
        else:
            Text.configure(state = NORMAL)
    def resetar_lado_direito(self):
        #ano
        self.ano_spinbox_dir.config(state="normal")
        self.ano_spinbox_dir.delete(0, END)
        self.ano_spinbox_dir.insert(0, "ANO")
        self.ano_spinbox_dir.config(state="readonly")
        #numero
        self.numero_entry.delete(0, END)
        self.numero_entry.insert(0, "NÚMERO")
        #empresa/cnpj
        self.empresacnpj_combobox.set("EMPRESA/CNPJ")
        #revisao
        self.revisao_entry.delete(0, END)
        self.revisao_entry.insert(0, "REVISÃO")
        #extensao
        self.extensao_combobox.set(".xlsx")
        #descricao
        self.descricao_text.delete("1.0", END)
        self.descricao_text.insert("1.0", "DESCRIÇÃO")
        #caminho
        self.caminho_entry.delete(0, END)
        self.caminho_entry.insert(0, "CAMINHO")

class custom_entry(tk.Entry):
    def __init__(self, master, texto_padrao, **kargs):
        super().__init__(master, **kargs)
        self.texto = texto_padrao
        self.insert(0, self.texto)
        self.bind("<FocusIn>", self.resetar_label, add="+")
        self.bind("<FocusOut>", self.preencher_label)
    def resetar_label(self, event):
        if self.get() == self.texto:
            self.delete(0, END)
            return
        self.select_range(0, END)
    def preencher_label(self, event):
        if self.get() == "":
            self.insert(0, self.texto) 
    def limite_caracteres(self, limite, placeholder):
        self.limite = limite
        self.placeholder = placeholder
        limitar = self.register(self.tmp_limite_caracteres)
        self.configure(validate='key', validatecommand = (limitar, '%S', '%d'))
    def tmp_limite_caracteres(self, caracter, porque):
        texto = self.get()
        if caracter == self.placeholder:
            return True
        if not (texto == self.placeholder):
            if len(texto) > self.limite-1 and porque == '1':
                return False
            try:
                int(caracter)
            except:
                return False
            return True
        return True

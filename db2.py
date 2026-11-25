import sqlite3

class DB:
    def __init__(self) -> None:
        self.caminho_head = ""
    def estabelecer_coneccao(self, db_nome_2):
        #guardar nome
        self.db_nome = db_nome_2
        # estabelecer conexão
        self.connection = sqlite3.connect(db_nome_2)
        #criar cursor
        self.cursor = self.connection.cursor()
        #criar tabela(s)
        self.criar_tabela()
    
    def verifica_db(self, table: str) -> bool:
        match table:
            case "Empresas_table":
                 tabela_escolhida = "Select * from Empresas_table"
                 columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                            "empresa": "TEXT",
                            "CNPJ": "TEXT UNIQUE",
                            "rua": "TEXT",
                            "bairro": "TEXT",
                            "numero": "TEXT",
                            "cidade": "TEXT",
                            "estado": "TEXT",
                            "cep": "TEXT"}
            case "Contatos_table":
                 tabela_escolhida = "Select * from Contatos_table"
                 columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                            "nome": "TEXT UNIQUE",
                            "telefone": "TEXT UNIQUE",
                            "email":"TEXT UNIQUE"}
            case "Clientes_table":
                 tabela_escolhida = "Select * from Clientes_table"
                 columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                            "Empresas_id": "INTEGER",
                            "Contatos_id": "INTEGER"}
            case "Propostas_table":
                 tabela_escolhida = "Select * from Propostas_table"
                 columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                        "ano": "TEXT",
                        "numero": "TEXT",
                        "empresacnpj": "TEXT",
                        "revisao": "TEXT",
                        "extensao": "TEXT",
                        "descricao": "TEXT",
                        "caminho": "TEXT",
                        "nome_do_arq_completo": "TEXT UNIQUE"}
            case _:
                return 0
        data = self.cursor.execute(tabela_escolhida)
        print(data.description)
        for column in data.description:
            if column[0] not in columns.keys():
                return 0 #banco de dados inválido
        return 1 #banco de dados parcialmente válido
    
    def verifica_db_v2(self, table: str) -> bool:
        match table:
            case "Empresas_table":
                 tabela_escolhida = "PRAGMA table_info(Empresas_table)"
                 columns = [(0, 'id', 'INTEGER', 0, None, 1),
                            (1, 'empresa', 'TEXT', 0, None, 0),
                            (2, 'CNPJ', 'TEXT', 0, None, 0),
                            (3, 'rua', 'TEXT', 0, None, 0),
                            (4, 'bairro', 'TEXT', 0, None, 0),
                            (5, 'numero', 'TEXT', 0, None, 0),
                            (6, 'cidade', 'TEXT', 0, None, 0),
                            (7, 'estado', 'TEXT', 0, None, 0), 
                            (8, 'cep', 'TEXT', 0, None, 0)]
            case "Contatos_table":
                 tabela_escolhida = "PRAGMA table_info(Contatos_table)"
                 columns = [(0, 'id', 'INTEGER', 0, None, 1),
                            (1, 'nome', 'TEXT', 0, None, 0),
                            (2, 'telefone', 'TEXT', 0, None, 0),
                            (3, 'email', 'TEXT', 0, None, 0)]
            case "Clientes_table":
                 tabela_escolhida = "PRAGMA table_info(Clientes_table)"
                 columns = [(0, 'id', 'INTEGER', 0, None, 1),
                            (1, 'Empresas_id', 'INTEGER', 0, None, 0),
                            (2, 'Contatos_id', 'INTEGER', 0, None, 0)]
            case "Propostas_table":
                 tabela_escolhida = "PRAGMA table_info(Propostas_table)"
                 columns = [(0, 'id', 'INTEGER', 0, None, 1),
                            (1, 'ano', 'TEXT', 0, None, 0),
                            (2, 'numero', 'TEXT', 0, None, 0),
                            (3, 'empresacnpj', 'TEXT', 0, None, 0),
                            (4, 'revisao', 'TEXT', 0, None, 0),
                            (5, 'extensao', 'TEXT', 0, None, 0),
                            (6, 'descricao', 'TEXT', 0, None, 0),
                            (7, 'caminho', 'TEXT', 0, None, 0),
                            (8, 'nome_do_arq_completo', 'TEXT', 0, None, 0)]
            case _:
                return 0
        column_dados = self.cursor.execute(tabela_escolhida).fetchall()
        #verificar se a qtd de colunas está de acordo
        if len(columns) != len(column_dados):
            return 0
        for i in range(len(column_dados)):
            #verificar se a coluna 0 é Primary Key (PK)
            if i == 0:
                if column_dados[0][5] != 1:
                    return 0
            #verificar se o nome da coluna e o tipo de dado estão de acordo
                #index 1 -> nome da coluna, index 2 -> tipo de dado
            if column_dados[i][1] != columns[i][1] or column_dados[i][2] != columns[i][2]:
                return 0
        return 1 #banco de dados válido

    def retorna_connection(self):
        try:
            self.connection
        except AttributeError:
            return False
    def criar_tabela(self):
        self.cursor.executescript("""
                        CREATE TABLE IF NOT EXISTS Empresas_table(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         empresa TEXT,
                         CNPJ TEXT UNIQUE,
                         rua TEXT,
                         bairro TEXT,
                         numero TEXT,
                         cidade TEXT,
                         estado TEXT,
                         cep TEXT
                        );
                        CREATE TABLE IF NOT EXISTS Contatos_table(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE,
                        telefone TEXT UNIQUE,
                        email TEXT UNIQUE
                        );
                        CREATE TABLE IF NOT EXISTS Clientes_table(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Empresas_id INTEGER,
                        Contatos_id INTEGER,
                        FOREIGN KEY (Empresas_id) REFERENCES Empresas_table(id),
                        FOREIGN KEY (Contatos_id) REFERENCES Contatos_table(id)
                        );
                        CREATE TABLE IF NOT EXISTS Propostas_table(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ano TEXT,
                        numero TEXT,
                        empresacnpj TEXT,
                        revisao TEXT,
                        extensao TEXT,
                        descricao TEXT,
                        caminho TEXT,
                        nome_do_arq_completo TEXT UNIQUE,
                        FOREIGN KEY (empresacnpj) REFERENCES Empresas_table(id)
                        );
                        """)
        self.connection.commit()
    def fechar_connection(self):
        self.cursor.close()
        self.connection.close()   
    def selecionar_todas_empresa(self):
        empresa = self.cursor.execute("SELECT DISTINCT empresa FROM Empresas_table ORDER BY empresa").fetchall()
        return empresa
    def obter_cnpj_empresa_selecionada(self, empresa):
        cnpjs = self.cursor.execute("SELECT cnpj FROM Empresas_table WHERE empresa = ?", (empresa,)).fetchall()
        return cnpjs
    def obter_endereco_cnpj_selecionado(self, cnpj):
        endereco = self.cursor.execute("SELECT rua, bairro, numero, cidade, estado, cep FROM Empresas_table WHERE cnpj = ?", (cnpj,)).fetchone()
        return endereco
    def obter_contatos_cnpj_selecionado(self, cnpj):
        #retorna um array de tuplas de comprimento único cujo conteúdo é o id de um contato especificado pelo cnpj
        id_contatos = self.cursor.execute("SELECT Contatos_id FROM Clientes_table WHERE Empresas_id = (SELECT id FROM Empresas_table WHERE cnpj = ?)", (cnpj,)).fetchall()
        temporario = ['?' for _ in id_contatos]
        #string do tipo (?,...,?) 
        place_holders = ",".join(temporario)
        #retorna um lista de tuplas de tamanho 1, cada qual com seu o nome do respectivo id passado
        nomes = self.cursor.execute(f"SELECT nome FROM Contatos_table WHERE id IN ({place_holders})", tuple([id_contato[0] for id_contato in id_contatos])).fetchall()
        return [nome[0] for nome in nomes]
    def obter_telefone_email(self, nome):
        telefone_email = self.cursor.execute("SELECT telefone, email FROM Contatos_table WHERE nome = ?", (nome,)).fetchone()
        return telefone_email
    def novo_cliente(self, dados_empresa: list, cnpj, dados_contato, nome):
        self.cursor.execute("INSERT OR IGNORE INTO Empresas_table(empresa, cnpj, rua, bairro, numero, cidade, estado, cep) VALUES (?,?,?,?,?,?,?,?)", dados_empresa)
        self.connection.commit()
        self.cursor.execute("INSERT OR IGNORE INTO Contatos_table(nome, telefone, email) VALUES (?,?,?)", dados_contato)
        self.connection.commit()
        cnpj_id = self.cursor.execute("SELECT id FROM Empresas_table WHERE cnpj = ?", (cnpj,)).fetchone()[0]
        nome_id = self.cursor.execute("SELECT id FROM Contatos_table WHERE nome = ?", (nome,)).fetchone()[0]
        self.cursor.execute("INSERT OR IGNORE INTO Clientes_table(Empresas_id, Contatos_id) VALUES (?,?)", (cnpj_id, nome_id))
        self.connection.commit()
    def verificar_cliente_existe(self, cnpj) -> bool:
        cnpj_id = self.cursor.execute("SELECT id FROM Empresas_table WHERE cnpj = ?", (cnpj,)).fetchone()
        print(f"cnpj_id: {cnpj_id}")
        if cnpj_id == None:
            return False
        return True
    def novo_contato(self, dados_contato:list, cnpj):
        #pegar id da empresa
        cnpj_id = self.cursor.execute("SELECT id FROM Empresas_table WHERE cnpj = ?", (cnpj,)).fetchone()[0]
        #registrar novo contato
        self.cursor.execute("INSERT OR IGNORE INTO Contatos_table(nome, telefone, email) VALUES (?,?,?)", dados_contato)
        self.connection.commit()
        #pegar id do contato
        nome_id = self.cursor.execute("SELECT id FROM Contatos_table WHERE nome = ?", (dados_contato[0],)).fetchone()[0]
        #registrar novo cliente
        print(f"nome_id: {nome_id}, cnpj_id: {cnpj_id}")
        self.cursor.execute("INSERT OR IGNORE INTO Clientes_table(Empresas_id, Contatos_id) VALUES (?,?)", (cnpj_id, nome_id))
        self.connection.commit()
    def atualiza_empresa(self, dados_empresa:list):
        self.cursor.execute("UPDATE Empresas_table SET empresa = ? , cnpj = ? , rua = ? , bairro = ? , numero = ? , cidade = ? , estado = ? , cep = ? WHERE cnpj = ?", dados_empresa)
        self.connection.commit()
    def atualiza_contato(self, dados_contato:list):
        self.cursor.execute("UPDATE Contatos_table SET nome = ? , telefone = ? , email = ? WHERE nome = ?", dados_contato)
        self.connection.commit()
    def deleta_cliente(self, cnpj):
        #deletar contatos
        #retorna um array de tuplas de comprimento único cujo conteúdo é o id de um contato especificado pelo cnpj
        id_contatos = self.cursor.execute("SELECT Contatos_id FROM Clientes_table WHERE Empresas_id = (SELECT id FROM Empresas_table WHERE cnpj = ?)", (cnpj,)).fetchall()
        #array do tipo (?,...,?)
        temporario = ['?' for _ in id_contatos] 
        place_holders = ",".join(temporario)
        #retorna um lista de tuplas de tamanho 1, cada qual com seu o nome do respectivo id passado
        self.cursor.execute(f"DELETE FROM Contatos_table WHERE id IN ({place_holders})", tuple([id_contato[0] for id_contato in id_contatos]))
        self.connection.commit()
        #deletar cliente
        self.cursor.execute("DELETE FROM Clientes_table WHERE Empresas_id = (SELECT id FROM Empresas_table WHERE cnpj = ?)", (cnpj,))
        self.connection.commit()
        #deletar a empresa
        empresa = self.cursor.execute("SELECT empresa FROM Empresas_table WHERE cnpj = ?", (cnpj,)).fetchone()[0]
        self.cursor.execute("DELETE FROM Empresas_table WHERE cnpj = ?", (cnpj,))
        self.connection.commit()
        #
        return empresa
    def deleta_contato(self, nome):
        #desvincula a empresa ao contato
        self.cursor.execute("DELETE FROM Clientes_table WHERE Contatos_id = (SELECT id FROM Contatos_table WHERE nome = ?)", (nome,))
        self.connection.commit()
        #deleta o contato
        self.cursor.execute("DELETE FROM Contatos_table WHERE nome = ?", (nome,))
        self.connection.commit()
    def obter_empresas_cnpjs(self):
        empresas_cnpjs = self.cursor.execute("SELECT empresa,cnpj FROM Empresas_table").fetchall()
        return empresas_cnpjs
    def obter_todas_propostas(self):
        dict_propostas = {}
        anos = self.cursor.execute("SELECT DISTINCT ano from Propostas_table ORDER BY ano").fetchall()
        for ano in anos:
            propostas_por_ano = self.cursor.execute("SELECT ano, numero, empresacnpj, revisao, extensao, descricao, caminho, nome_do_arq_completo FROM Propostas_table WHERE ano = ? ORDER BY ano, numero, revisao", (ano[0],)).fetchall()
            dict_propostas[ano[0]] = propostas_por_ano 
        return dict_propostas
        # propostas = self.cursor.execute("SELECT ano, numero, empresacnpj, revisao, extensao, descricao, caminho FROM Propostas_table ORDER BY ano, numero, revisao").fetchall()
        # return propostas
    def inserir_multiplas_propostas(self, propostas):
        for proposta in propostas:
            self.cursor.execute("INSERT OR IGNORE INTO Propostas_table(ano, numero, revisao, extensao, caminho, nome_do_arq_completo) values (?,?,?,?,?,?)", proposta)
            self.connection.commit()
        return
    def inserir_proposta(self, dados):
        self.cursor.execute("INSERT OR IGNORE INTO Propostas_table(ano, numero, empresacnpj, revisao, extensao, descricao, caminho, nome_do_arq_completo) values (?,?,?,?,?,?,?,?)", dados)
        self.connection.commit()
        return
    def atualizar_proposta(self, dado, proposta_selecionada):
        self.cursor.execute(
            "UPDATE Propostas_table SET ano = ?, numero = ?, empresacnpj = ?, revisao = ?, extensao = ?, descricao = ?, caminho = ?, nome_do_arq_completo = ? WHERE nome_do_arq_completo = ?", (*dado, proposta_selecionada)
            )
        self.connection.commit()
    def deletar_proposta(self, proposta_selecionada):
        self.cursor.execute(
            "DELETE FROM Propostas_table WHERE nome_do_arq_completo = ?", (proposta_selecionada,)
        )
        self.connection.commit()

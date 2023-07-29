import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, filedialog
from PIL import Image
import random, datetime, os, qrcode
import pandas as pd
import sys, subprocess
import shutil

class TelaCadastro:
    def __init__(self, main_window):
        self.main_window = main_window
        self.janela = tk.Toplevel(self.main_window.janela)
        self.janela.title("Cadastro de aluno")
        self.janela.geometry("1300x600")
        self.centralizar_janela(self.janela)
        self.label_nome = tk.Label(self.janela, text="Nome:")
        self.label_nome.pack()
        self.entry_nome = tk.Entry(self.janela)
        self.entry_nome.pack()
        self.label_serie = tk.Label(self.janela, text="Série:")
        self.label_serie.pack()
        self.combo_serie = ttk.Combobox(self.janela, values=[
            "1º A - Biotecnologia",
            "1º A - Agropecuária",
            "1º A - Alimentos",
            "2º A - Alimentos",
            "2º A - Biotecnologia",
            "2º B - Biotecnologia",
            "3º A - Biotecnologia",
            "3º B - Biotecnologia",
            "3º C - Biotecnologia"
        ])
        self.combo_serie.pack()
        self.label_matricula = tk.Label(self.janela, text="Matrícula:")
        self.label_matricula.pack()
        self.entry_matricula = tk.Entry(self.janela)
        self.entry_matricula.pack()
        self.button_cadastrar = tk.Button(
            self.janela,
            text="Cadastrar",
            command=self.cadastrar_aluno,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_cadastrar.pack(padx=10, pady=10)
        self.button_cadastrar_planilha = tk.Button(
            self.janela,
            text="Cadastrar por Planilha",
            command=self.cadastrar_alunos_planilha,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_cadastrar_planilha.pack(padx=10, pady=10)
        self.button_voltar = tk.Button(
            self.janela,
            text="Voltar",
            command=self.voltar_para_menu,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_voltar.pack(padx=10, pady=10)

    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def mostrar(self):
        self.main_window.janela.withdraw()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_para_menu)
        self.centralizar_janela(self.janela)
        self.janela.mainloop()

    def voltar_para_menu(self):
        self.janela.destroy()
        self.main_window.janela.deiconify()

    def cadastrar_aluno(self):
        nome = self.entry_nome.get()
        serie = self.combo_serie.get()
        matricula = self.entry_matricula.get()
        self.main_window.cadastrar_aluno(nome, serie, matricula)
        self.entry_nome.delete(0, tk.END)
        self.combo_serie.set("")
        self.entry_matricula.delete(0, tk.END)

    def cadastrar_alunos_planilha(self):
        arquivo = filedialog.askopenfilename(
            filetypes=(("Planilhas", "*.xlsx;*.xls"), ("Todos os arquivos", "*.*"))
        )
        if arquivo:
            try:
                df = pd.read_excel(arquivo)
                quantidade_alunos = len(df)
                if quantidade_alunos > 0:
                    for _, row in df.iterrows():
                        nome = row['Nome']
                        serie = row['Série']
                        matricula = row['Matrícula']
                        self.main_window.cadastrar_aluno(nome, serie, matricula)

                    messagebox.showinfo("Cadastro de Alunos", f"Todos os {quantidade_alunos} aluno(s) foram cadastrados com sucesso!")
                else:
                    messagebox.showwarning("Cadastro de Alunos", "Nenhum aluno encontrado na planilha.")
            except Exception as e:
                messagebox.showerror("Cadastro de Alunos", f"Erro ao ler planilha: {str(e)}")
        else:
            messagebox.showwarning("Cadastro de Alunos", "Nenhum arquivo selecionado.")


class CadastroAluno:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Ifatech")
        self.janela.geometry("1300x600")
        self.centralizar_janela(self.janela)
        self.frame_cadastro = tk.Frame(self.janela)
        self.frame_cadastro.pack()
        self.button_buscar = tk.Button(
            self.frame_cadastro,
            text="Buscar aluno",
            command=self.exibir_janela_busca,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_buscar.pack(pady=10)
        self.button_cadastro = tk.Button(
            self.frame_cadastro,
            text="Cadastro de alunos",
            command=self.exibir_tela_cadastro,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_cadastro.pack(pady=10)
        self.button_verificar_qr_code = tk.Button(
            self.frame_cadastro,
            text="Verificar QR code",
            command=self.exibir_janela_verificar_qr_code,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_verificar_qr_code.pack(pady=10)
        self.exibir_mensagem = True  # Variável de controle para exibir a mensagem a cada cadastro
        self.treeview = None
        self.janela.mainloop()

    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def exibir_tela_cadastro(self):
        self.janela.withdraw()
        tela_cadastro = TelaCadastro(self)
        tela_cadastro.mostrar()

    def voltar_para_menu(self):
        self.janela.deiconify()

    def cadastrar_aluno(self, nome, serie, matricula):
        if nome and serie and matricula:
            aluno = {"nome": nome, "serie": serie, "matricula": matricula}

            codigo = self.gerar_codigo_aleatorio()
            self.salvar_aluno(aluno, codigo)
            self.gerar_qr_code_e_salvar(aluno, codigo)

            messagebox.showinfo("Cadastro de alunos", "Aluno cadastrado com sucesso!")

        else:
            messagebox.showwarning("Cadastro de alunos", "Por favor, preencha todos os campos!")

    def exibir_janela_busca(self):
        nome_busca = simpledialog.askstring("Buscar aluno", "Digite o nome do aluno:")
        if nome_busca:
            alunos_encontrados = self.buscar_aluno_por_nome(nome_busca)
            if alunos_encontrados:
                self.exibir_janela_opcoes(alunos_encontrados)
            else:
                messagebox.showinfo("Buscar aluno", "Nenhum aluno encontrado.")
        else:
            messagebox.showwarning("Buscar aluno", "Por favor, digite um nome para busca.")

    def exibir_janela_verificar_qr_code(self):
        while True:
            codigo = simpledialog.askstring("Verificar QR code", "Digite o código do aluno:")
            if codigo:
                self.verificar_qr_code(codigo)
            else:
                messagebox.showwarning("Verificar QR code", "Por favor, digite o código do aluno.")
            resposta = messagebox.askquestion("Verificar QR code", "Deseja verificar outro código?")
            if resposta == "no":
                break

    def exibir_janela_opcoes(self, alunos):
        self.janela_opcoes = JanelaOpcoes(self.janela, self, alunos)
        self.janela.withdraw()

    def visualizar_aluno(self):
        selected_item = self.janela_opcoes.treeview.focus()
        if selected_item:
            item = self.janela_opcoes.treeview.item(selected_item)
            nome_completo = item["values"][0]
            serie_completa = item["values"][1]
            matricula = item["values"][2]
            qr_code = item["values"][3]
            if nome_completo and serie_completa and matricula and qr_code:
                messagebox.showinfo(
                    "Visualizar aluno",
                    f"Nome Completo: {nome_completo}\nSérie: {serie_completa}\nMatrícula: {matricula}\nNúmero de QR Code Gerado: {qr_code}",
                )
            else:
                messagebox.showinfo("Visualizar aluno", "Informações do aluno incompletas")
        else:
            messagebox.showinfo("Visualizar aluno", "Nenhum aluno selecionado")

    def salvar_aluno(self, aluno, codigo):
        data_registro = datetime.date.today().strftime("%Y-%m-%d")
        with open("registros.txt", "a") as arquivo:
            arquivo.write(f"{aluno['nome']},{aluno['serie']},{aluno['matricula']},{codigo},{data_registro}\n")

    def gerar_qr_code_e_salvar(self, aluno, codigo):
        nome_arquivo = f"{codigo}_{aluno['nome']}.png"

        qr_code = qrcode.make(codigo)
        qr_code.save(os.path.join("qr_codes", nome_arquivo))

    def gerar_codigo_aleatorio(self):
        codigo = str(random.randint(10000, 99999))
        return codigo

    def buscar_aluno_por_nome(self, nome):
        alunos_encontrados = []

        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                nome_aluno = dados[0]
                serie_aluno = dados[1]
                matricula_aluno = dados[2]
                qr_code_aluno = dados[3]

                if nome.lower() in nome_aluno.lower():
                    aluno = f"{nome_aluno},{serie_aluno},{matricula_aluno},{qr_code_aluno}"
                    alunos_encontrados.append(aluno)

        return alunos_encontrados

    def verificar_qr_code(self, codigo):
        encontrado = False
        aluno = None
        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                codigo_aluno = dados[3]
                data_registro_aluno = dados[4]

                if codigo == codigo_aluno:
                    encontrado = True
                    if self.verificar_ficha_usada(codigo, data_registro_aluno):
                        messagebox.showerror("Verificar QR code", "Código já verificado hoje.")
                    else:
                        aluno = linha
                    break
        if encontrado:
            data_atual = datetime.date.today().strftime("%Y-%m-%d")
            hora_atual = datetime.datetime.now().strftime("%H:%M:%S")

            if aluno is not None:  # Verifica se aluno não é None
                self.registrar_ficha_usada(aluno, codigo, data_atual, hora_atual)
                messagebox.showinfo("Verificar QR Code", "Aluno apto a receber.")
            elif not self.verificar_ficha_usada(codigo, data_registro_aluno):
                messagebox.showerror("Verificar QR Code", "Erro ao obter informações do aluno.")
        else:
            messagebox.showerror("Verificar QR code", "Código inválido. Por favor, verifique o código digitado.")

    def verificar_ficha_usada(self, codigo):
        data_atual = datetime.date.today().strftime("%Y-%m-%d")

        with open("fichas_usadas.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                codigo_ficha = dados[1]
                data_registro_ficha = dados[2]

                if codigo == codigo_ficha and data_atual == data_registro_ficha:
                    return True

        return False

    def registrar_ficha_usada(self, aluno, codigo, data, hora):
        if aluno is not None:  # Verifica se aluno não é None
            nome_aluno = aluno.split(",")[0].strip()
            with open("fichas_usadas.txt", "a") as arquivo:
                arquivo.write(f"{nome_aluno},{codigo},{data},{hora}\n")
        else:
            messagebox.showerror("Registrar ficha usada", "Erro ao obter informações do aluno.")

class JanelaOpcoes:
    def __init__(self, janela_principal, main_window, alunos):
        self.janela_principal = janela_principal
        self.main_window = main_window
        self.alunos = alunos
        self.janela = tk.Toplevel(self.janela_principal)
        self.janela.title("Opções")
        self.janela.geometry("1300x600")
        self.centralizar_janela(self.janela)
        self.treeview = ttk.Treeview(self.janela)
        self.treeview["columns"] = ("Nome", "Série", "Matrícula", "QR Code")
        self.treeview.heading("#0", text="ID")
        self.treeview.column("#0", minwidth=0, width=50, stretch=tk.NO)
        self.treeview.heading("Nome", text="Nome")
        self.treeview.column("Nome", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("Série", text="Série")
        self.treeview.column("Série", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("Matrícula", text="Matrícula")
        self.treeview.column("Matrícula", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("QR Code", text="QR Code")
        self.treeview.column("QR Code", minwidth=0, width=100, stretch=tk.NO)
        self.scrollbar = ttk.Scrollbar(
            self.janela, orient="vertical", command=self.treeview.yview
        )
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.treeview.pack(side="left", fill="both")
        self.scrollbar.pack(side="right", fill="y")
        self.button_visualizar = tk.Button(
            self.janela,
            text="Visualizar",
            command=self.visualizar_aluno,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_visualizar.pack(pady=10)
        self.button_mostrar_pasta_qr_code = tk.Button(
            self.janela,
            text="Mostrar Pasta e QR Code",
            command=self.mostrar_pasta_qr_code,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_mostrar_pasta_qr_code.pack(pady=10)
        self.button_voltar = tk.Button(
            self.janela,
            text="Voltar",
            command=self.voltar_para_menu,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_voltar.pack(pady=10)
        self.preencher_treeview()
    
    def mostrar_pasta_qr_code(self):
        selected_item = self.treeview.focus()
        if selected_item:
            item = self.treeview.item(selected_item)
            values = item["values"]
            if len(values) > 3:
                qr_code_path = values[3]
                if qr_code_path:
                    aluno_path = os.path.dirname(str(qr_code_path))
                    pasta_qr_codes = os.path.join(aluno_path, "qr_codes")

                    if os.path.exists(pasta_qr_codes):
                        if sys.platform == "win32":
                            # Para Windows
                            subprocess.Popen(f'explorer "{pasta_qr_codes}"')
                        elif sys.platform == "darwin":
                            # Para macOS
                            subprocess.Popen(["open", pasta_qr_codes])
                        else:
                            # Para Linux ou outros sistemas operacionais
                            subprocess.Popen(["xdg-open", pasta_qr_codes])
                    else:
                        print(f"A pasta {pasta_qr_codes} não existe.")
                else:
                    messagebox.showinfo("Mostrar Pasta e QR Code", "QR Code não encontrado.")
            else:
                messagebox.showinfo("Mostrar Pasta e QR Code", "Informações do aluno incompletas.")
        else:
            messagebox.showinfo("Mostrar Pasta e QR Code", "Nenhum aluno selecionado.")

    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def preencher_treeview(self):
        for index, aluno in enumerate(self.alunos, start=1):
            nome_completo, serie_completa, matricula, qr_code = aluno.split(",")
            self.treeview.insert(
                "",
                "end",
                text=index,
                values=(nome_completo, serie_completa, matricula, qr_code),
            )

    def voltar_para_menu(self):
        self.janela.destroy()
        self.main_window.voltar_para_menu()

    def visualizar_aluno(self):
        selected_item = self.treeview.focus()
        if selected_item:
            item = self.treeview.item(selected_item)
            nome_completo = item["values"][0]
            serie_completa = item["values"][1]
            matricula = item["values"][2]
            qr_code = item["values"][3]
            if nome_completo and serie_completa and matricula and qr_code:
                messagebox.showinfo(
                    "Visualizar aluno",
                    f"Nome Completo: {nome_completo}\nSérie: {serie_completa}\nMatrícula: {matricula}\nNúmero de QR Code Gerado: {qr_code}",
                )
            else:
                messagebox.showinfo("Visualizar aluno", "Informações do aluno incompletas")
        else:
            messagebox.showinfo("Visualizar aluno", "Nenhum aluno selecionado")

class JanelaRegistros:
    def __init__(self, janela_principal, main_window):
        self.janela_principal = janela_principal
        self.main_window = main_window
        self.janela = tk.Toplevel(self.janela_principal)
        self.janela.title("Registros")
        self.janela.geometry("1300x600")
        self.centralizar_janela(self.janela)
        self.treeview = ttk.Treeview(self.janela)
        self.treeview["columns"] = ("Nome", "Série", "Matrícula", "QR Code", "Data Registro")
        self.treeview.heading("#0", text="ID")
        self.treeview.column("#0", minwidth=0, width=50, stretch=tk.NO)
        self.treeview.heading("Nome", text="Nome")
        self.treeview.column("Nome", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("Série", text="Série")
        self.treeview.column("Série", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("Matrícula", text="Matrícula")
        self.treeview.column("Matrícula", minwidth=0, width=200, stretch=tk.NO)
        self.treeview.heading("QR Code", text="QR Code")
        self.treeview.column("QR Code", minwidth=0, width=100, stretch=tk.NO)
        self.treeview.heading("Data Registro", text="Data Registro")
        self.treeview.column("Data Registro", minwidth=0, width=100, stretch=tk.NO)
        self.scrollbar = ttk.Scrollbar(
            self.janela, orient="vertical", command=self.treeview.yview
        )
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.treeview.pack(side="left", fill="both")
        self.scrollbar.pack(side="right", fill="y")
        self.button_excluir = tk.Button(
            self.janela,
            text="Excluir Registro",
            command=self.excluir_registro,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_excluir.pack(side="bottom", pady=10)
        self.button_voltar = tk.Button(
            self.janela,
            text="Voltar",
            command=self.voltar_para_menu,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_voltar.pack(side="bottom", pady=10)
        self.preencher_treeview()

    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def preencher_treeview(self):
        with open("registros.txt", "r") as arquivo:
            for index, linha in enumerate(arquivo, start=1):
                dados = linha.strip().split(",")
                nome = dados[0]
                serie = dados[1]
                matricula = dados[2]
                qr_code = dados[3]
                data_registro = dados[4]
                self.treeview.insert(
                    "",
                    "end",
                    text=index,
                    values=(nome, serie, matricula, qr_code, data_registro),
                )

    def voltar_para_menu(self):
        self.janela.destroy()
        self.main_window.voltar_para_menu()
    def excluir_registro(self):
        selected_item = self.treeview.focus()
        if selected_item:
            item = self.treeview.item(selected_item)
            nome_completo = item["values"][0]
            matricula = item["values"][2]
            qr_code = item["values"][3]
            if nome_completo and matricula and qr_code:
                resposta = messagebox.askyesno(
                    "Excluir Registro",
                    f"Tem certeza de que deseja excluir o registro do aluno {nome_completo}?",
                )
                if resposta:
                    self.remover_registro(nome_completo, matricula, qr_code)
                    messagebox.showinfo("Excluir Registro", "Registro excluído com sucesso!")
                    self.atualizar_treeview()
            else:
                messagebox.showinfo("Excluir Registro", "Informações do aluno incompletas")
        else:
            messagebox.showinfo("Excluir Registro", "Nenhum aluno selecionado")

    def remover_registro(self, nome, matricula, qr_code):
        registros = []
        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                nome_aluno = dados[0]
                matricula_aluno = dados[2]
                qr_code_aluno = dados[3]
                if nome_aluno != nome or str(matricula_aluno) != str(matricula) or str(qr_code_aluno) != str(qr_code):
                    registros.append(linha)

        with open("registros.txt", "w") as arquivo:
            arquivo.writelines(registros)

        # Excluir o arquivo do QR code
        nome_arquivo = f"{qr_code}_{nome}.png"
        caminho_arquivo = os.path.join("qr_codes", nome_arquivo)
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)

        # Excluir o diretório qr_codes se estiver vazio
        pasta_qr_codes = os.path.join(os.getcwd(), "qr_codes")
        if not os.listdir(pasta_qr_codes):
            shutil.rmtree(pasta_qr_codes)

        # Atualizar a exibição na lista
        self.atualizar_treeview()

    def atualizar_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        self.preencher_treeview()
        
class TelaCadastroPlanilha:
    def __init__(self, main_window):
        self.main_window = main_window
        self.janela = tk.Toplevel(self.main_window.janela)
        self.janela.title("Cadastro de Alunos por Planilha")
        self.janela.geometry("1300x600")
        self.centralizar_janela(self.janela)
        self.label_arquivo = tk.Label(self.janela, text="Selecione o arquivo da planilha:")
        self.label_arquivo.pack()
        self.button_selecionar_arquivo = tk.Button(
            self.janela,
            text="Selecionar Arquivo",
            command=self.selecionar_arquivo,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_selecionar_arquivo.pack(pady=10)
        self.button_cadastrar = tk.Button(
            self.janela,
            text="Cadastrar Alunos",
            command=self.cadastrar_alunos,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_cadastrar.pack(pady=10)
        self.button_voltar = tk.Button(
            self.janela,
            text="Voltar",
            command=self.voltar_para_menu,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_voltar.pack(pady=10)
        self.arquivo_selecionado = ""

    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def mostrar(self):
        self.main_window.janela.withdraw()
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_para_menu)
        self.centralizar_janela(self.janela)
        self.janela.mainloop()

    def selecionar_arquivo(self):
        self.arquivo_selecionado = filedialog.askopenfilename(
            filetypes=(("Planilhas", "*.xlsx;*.xls"), ("Todos os arquivos", "*.*"))
        )

    def cadastrar_alunos(self):
        if self.arquivo_selecionado:
            try:
                df = pd.read_excel(self.arquivo_selecionado)
                for _, row in df.iterrows():
                    nome = row["Nome"]
                    serie = row["Série"]
                    matricula = row["Matrícula"]
                    self.main_window.cadastrar_aluno(nome, serie, matricula, show_message=False)
            except Exception as e:
                messagebox.showerror("Cadastro de Alunos", f"Erro ao ler planilha: {str(e)}")
            messagebox.showinfo("Cadastro de Alunos", "Todos os alunos foram cadastrados com sucesso!")
        else:
            messagebox.showwarning("Cadastro de Alunos", "Nenhum arquivo selecionado.")


    def voltar_para_menu(self):
        self.janela.destroy()
        self.main_window.janela.deiconify()

class MainWindow:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Ifatech")
        self.janela.geometry("800x400")
        self.centralizar_janela(self.janela)

        self.frame_cadastro = tk.Frame(self.janela)
        self.frame_cadastro.pack()

        self.button_cadastro = tk.Button(
            self.frame_cadastro,
            text="Cadastro de Alunos",
            command=self.exibir_tela_cadastro,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_cadastro.pack(pady=10)
        self.button_buscar = tk.Button(
            self.frame_cadastro,
            text="Buscar Aluno",
            command=self.exibir_janela_busca,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_buscar.pack(pady=10)
        self.button_verificar_qr_code = tk.Button(
            self.frame_cadastro,
            text="Verificar QR Code",
            command=self.exibir_janela_verificar_qr_code,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_verificar_qr_code.pack(pady=10)
        self.button_registros = tk.Button(
            self.frame_cadastro,
            text="Registros",
            command=self.exibir_janela_registros,
            font=("Arial", 13),
            wraplength=150,
            width=20,
            height=2,
        )
        self.button_registros.pack(pady=10)
        self.janela.mainloop()
    
    def dentro_do_periodo(self):
        agora = datetime.datetime.now()
        dia_semana = agora.weekday()

        hora_atual = agora.hour + agora.minute / 60

        if 0 <= dia_semana <= 2:  # Segunda, terça e quarta-feira
            if 7 <= hora_atual < 12 or 12 <= hora_atual < 17:
                return True
        elif 3 <= dia_semana <= 6:  # Quinta, sexta, sábado e domingo
            if 8 <= hora_atual < 17:
                return True

        return False


    def centralizar_janela(self, window):
        window.update_idletasks()
        largura = window.winfo_width()
        altura = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (largura // 2)
        y = (window.winfo_screenheight() // 2) - (altura // 2)
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def exibir_tela_cadastro(self):
        self.janela.withdraw()
        tela_cadastro = TelaCadastro(self)
        tela_cadastro.mostrar()

    def voltar_para_menu(self):
        self.janela.deiconify()

    def cadastrar_aluno(self, nome, serie, matricula, show_message=True):
        if nome and serie and matricula:
            aluno = {"nome": nome, "serie": serie, "matricula": matricula}
            codigo = self.gerar_codigo_aleatorio()
            self.salvar_aluno(aluno, codigo)
            self.gerar_qr_code_e_salvar(aluno, codigo)
        else:
            messagebox.showwarning("Cadastro de Alunos", "Por favor, preencha todos os campos!")

    def verificar_aluno_cadastrado(self, matricula):
        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                matricula_aluno = dados[2]
                if matricula_aluno == matricula:
                    return True
        return False

    def exibir_janela_busca(self):
        nome_busca = simpledialog.askstring("Buscar Aluno", "Digite o nome do aluno:")
        if nome_busca:
            alunos_encontrados = self.buscar_aluno_por_nome(nome_busca)
            if alunos_encontrados:
                self.exibir_janela_opcoes(alunos_encontrados)
            else:
                messagebox.showinfo("Buscar Aluno", "Nenhum aluno encontrado.")
        else:
            messagebox.showwarning("Buscar Aluno", "Por favor, digite um nome para busca.")

    def exibir_janela_verificar_qr_code(self):
        while True:
            codigo = simpledialog.askstring("Verificar QR Code", "Digite o código do aluno:")
            if codigo:
                self.verificar_qr_code(codigo)
            else:
                messagebox.showwarning("Verificar QR Code", "Por favor, digite o código do aluno.")
            resposta = messagebox.askquestion("Verificar QR Code", "Deseja verificar outro código?")
            if resposta == "no":
                break

    def exibir_janela_opcoes(self, alunos):
        self.janela_opcoes = JanelaOpcoes(self.janela, self, alunos)
        self.janela.withdraw()

    def exibir_janela_registros(self):
        self.janela_registros = JanelaRegistros(self.janela, self)
        self.janela.withdraw()

    def exibir_tela_cadastro_planilha(self):
        self.tela_cadastro_planilha = TelaCadastroPlanilha(self)
        self.tela_cadastro_planilha.mostrar()

    def salvar_aluno(self, aluno, codigo):
        data_registro = datetime.date.today().strftime("%Y-%m-%d")
        with open("registros.txt", "a") as arquivo:
            arquivo.write(f"{aluno['nome']},{aluno['serie']},{aluno['matricula']},{codigo},{data_registro}\n")

    def gerar_qr_code_e_salvar(self, aluno, codigo):
        nome_arquivo = f"{codigo}_{aluno['nome']}.png"

        qr_code = qrcode.make(codigo)
        qr_code.save(os.path.join("qr_codes", nome_arquivo))

    def gerar_codigo_aleatorio(self):
        codigo = str(random.randint(10000, 99999))
        return codigo

    def buscar_aluno_por_nome(self, nome):
        alunos_encontrados = []

        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                nome_aluno = dados[0]
                serie_aluno = dados[1]
                matricula_aluno = dados[2]
                qr_code_aluno = dados[3]

                if nome.lower() in nome_aluno.lower():
                    aluno = f"{nome_aluno},{serie_aluno},{matricula_aluno},{qr_code_aluno}"
                    alunos_encontrados.append(aluno)

        return alunos_encontrados

    def verificar_qr_code(self, codigo):
        encontrado = False
        aluno = None

        with open("registros.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                codigo_aluno = dados[3]
                data_registro_aluno = dados[4]

                if codigo == codigo_aluno:
                    encontrado = True
                    if self.verificar_ficha_usada(codigo):
                        messagebox.showerror("Verificar QR Code", "Código já verificado hoje.")
                        return
                    else:
                        aluno = linha
                    break

        if encontrado:
            data_atual = datetime.date.today().strftime("%Y-%m-%d")
            hora_atual = datetime.datetime.now().strftime("%H:%M:%S")

            if aluno is not None:  # Verifica se aluno não é None
                if self.dentro_do_periodo():
                    self.registrar_ficha_usada(aluno, codigo, data_atual, hora_atual)
                    messagebox.showinfo("Verificar QR Code", "Aluno apto a receber.")
                else:
                    messagebox.showerror("Verificar QR Code", "O aluno não pode receber a ficha no momento.")
            elif not self.verificar_ficha_usada(codigo):
                messagebox.showerror("Verificar QR Code", "Erro ao obter informações do aluno.")
        else:
            messagebox.showerror("Verificar QR Code", "Código inválido. Por favor, verifique o código digitado.")

    def verificar_ficha_usada(self, codigo):
        data_atual = datetime.date.today()
        dia_semana = data_atual.weekday()  # 0 é segunda-feira, 6 é domingo
        data_atual_str = data_atual.strftime("%Y-%m-%d")
        hora_atual = datetime.datetime.now().strftime("%H:%M:%S")
        with open("fichas_usadas.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(",")
                if len(dados) < 4:  # Verificar se a linha tem o número esperado de elementos
                    continue
                codigo_ficha = dados[1]
                data_registro_ficha = dados[2]
                hora_registro_ficha = dados[3]
                if codigo == codigo_ficha and data_atual_str == data_registro_ficha:
                    if self.dentro_do_periodo():
                        hora_registro = datetime.datetime.strptime(hora_registro_ficha, "%H:%M:%S").time()
                        hora_agora = datetime.datetime.strptime(hora_atual, "%H:%M:%S").time()
                        # Se for segunda-feira (0), terça-feira (1) ou quarta-feira (2)
                        if dia_semana <= 2:
                            periodo_manha = datetime.time(7, 0) <= hora_registro < datetime.time(12, 0)
                            periodo_tarde = datetime.time(12, 0) <= hora_registro < datetime.time(17, 0)
                            # Verificar se o registro anterior foi feito no mesmo período do dia
                            if (periodo_manha and datetime.time(7, 0) <= hora_agora < datetime.time(12, 0)) or \
                                    (periodo_tarde and datetime.time(12, 0) <= hora_agora < datetime.time(17, 0)):
                                return True
                        else:  # Se for quinta-feira (3), sexta-feira (4), sábado (5) ou domingo (6)
                            periodo_dia = datetime.time(8, 0) <= hora_registro < datetime.time(17, 0)
                            # Verificar se o registro anterior foi feito no mesmo período do dia
                            if periodo_dia and datetime.time(8, 0) <= hora_agora < datetime.time(17, 0):
                                return True
        return False

    def registrar_ficha_usada(self, aluno, codigo, data, hora):
        if aluno is not None:  # Verifica se aluno não é None
            nome_aluno = aluno.split(",")[0].strip()
            with open("fichas_usadas.txt", "a") as arquivo:
                arquivo.write(f"{nome_aluno},{codigo},{data},{hora}\n")
        else:
            messagebox.showerror("Registrar ficha usada", "Erro ao obter informações do aluno.")

if __name__ == "__main__":
    app = MainWindow()

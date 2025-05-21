import json
import os
import hashlib
import statistics

ARQUIVO_DADOS = "dados.json"

# === ADMIN CONFIGURAÇÃO ===
ADMIN_EMAIL = "admin@plataforma.com"
ADMIN_SENHA_HASH = hashlib.md5("admin123".encode()).hexdigest()

# === PERGUNTAS DOS CURSOS ===
PERGUNTAS = {
    "Matemática": [
        {"pergunta": "Quanto é 2 + 2?", "resposta": "4"},
        {"pergunta": "Quanto é 5 * 3?", "resposta": "15"},
        {"pergunta": "Quanto é 10 - 7?", "resposta": "3"},
        {"pergunta": "Quanto é 9 / 3?", "resposta": "3"},
    ],
    "Português": [
        {"pergunta": "Qual é o plural de 'cão'?", "resposta": "cães"},
        {"pergunta": "Qual é o antônimo de 'feliz'?", "resposta": "triste"},
        {"pergunta": "Qual é a classe gramatical de 'rapidamente'?", "resposta": "advérbio"},
        {"pergunta": "Qual é o sujeito da frase: 'O menino correu'?", "resposta": "o menino"},
    ],
    "Ciências": [
        {"pergunta": "Qual planeta é conhecido como o planeta vermelho?", "resposta": "marte"},
        {"pergunta": "Qual órgão é responsável pela circulação do sangue?", "resposta": "coração"},
        {"pergunta": "Quantos ossos tem o corpo humano (aproximadamente)?", "resposta": "206"},
        {"pergunta": "A água é formada por quais elementos?", "resposta": "hidrogênio e oxigênio"},
    ]
}

# === Funções auxiliares ===

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as arquivo:
            return json.load(arquivo)
    return []

def salvar_dados(lista_info_alunos):
    with open(ARQUIVO_DADOS, "w") as arquivo:
        json.dump(lista_info_alunos, arquivo, indent=4)

def hash_senha(senha):
    return hashlib.md5(senha.encode()).hexdigest()

def email_existe(email, lista_info_alunos):
    return any(aluno["email"] == email for aluno in lista_info_alunos)

def encontrar_aluno_por_email(email, lista_info_alunos):
    for aluno in lista_info_alunos:
        if aluno["email"] == email:
            return aluno
    return None

# === Cadastro de aluno ===

def coletar_dados():
    nome = input("Digite o seu nome: ")
    celular = input("Digite o seu telefone: ")
    email = input("Digite o seu E-mail: ")
    cpf = input("Digite o seu CPF: ")
    senha = input("Crie uma senha: ")
    
    return {
        "nome": nome,
        "celular": celular,
        "email": email,
        "cpf": cpf,
        "senha": hash_senha(senha),
        "cursos": [],
        "notas": {}
    }

# === Login ===

def login(lista_info_alunos):
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")
    senha_hash = hash_senha(senha)

    if email == ADMIN_EMAIL and senha_hash == ADMIN_SENHA_HASH:
        print("Login como administrador.")
        menu_admin(lista_info_alunos)
        return

    aluno = encontrar_aluno_por_email(email, lista_info_alunos)
    if aluno and aluno["senha"] == senha_hash:
        print("Login bem-sucedido!")
        menu_aluno(aluno, lista_info_alunos)
    else:
        print("Email ou senha incorretos.")

# === Menu do aluno ===

def exibir_dados_aluno(aluno):
    print("\n--- Seus Dados ---")
    for chave, valor in aluno.items():
        if chave not in ["senha", "cursos", "notas"]:
            print(f"{chave.capitalize()}: {valor}")

def exibir_cursos(aluno):
    print("\n--- Seus Cursos ---")
    if aluno["cursos"]:
        for i, curso in enumerate(aluno["cursos"], 1):
            print(f"{i}. {curso}")
    else:
        print("Você ainda não está matriculado em nenhum curso.")

def adicionar_curso(aluno):
    cursos_disponiveis = list(PERGUNTAS.keys())
    print("\nCursos disponíveis:")
    for i, curso in enumerate(cursos_disponiveis, 1):
        print(f"{i}. {curso}")
    
    try:
        opcao = int(input("Escolha o curso (número): "))
        novo_curso = cursos_disponiveis[opcao - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    if novo_curso in aluno["cursos"]:
        print("Você já está matriculado neste curso.")
    else:
        aluno["cursos"].append(novo_curso)
        print("Curso adicionado com sucesso!")

def realizar_prova(aluno, lista_info_alunos):
    print("\n=== REALIZAR PROVA ===")
    cursos_disponiveis = aluno["cursos"]
    
    if not cursos_disponiveis:
        print("Você não está matriculado em nenhum curso.")
        return

    for i, curso in enumerate(cursos_disponiveis, 1):
        print(f"{i}. {curso}")
    
    try:
        opcao = int(input("Escolha o curso (número): "))
        curso_escolhido = cursos_disponiveis[opcao - 1]
    except (ValueError, IndexError):
        print("Opção inválida.")
        return

    print(f"\nIniciando prova de {curso_escolhido}...")
    acertos = 0
    for pergunta in PERGUNTAS[curso_escolhido]:
        resposta = input(pergunta["pergunta"] + " ").strip().lower()
        if resposta == pergunta["resposta"].lower():
            acertos += 1

    nota = (acertos / 4) * 10
    print(f"Você acertou {acertos} de 4. Nota: {nota:.1f}")

    if curso_escolhido not in aluno["notas"]:
        aluno["notas"][curso_escolhido] = []

    aluno["notas"][curso_escolhido].append(nota)
    salvar_dados(lista_info_alunos)

def exibir_relatorio(aluno):
    print("\n=== RELATÓRIO DE NOTAS ===")
    if not aluno.get("notas"):
        print("Nenhuma nota registrada ainda.")
        return

    for curso, notas in aluno["notas"].items():
        media = statistics.mean(notas)
        try:
            moda = statistics.mode(notas)
        except statistics.StatisticsError:
            moda = "sem moda"
        print(f"\nCurso: {curso}")
        print(f"Notas: {notas}")
        print(f"Média: {media:.2f}")
        print(f"Moda: {moda}")

def menu_aluno(aluno, lista_info_alunos):
    while True:
        print("\n===== MENU DO ALUNO =====")
        print("1. Ver meus dados")
        print("2. Ver meus cursos")
        print("3. Adicionar curso")
        print("4. Realizar prova")
        print("5. Ver relatório de notas")
        print("6. Logout")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            exibir_dados_aluno(aluno)
        elif opcao == "2":
            exibir_cursos(aluno)
        elif opcao == "3":
            adicionar_curso(aluno)
            salvar_dados(lista_info_alunos)
        elif opcao == "4":
            realizar_prova(aluno, lista_info_alunos)
        elif opcao == "5":
            exibir_relatorio(aluno)
        elif opcao == "6":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida.")

# === Menu do administrador ===

def excluir_aluno(lista_info_alunos):
    email = input("Digite o e-mail do aluno a ser excluído: ")
    aluno = encontrar_aluno_por_email(email, lista_info_alunos)
    if aluno:
        lista_info_alunos.remove(aluno)
        salvar_dados(lista_info_alunos)
        print(f"Aluno com email '{email}' foi excluído.")
    else:
        print("Aluno não encontrado.")

def excluir_curso_de_aluno(lista_info_alunos):
    email = input("Digite o e-mail do aluno: ")
    aluno = encontrar_aluno_por_email(email, lista_info_alunos)
    if not aluno:
        print("Aluno não encontrado.")
        return

    if not aluno["cursos"]:
        print("Este aluno não possui cursos.")
        return

    print("Cursos do aluno:")
    for i, curso in enumerate(aluno["cursos"], 1):
        print(f"{i}. {curso}")

    try:
        opcao = int(input("Digite o número do curso para remover: ")) - 1
        if 0 <= opcao < len(aluno["cursos"]):
            curso_removido = aluno["cursos"].pop(opcao)
            salvar_dados(lista_info_alunos)
            print(f"Curso '{curso_removido}' removido com sucesso.")
        else:
            print("Opção inválida.")
    except ValueError:
        print("Entrada inválida.")

def menu_admin(lista_info_alunos):
    while True:
        print("\n===== MENU DO ADMINISTRADOR =====")
        print("1. Visualizar todos os alunos")
        print("2. Excluir aluno")
        print("3. Excluir curso de um aluno")
        print("4. Logout")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if not lista_info_alunos:
                print("Nenhum aluno cadastrado.")
            else:
                for i, aluno in enumerate(lista_info_alunos, 1):
                    print(f"\nAluno {i}:")
                    for chave, valor in aluno.items():
                        if chave != "senha":
                            print(f"{chave.capitalize()}: {valor}")
        elif opcao == "2":
            excluir_aluno(lista_info_alunos)
        elif opcao == "3":
            excluir_curso_de_aluno(lista_info_alunos)
        elif opcao == "4":
            print("Logout do administrador.")
            break
        else:
            print("Opção inválida.")

# === Menu principal ===

def menu():
    lista_info_alunos = carregar_dados()

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Cadastrar novo aluno")
        print("2. Visualizar todos os alunos")
        print("3. Login")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            novo_aluno = coletar_dados()
            if email_existe(novo_aluno["email"], lista_info_alunos):
                print("Erro: Este e-mail já está cadastrado.")
            else:
                lista_info_alunos.append(novo_aluno)
                salvar_dados(lista_info_alunos)
                print("Aluno cadastrado com sucesso!")

        elif opcao == "2":
            if not lista_info_alunos:
                print("Nenhum aluno cadastrado.")
            else:
                for i, aluno in enumerate(lista_info_alunos, 1):
                    print(f"\nAluno {i}:")
                    for chave, valor in aluno.items():
                        if chave != "senha":
                            print(f"{chave.capitalize()}: {valor}")

        elif opcao == "3":
            login(lista_info_alunos)

        elif opcao == "4":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida.")

# === Executar o sistema ===
if __name__ == "__main__":
    menu()

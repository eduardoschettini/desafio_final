# -----------------------
# depencies
# -----------------------
import json
import os
import uuid
import random
import sys

# -----------------------
# load settings
# -----------------------
sys.path.append('./data/')
from data import settings

# -----------------------
# SYSTEM functions 
# -----------------------
# não alterar nada das funções de system
def gera_transacao(categoria):
    return {
        "UUID": str(uuid.uuid4()),
        "valor": round(random.uniform(1.0, 1000.0), 2),  # Preço aleatório entre 1 e 1000
        "categoria": categoria
    }

def criar_transacoes(proporcao_categorias, num_transacoes=1,  categoria=None, seed=settings.seed):
    assert sum([proporcao_categorias[k] for k in proporcao_categorias])==1, '`proporcao_categorias` não soma 100%! Favor rever.'

    # garantir reprodutibilidade dos valores
    random.seed(seed)
    
    # Insere as transações para uma determinada categoria.
    if categoria:
        return [gera_transacao(categoria) for _ in range(0, num_transacoes)]
    
    # Calcula o número de transações por categoria com base na proporção
    numero_transacoes_por_categoria = {categoria: int(num_transacoes * proporcao) for categoria, proporcao in proporcao_categorias.items()}

    # Gera as transações
    transacoes = []
    for categoria, quantidade in numero_transacoes_por_categoria.items():
        for _ in range(quantidade):
            transacoes.append(gera_transacao(categoria))

    return transacoes

def salvar_json(transacoes, path2save, filename):
    # create path if not exist
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    with open(os.path.join(path2save,filename), "w") as file:
        json.dump(transacoes, file, indent=4)
    print(f"Arquivo salvo em: {os.path.abspath(os.path.curdir)+'/'+path2save+'/'+filename}")

def criar_bd(num_transacoes:int = 10000, proporcao_categorias:list = settings.categorias_proporcao, path2save="./data", filename='transactions.json'):
    salvar_json(criar_transacoes(num_transacoes=num_transacoes,  proporcao_categorias=proporcao_categorias),
                path2save, filename
    )

def load_bd(filepath='./data/transactions.json'):
    with open(filepath, "r") as file:
        bd = json.load(file)
    return bd

def tela_inicial():
    global nomeUsuario
    print(f"Bem-vindo {nomeUsuario}!")
    print('conta: 0000001-0')
    print("\nEste programa permite gerenciar transações de sua conta pessoal.")
    print("\nEscolha uma das opções abaixo:")
    print("1. Visualizar relatórios")
    print("2. Cadastrar transações")
    print("3. Editar transações")
    print("4. Excluir transações")
    print("5. Consultar transação por ID")
    print("-" * 10)
    print("0. Sair")
    print('\n')

# -----------------------
# PROGRAM functions 
# -----------------------
# pode editar como quiser as funções abaixo! Somente não altere os nomes das funções.
# para alterar as funções abaixo, basta apagar o `pass` e preencher com as instruções.

def run(tela=None):
    print(f'Tipo de tela: {tela}')
    
    global nomeUsuario
    
    ativo = True
    
    if tela is None:
        clear_terminal()
        tela = 'tela_inicial' 
        

        nomeUsuario = input("Informe o seu nome: ")

    # exibe a tela inicial
    while ativo:
        clear_terminal() 
        tela_inicial()
        opcao =  input("Digite o número da opção: ")
        clear_terminal()
        print(f"Tamanho do banco de dados: {len(bd)} transações") 
        try:
            match int(opcao):
                case 1:
                    print("Opção selecionada: Visualizar relatórios\n")
                    visualizar_relatorios(tela)
                    continue
                case 2:
                    print("Cadastrar transações\n")
                    cadastrar_transacao(tela)
                    continue
                case 3:
                    print("Opção selecionada: Editar transações\n")
                    editar_transacao_por_ID(tela)
                    continue
                case 4:
                    print("Opção selecionada: Excluir transações\n")
                    excluir_transacao(tela)
                    continue
                case 5:
                    print("Opção selecionada: Consultar transação por ID\n")
                    consultar_transacao_por_ID(tela)
                    continue
                case 0:
                    print("Obrigado por usar nosso programa!!!\n")
                    ativo = False
                    sys.exit(0)
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    continue
        except ValueError:
            print("\n\nPor favor, digite um número inteiro válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
            continue
    

def visualizar_relatorios(tela_anterior):
    global bd
    global nomeUsuario
    
    jaPesquisou = False

    ativo = True

    while ativo:
        clear_terminal()
        print(f"Bem-vindo, {nomeUsuario}!")
        print('conta: 0000001-0')
        print("\n- Visualizar Relatórios.")
        print("\nEscolha uma das opções abaixo:")

        if not jaPesquisou:
            print("1. Visualizar um Relatório")
        else:
            print("1. Visualizar um novo Relatório")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            match int(opcao):
                case 1:
                    clear_terminal()
                    print("Opção selecionada: Visualizar relatórios\n")
                    print("""Informe o tipo de relatório que deseja visualizar:
                    \n1. Consultar transações por UUDI
                    \n2. Calcular total de transações
                    \n3. Mostrar as 5 transações com maior valor
                    \n4. Calcular média das transações""")
                    
                    opcao_relatorio = input("\nDigite o número da opção (1-4): ")

                    match int(opcao_relatorio):
                        case 1:
                            consultar_transacao_por_ID('visualizar_relatorios')
                            jaPesquisou = True
                            continue
                        case 2:
                            calcular_total_transacoes('visualizar_relatorios')
                            jaPesquisou = True
                            continue
                        case 3:
                            mostrar_m5_transacoes('visualizar_relatorios')
                            jaPesquisou = True
                            continue
                        case 4:
                            calcular_media('visualizar_relatorios')
                            jaPesquisou = True
                            continue
                        case _:
                            print("Opção inválida, escolha uma opção válida.")
                            input("\n\nPressione Enter para continuar...")
                            continue                    
                case 2:
                    run('consultar_transacao_por_ID')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    retorna_tela_anterior('visualizar_relatorios', tela_anterior)
                    break
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    continue

            input("Pressione Enter para continuar...")
        except ValueError:
            clear_terminal() 
            print("\n\nPor favor, digite um número inteiro válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
            continue

def salvar_relatorio(tela):
    print('Função salvar_relatorio ainda não implementada.')
    input("Pressione Enter para continuar...")

def calcular_total_transacoes(tela):
    print('Função calcular_total_transacoes ainda não implementada.')
    input("Pressione Enter para continuar...")
    visualizar_relatorios('calcular_total_transacoes')

def mostrar_m5_transacoes(tela):
    print('Função mostrar_m5_transacoes ainda não implementada.')
    input("Pressione Enter para continuar...")
    visualizar_relatorios('mostrar_m5_transacoes')

def calcular_media():
    print('Função calcular_media ainda não implementada.')
    input("Pressione Enter para continuar...")
    visualizar_relatorios('calcular_media')

def consultar_transacao_por_ID(tela_anterior):
    global bd
    global nomeUsuario
    
    jaPesquisou = False

    ativo = True

    while ativo:
        
        if tela is None:
            clear_terminal()
            print(f"Bem-vindo, {nomeUsuario}!")
            print('conta: 0000001-0')
            print("\n- Pesquisar Transação por UUID.")
            print("\nEscolha uma das opções abaixo:")

        if not jaPesquisou:
            print("1. Pesquisar uma transação por UUID")
        else:
            print("1. Pesquisar uma nova transação por UUID")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            match int(opcao):
                case 1:
                    clear_terminal()
                    print("Opção selecionada: Visualizar relatórios\n")
                    uuid_to_search = input("Digite o UUID da transação que deseja pesquisar: ")

                    transacao = next((t for t in bd if t['UUID'] == uuid_to_search), None)
                    if transacao:
                        print("\nTransação encontrada: \n"
                            f"UUID: {transacao['UUID']}\n"
                            f"Valor: R$ {transacao['valor']}\n"
                            f"Categoria: {transacao['categoria']}\n\n")
                    else:
                        print("Transação não encontrada.")
                    
                    jaPesquisou = True
                    
                    if tela is None:
                        input("\n\nPressione Enter para continuar...")
                    
                    continue
                case 2:
                    run('consultar_transacao_por_ID')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    retorna_tela_anterior('consultar_transacao_por_ID', tela_anterior)
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    input("\n\nPressione Enter para continuar...")
                    continue

        except ValueError:
            clear_terminal() 
            print("\n\nPor favor, digite um número inteiro válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
            continue

def cadastrar_transacao(tela_anterior):
    global bd
    global nomeUsuario
    
    jaCadastrou = False

    ativo = True

    while ativo:
        clear_terminal()
        print(f"Bem-vindo, {nomeUsuario}!")
        print('conta: 0000001-0')
        print("\n- Cadastrar uma nova transação.")
        print("\nEscolha uma das opções abaixo:")

        if not jaCadastrou:
            print("1. Cadastrar uma transação")
        else:
            print("1. Cadastrar uma nova transação")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            categoriaValida = False
            match int(opcao):
                case 1:
                    clear_terminal()
                    print("Informe os dados necessário para cadastrar numa nova transacao\n")
                    chaves_categorias = list(settings.categorias_proporcao.keys())
                    print("Categorias disponíveis:")
                    for i, categoria in enumerate(chaves_categorias, start=1):
                        print(f"{i}. {categoria}")

                    opcao_categoria = int(input("\nDigite a categoria da transação (1 - 7): "))

                    if 1 <= opcao_categoria <= len(chaves_categorias):
                        nome_categoria = chaves_categorias[opcao_categoria - 1]
                        print(f"Você selecionou a categoria: {nome_categoria}")
                        categoriaValida = True
                    else:
                        print("\n\nErro: O número deve ser entre 1 e 7. Por favor, tente novamente.")
                        input("\nPressione Enter para continuar...")
                        clear_terminal()
                        continue
                    
                    if categoriaValida:   
                        valor = float(input("\nDigite o valor da transação: "))

                        nova_transacao = {'UUID': str(uuid.uuid4()), 'valor': valor, 'categoria': nome_categoria}

                        clear_terminal()
                        print(f"Transação cadastrada com sucesso!\n"
                            f"UUID: {nova_transacao['UUID']}\n"
                            f"Valor: {nova_transacao['valor']}\n"
                            f"Categoria: {nova_transacao['categoria']}\n\n")
                        bd.append(nova_transacao)
                        jaCadastrou = True
                        salvar_json(bd, './data', 'transactions.json')
                        print("Transação salva com sucesso!")
                        
                        input("\n\nPressione Enter para continuar...")
                        continue
                case 2:
                    run('cadastrar_transacao')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    retorna_tela_anterior('cadastrar_transacao', tela_anterior)
                    break
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    continue
        except ValueError as e:
            clear_terminal() 
            print("\n\nPor favor, digite um número válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            input("Pressione Enter para continuar...")

def editar_transacao_por_ID(tela_anterior):
    global bd
    global nomeUsuario
    
    jaCadastrou = False

    ativo = True

    while ativo:
        clear_terminal()
        print(f"Bem-vindo, {nomeUsuario}!")
        print('conta: 0000001-0')
        print("\n- Editar Transação por UUID.")
        print("\nEscolha uma das opções abaixo:")

        if not jaCadastrou:
            print("1. Editar uma transação")
        else:
            print("1. Editar uma nova transação")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            categoriaValida = False
            match int(opcao):
                case 1:
                    #clear_terminal()

                    clear_terminal()
                    print("Opção selecionada: Editar uma transação\n")
                    uuid_to_modified = input("Digite o UUID da transação que deseja modificar: ")

                    transacao = next((t for t in bd if t['UUID'] == uuid_to_modified), None)
                    if transacao:
                        print("\nTransação encontrada: \n"
                            f"UUID: {transacao['UUID']}\n"
                            f"Valor: {transacao['valor']}\n"
                            f"Categoria: {transacao['categoria']}\n\n")
                        
                        print("Informe a nova categoria\n")
                        chaves_categorias = list(settings.categorias_proporcao.keys())
                        print("Categorias disponíveis:")
                        for i, categoria in enumerate(chaves_categorias, start=1):
                            print(f"{i}. {categoria}")

                        opcao_categoria = int(input("\nDigite a categoria da transação (1 - 7), -1 para não editar a categoria: "))
                        if opcao_categoria != -1:
                            if 1 <= opcao_categoria <= len(chaves_categorias):
                                nova_categoria = chaves_categorias[opcao_categoria - 1]
                                print(f"Você selecionou a categoria: {nova_categoria}")
                                categoriaValida = True
                            else:
                                print("\n\nErro: O número deve ser entre 1 e 7. Por favor, tente novamente.")
                                input("\nPressione Enter para continuar...")
                                clear_terminal()
                                continue
                        else:
                            nova_categoria = transacao['categoria']
                            categoriaValida = True
                    
                        if categoriaValida:   
                            valor = float(input("\nDigite o valor da transação (-1 para não editar o valor): "))
                            if valor >= 0:
                                novo_valor = valor
                            else:
                                novo_valor = transacao['valor']
                            
                            nova_transacao = {'UUID': transacao['UUID'], 'valor': novo_valor, 'categoria': nova_categoria}

                            clear_terminal()
                            print(f"Dados da alteração da Transação!\n"
                                f"UUID: {nova_transacao['UUID']}\n"
                                f"Valor: {nova_transacao['valor']}\n"
                                f"Categoria: {nova_transacao['categoria']}\n")
                            
                            print("Deseja salvar as alterações? (s/n)")
                            
                            if(input().strip().lower() == 's'):
                                uuid_to_update = nova_transacao['UUID']
                                for idx, transacao in enumerate(bd):
                                    if transacao['UUID'] == uuid_to_update:
                                        bd[idx] = nova_transacao  
                                        salvar_json(bd, './data', 'transactions.json')
                                        print("Transação atualizada e salva com sucesso!")
                                        jaCadastrou = True

                            input("\n\nPressione Enter para continuar...")
                            continue

                    else:
                        print("Transação não encontrada.")

                    
                case 2:
                    run('cadastrar_transacao')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    retorna_tela_anterior('editar_transacao_por_ID', tela_anterior)
                    break
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    continue
        except ValueError as e:
            clear_terminal() 
            print("\n\nPor favor, digite um número válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            input("Pressione Enter para continuar...")

def excluir_transacao(tela_anterior):
    global bd
    global nomeUsuario
    
    jaCadastrou = False

    ativo = True

    while ativo:
        clear_terminal()
        print(f"Bem-vindo, {nomeUsuario}!")
        print('conta: 0000001-0')
        print("\n- Excluir Transação por UUID.")
        print("\nEscolha uma das opções abaixo:")

        if not jaExcluiu:
            print("1. Excluir uma transação")
        else:
            print("1. Excluir uma nova transação")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            categoriaValida = False
            match int(opcao):
                case 1:
                    #clear_terminal()

                    clear_terminal()
                    print("Opção selecionada: Excluir Transação\n")
                    uuid_to_remove = input("Digite o UUID da transação que deseja excluir: ")

                    transacao = next((t for t in bd if t['UUID'] == uuid_to_remove), None)
                    if transacao:
                        print("\nTransação encontrada: \n"
                            f"UUID: {transacao['UUID']}\n"
                            f"Valor: {transacao['valor']}\n"
                            f"Categoria: {transacao['categoria']}\n\n")
                        
                        deseja_remover = int(input("\nDeseja remover a transação? (1 - Sim, 2 - Não): "))
                        if deseja_remover == 1:
                            bd = [t for t in bd if t['UUID'] != uuid_to_remove]
                            salvar_json(bd, './data', 'transactions.json')
                            print("Transação removida com sucesso!")
                            jaCadastrou = True

                            input("\n\nPressione Enter para continuar...")
                            continue

                    else:
                        print("Transação não encontrada.")

                    
                case 2:
                    run('cadastrar_transacao')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    retorna_tela_anterior('excluir_transacao', tela)
                    break
                case _:
                    print("Opção inválida, escolha uma opcão válida.")
                    continue
        except ValueError as e:
            clear_terminal() 
            print("\n\nPor favor, digite um número válido para a opção.\n\n")
            input("Pressione Enter para continuar...")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            input("Pressione Enter para continuar...")

def clear_terminal():
    """Clears the terminal screen based on the operating system."""
    # Check if the operating system is Windows (nt)
    if os.name == 'nt':
        _ = os.system('cls')  # Use 'cls' for Windows
    # Otherwise, assume it's a Unix-like system (Linux, macOS, etc.)
    else:
        _ = os.system('clear') # Use 'clear' for Unix-like systems

def retorna_tela_anterior(tela_atual, tela_anterior):
    match tela_anterior:
        case 'visualizar_relatorios':
            visualizar_relatorios(tela_atual)
            break
        case 'cadastrar_transacao':
            cadastrar_transacao(tela_atual)
            break
        case 'editar_transacao_por_ID':
            editar_transacao_por_ID(tela_atual)
            break  
        case 'excluir_transacao':
            excluir_transacao(tela_atual)
            break
        case 'salvar_relatorio':
            salvar_relatorio(tela_atual)
            break
# -----------------------
# MAIN SCRIPT
# -----------------------
# não alterar nada abaixo
if __name__ == "__main__":
    
    # -----------------------
    # NÃO ALTERAR ESTE BLOCO
    # -----------------------
    # criar o banco de dados caso ele não exista
    print(os.path.abspath('.'))
    if not os.path.exists('./data/transactions.json'):
        criar_bd()
    
    # load bd 
    bd = load_bd()
    # -----------------------

    # -----------------------
    # ABAIXO PODE ALTERAR
    # -----------------------
    #limpar console (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    # inicia o programa
    run()
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
def criar_transacoes(num_transacoes, proporcao_categorias, seed=settings.seed):
    assert sum([proporcao_categorias[k] for k in proporcao_categorias])==1, '`proporcao_categorias` não soma 100%! Favor rever.'

    # garantir reprodutibilidade dos valores
    random.seed(seed)

    # Calcula o número de transações por categoria com base na proporção
    numero_transacoes_por_categoria = {categoria: int(num_transacoes * proporcao) for categoria, proporcao in proporcao_categorias.items()}
    
    transacoes = []
    
    # Gera as transações
    for categoria, quantidade in numero_transacoes_por_categoria.items():
        for _ in range(quantidade):
            transacao = {
                "UUID": str(uuid.uuid4()),
                "valor": round(random.uniform(1.0, 1000.0), 2),  # Preço aleatório entre 1 e 1000
                "categoria": categoria
            }
            transacoes.append(transacao)
    
    return transacoes

def salvar_json(transacoes, path2save, filename):
    # create path if not exist
    if not os.path.exists(path2save):
        os.makedirs(path2save)
    with open(os.path.join(path2save,filename), "w") as file:
        json.dump(transacoes, file, indent=4)
    print(f"Arquivo salvo em: {os.path.abspath(os.path.curdir)+'/'+path2save+'/'+filename}")

def criar_bd(num_transacoes:int = 10000, proporcao_categorias:list = settings.categorias_proporcao, path2save="./data", filename='transactions.json'):
    salvar_json(criar_transacoes(num_transacoes,  proporcao_categorias),
                path2save, filename
    )

def load_bd(filepath='./data/transactions.json'):
    with open(filepath, "r") as file:
        bd = json.load(file)
    return bd

def tela_inicial(tela):
    global nomeUsuario
    
    ativo = True

    if tela is None:
        nomeUsuario = input("Informe o seu nome: ")
    
    while ativo:
        print(f"Bem-vindo, {nomeUsuario}!")
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

        opcao =  input("Digite o número da opção: ")
        try:
            match int(opcao):
                case 1:
                    print("Opção selecionada: Visualizar relatórios\n")
                    visualizar_relatorios()
                    continue
                case 2:
                    print("Cadastrar transações\n")
                    cadastrar_transacao()
                    continue
                case 3:
                    print("Opção selecionada: Editar transações\n")
                    editar_transacao_por_ID()
                    continue
                case 4:
                    print("Opção selecionada: Excluir transações\n")
                    excluir_transacao()
                    continue
                case 5:
                    print("Opção selecionada: Consultar transação por ID\n")
                    consultar_transacao_por_ID('tela_inicial')
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
            continue


# -----------------------
# PROGRAM functions 
# -----------------------
# pode editar como quiser as funções abaixo! Somente não altere os nomes das funções.
# para alterar as funções abaixo, basta apagar o `pass` e preencher com as instruções.

def run():
    """
    Esta é a função principal que vai rodar o programa
    """  
    # exibe a tela inicial
    tela_inicial(None)

def visualizar_relatorios():
    """
    Mostra um menu de opcoes no qual gera relatórios com base na escolha do usuário.
    """
    pass

def salvar_relatorio():
    """
    Salvar o relatório gerado em .txt
    \nAplicar esta função em todos os relatórios listados em `visualizar_relatorios`
    """

def calcular_total_transacoes():
    """
    Calcula o valor total de transações da conta.
    Utilize essa mesma função para o caso `por categoria`
    """
    pass

def mostrar_m5_transacoes():
    """
    Mostra as m5 transações realizadas, sendo m parâmetro que deve ser adicionada à função.
    \nm : 'max','min','median', sendo 
    \n\t'max' mostra os top 5 maior valor,
    \n\t'min' mostra os top 5 menor valor,
    \n\t'median' mostra os top 5 valores próximos a média
    
    Utilize essa mesma função para o caso `por categoria`
    """
    pass

def calcular_media():
    """
    Calcula a média dos valores das transações.
    Utilize essa mesma função para o caso `por categoria`
    """
    pass

def consultar_transacao_por_ID(tela):
    global bd
    global nomeUsuario
    
    jaPesquisou = False

    ativo = True

    while ativo:
        print(f"Bem-vindo, {nomeUsuario}!")
        print('conta: 0000001-0')
        print("\n- Pesquisar Transação por ID.")
        print("\nEscolha uma das opções abaixo:")

        if not jaPesquisou:
            print("1. Pesquisar uma transação")
        else:
            print("1. Pesquisar uma nova transação")

        print("2. Voltar ao menu principal")

        if tela != 'tela_inicial':
            print("3. Voltar à tela anterior")

        opcao =  input("Digite o número da opção: ")

        try:
            match int(opcao):
                case 1:
                    print("Opção selecionada: Visualizar relatórios\n")
                    uuid_to_search = input("Digite o UUID da transação que deseja pesquisar: ")

                    transacao = next((t for t in bd if t['UUID'] == uuid_to_search), None)
                    if transacao:
                        print("\nTransação encontrada: \n"
                            f"UUID: {transacao['UUID']}\n"
                            f"Valor: {transacao['valor']}\n"
                            f"Categoria: {transacao['categoria']}\n\n")
                    else:
                        print("Transação não encontrada.")
                    
                    jaPesquisou = True
                    continue
                case 2:
                    tela_inicial('consultar_transacao_por_ID')
                    ativo = False
                    break
                case 3:
                    ativo = False
                    match tela:
                        case 'visualizar_relatorios':
                            visualizar_relatorios('consultar_transacao_por_ID')
                            break
                        case 'cadastrar_transacao':
                            cadastrar_transacao('consultar_transacao_por_ID')
                            break
                        case 'editar_transacao_por_ID':
                            editar_transacao_por_ID('consultar_transacao_por_ID')
                            break  
                        case 'excluir_transacao':
                            excluir_transacao('consultar_transacao_por_ID')
                            break
                        case 'salvar_relatorio':
                            salvar_relatorio('consultar_transacao_por_ID')
                            break

        except ValueError:
            print("\n\nPor favor, digite um número inteiro válido para a opção.\n\n")
            continue
            
    
    


def cadastrar_transacao():
    """
    Cadastra uma nova transação.
    \nObs:Para gerar um novo uuid, veja como é feito na função `criar_transacoes`.
    """

def editar_transacao_por_ID():
    """
    Edita uma transação específica pelo seu UUID.
    """
    pass

def excluir_transacao():
    """
    Exclui uma transação específica pelo UUID.
    """
    pass

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
    bd = load_bd() # carregar o banco de dados em uma lista em memória
    # -----------------------

    # -----------------------
    # ABAIXO PODE ALTERAR
    # -----------------------
    #limpar console (opcional)
    os.system('cls' if os.name == 'nt' else 'clear')
    # inicia o programa

    run()
import csv
import random
from faker import Faker
from datetime import datetime

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

quantidade_pessoas = 300

# Nome do arquivo CSV
nome_arquivo = 'funcionarios.csv'

# Campos que estarão no CSV
campos = ['nome_completo', 'cpf', 'dt_nasc', 'dpto_empresa', 'cargo', 'salario', 'ativo']

departamentos = ['Comercial', 'Pesquisa e desenvolvimento', 'Financeiro', 'Marketing', 'Logística']

cargos = ['Estagiário', 'Assistente', 'Analista', 'Supervisor', 'Gerente']

dias = [i for i in range(1, 31)]
meses = [i for i in range(1, 13)]
anos = [i for i in range(1970, 2008)]

def gerar_funcionario():
    data_inicio = datetime(1970, 1, 1)  # Data de início das compras
    data_fim = datetime(2007, 12, 31)  # Data atual
    nome = fake.name()
    cpf = str(fake.cpf()).replace(".", "").replace("-", "")
    dt_nasc = fake.date_between_dates(date_start=data_inicio, date_end=data_fim).strftime("%d/%m/%Y")
    dpto_empresa = random.choice(departamentos)
    cargo = random.choice(cargos)
    salario = round(random.uniform(2000, 16000), 2)
    ativo = random.choice([True, False])

    return {
        "nome_completo": nome,
        "cpf": cpf,
        "dt_nasc": dt_nasc,
        "dpto_empresa": dpto_empresa,
        "cargo": cargo,
        "salario": salario,
        "ativo": ativo
    }


# Gera o arquivo CSV em blocos para evitar consumo excessivo de memória
bloco = 100  # Número de registros a serem processados por vez
with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
    escritor_csv.writeheader()  # Escreve o cabeçalho

    id_pessoa = 1
    while id_pessoa <= quantidade_pessoas:
        pessoas_bloco = []
        for _ in range(bloco):
            if id_pessoa > quantidade_pessoas:
                break
            pessoas_bloco.append(gerar_funcionario())
            id_pessoa += 1
        
        # Escreve o bloco de dados no arquivo
        escritor_csv.writerows(pessoas_bloco)

print(f'Dados de {quantidade_pessoas} pessoas foram gerados e salvos no arquivo {nome_arquivo}.')
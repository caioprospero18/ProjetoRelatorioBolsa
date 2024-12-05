import requests
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import date
import os

data_atual = date.today()
data_formatada = data_atual.strftime('%d-%m-%Y')
caminho_pasta = f"Relatório_Ações_Dia_{data_formatada}/"
os.mkdir(caminho_pasta)

with open("Projeto_Analise_Acoes/API-Finnhub.txt", "r") as file:
    api_key = file.read().strip()  


url = "https://finnhub.io/api/v1/quote"
caminho = "Projeto_Analise_Acoes/tickers.xlsx"

list_variacao_diaria = []
list_variacao_anterior = []
list_percentual = []
graficos = []

tickers = pd.read_excel(caminho, sheet_name=0, header=None)

def criar_listas():
    for index, row in tickers.iterrows():
        nome_empresa = row[0]
        ticker = row[1]

        params = {
            "symbol": ticker,
            "token": api_key
        }
        
        try:
            resposta = requests.get(url, params=params)
            resposta.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao fazer requisição para {ticker}: {e}")
            continue
        if resposta.status_code == 200:
            data = resposta.json()
            preco_atual = data['c']
            preco_abertura = data['o']
            preco_fechamento_anterior = data['pc']
            variacao_diaria = preco_atual - preco_abertura
            if preco_abertura != 0:
                percentual = (variacao_diaria/preco_abertura)*100
            if preco_fechamento_anterior != 0:
                variacao_dia_anterior = ((preco_atual - preco_fechamento_anterior) / preco_fechamento_anterior) * 100
            list_variacao_diaria.append({nome_empresa: variacao_diaria})
            list_percentual.append({nome_empresa: percentual})
            list_variacao_anterior.append({nome_empresa: variacao_dia_anterior})
        else:
            print(f"Erro na requisição: {resposta.status_code} - {resposta.text}")
    return list_variacao_diaria, list_percentual, list_variacao_anterior

def ordenar_listas(list_variacao_diaria, list_percentual, list_variacao_anterior):
    list_variacao_diaria_positiva = sorted(list_variacao_diaria, key=lambda d: list(d.values())[0], reverse=True)
    list_percentual_positiva = sorted(list_percentual, key=lambda d: list(d.values())[0], reverse=True)
    list_variacao_anterior_positiva = sorted(list_variacao_anterior, key=lambda d: list(d.values())[0], reverse=True)
    return list_variacao_diaria_positiva, list_percentual_positiva, list_variacao_anterior_positiva

def criar_graficos(list_variacao_diaria_positiva, list_percentual_positiva, list_variacao_anterior_positiva):
    empresas_variacao_diaria = [next(iter(d.items()))[0] for d in list_variacao_diaria_positiva[:5]]
    variacoes_variacao_diaria = [next(iter(d.items()))[1] for d in list_variacao_diaria_positiva[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_variacao_diaria, variacoes_variacao_diaria)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação Diária Positiva")
    grafico_path = caminho_pasta + f"grafico_variacao_diaria_positiva_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

    empresas_percentual = [next(iter(d.items()))[0] for d in list_percentual_positiva[:5]]
    variacoes_percentual = [next(iter(d.items()))[1] for d in list_percentual_positiva[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_percentual, variacoes_percentual)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação Percentual Positiva")
    grafico_path = caminho_pasta + f"grafico_variacao_percentual_positiva_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

    empresas_variacao_anterior = [next(iter(d.items()))[0] for d in list_variacao_anterior_positiva[:5]]
    variacoes_variacao_anterior = [next(iter(d.items()))[1] for d in list_variacao_anterior_positiva[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_variacao_anterior, variacoes_variacao_anterior)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação em Relação ao Dia Anterior Positiva")
    grafico_path = caminho_pasta + f"grafico_variacao_dia_anterior_positiva_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

    list_variacao_diaria_negativa = sorted(list_variacao_diaria, key=lambda d: list(d.values())[0])
    list_percentual_negativa = sorted(list_percentual, key=lambda d: list(d.values())[0])
    list_variacao_anterior_negativa = sorted(list_variacao_anterior, key=lambda d: list(d.values())[0])

    empresas_variacao_diaria_negativa = [next(iter(d.items()))[0] for d in list_variacao_diaria_negativa[:5]]
    variacoes_variacao_negativa = [next(iter(d.items()))[1] for d in list_variacao_diaria_negativa[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_variacao_diaria_negativa, variacoes_variacao_negativa)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação Diária Negativa")
    grafico_path = caminho_pasta + f"grafico_variacao_diaria_negativa_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

    empresas_percentual_negativa = [next(iter(d.items()))[0] for d in list_percentual_negativa[:5]]
    variacoes_percentual_negativa = [next(iter(d.items()))[1] for d in list_percentual_negativa[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_percentual_negativa, variacoes_percentual_negativa)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação Percentual Negativa")
    grafico_path = caminho_pasta + f"grafico_variacao_percentual_negativa_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

    empresas_variacao_anterior_negativa = [next(iter(d.items()))[0] for d in list_variacao_anterior_negativa[:5]]
    variacoes_variacao_anterior_negativa = [next(iter(d.items()))[1] for d in list_variacao_anterior_negativa[:5]]

    plt.figure(figsize=(9, 9))
    plt.bar(empresas_variacao_anterior_negativa, variacoes_variacao_anterior_negativa)
    plt.xlabel("Empresas")
    plt.ylabel("Variação")
    plt.title(f"Top 5 Empresas - Variação em Relação ao Dia Anterior Negativa")
    grafico_path = caminho_pasta + f"grafico_variacao_dia_anterior_negativa_{data_formatada}.png"
    plt.savefig(grafico_path)  
    graficos.append(grafico_path)  
    plt.close()

def criar_pdf():
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.cell(0, 10, f"Relatório de Variação das Ações do dia {data_formatada}", align="C", ln=True)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Este script foi desenvolvido por Caio de Castro Sampaio Próspero", align="C")
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for grafico in graficos:
        pdf.add_page()
        pdf.image(grafico, x=10, y=30, w=180)  
    pdf.output(caminho_pasta + f"Relatorio_Graficos_Acoes_{data_formatada}.pdf")

listas_criadas = criar_listas()
ordenadas = ordenar_listas(*listas_criadas)
criar_graficos(*ordenadas)
criar_pdf()




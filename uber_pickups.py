import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use o backend Agg
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Função para carregar e processar a planilha
def load_data():
    # Carrega a planilha CSV
    file_path = 'es.csv'
    df = pd.read_csv(file_path, sep=',', quotechar='"', encoding='utf-8')

    return df

# Função principal do Streamlit
def main():
    # Título do aplicativo
    st.title('Dashboard Sudes')

    # Carrega os dados
    data = load_data()

    # Sidebar com filtros
    st.sidebar.title('Filtros')

    # Filtro pela primeira coluna (Polo)
    polo_filter = st.sidebar.multiselect('Selecione o Polo', data['Polo'].unique())

    # Filtro pela terceira coluna (Linha de Crédito) sem acentos
    linha_credito_filter = st.sidebar.multiselect('Selecione a Linha de Crédito', data['Linha de Credito'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').unique())

    # Converte a coluna 'Inicio Contrato' para o formato de data
    data['Inicio Contrato'] = pd.to_datetime(data['Inicio Contrato'], errors='coerce')

    # Remove linhas com datas inválidas (NaT)
    data = data.dropna(subset=['Inicio Contrato'])

    # Filtro pelo ano
    years = sorted(data['Inicio Contrato'].dt.year.unique())
    selected_year = st.sidebar.selectbox('Selecione o Ano', years, index=len(years)-1)

    # Filtra os dados pelo ano selecionado
    data = data[data['Inicio Contrato'].dt.year == selected_year]

    # Aplica os filtros se forem selecionados
    if polo_filter:
        data = data[data['Polo'].isin(polo_filter)]
    if linha_credito_filter:
        data = data[data['Linha de Credito'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').isin(linha_credito_filter)]

    # Informações Financeiras e Número de Contratos
    st.header('Informações Financeiras e Número de Contratos')

    # Soma do Saldo Devedor
    saldo_devedor_sum = data['Saldo Devedor'].sum()
    st.info(f'Saldo Devedor: {locale.currency(saldo_devedor_sum, grouping=True)}')

    # Soma do Saldo em Atraso
    saldo_atraso_sum = data['Saldo em Atraso'].sum()
    st.info(f'Saldo em Atraso: {locale.currency(saldo_atraso_sum, grouping=True)}')

    # Número de Contratos
    contract_count = data['Agencia'].count()
    st.info(f'Número de Contratos: {contract_count}')

    # Gráfico de linhas - Número de Contratações por Mês
    st.header('Número de Contratações por Mês')

    # Converte a coluna 'Inicio Contrato' para o formato de data
    data['Inicio Contrato'] = pd.to_datetime(data['Inicio Contrato'], format='%d/%m/%Y')

    # Extrai o mês da data
    data['Mes'] = data['Inicio Contrato'].dt.month

    # Agrupa os dados por mês e conta o número de contratações
    monthly_contract_count = data.groupby('Mes')['Agencia'].count()

    # Cria o gráfico de linhas
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_contract_count.plot(kind='line', marker='o', ax=ax)
    ax.set_xlabel('Mês')
    ax.set_title('Número de Contratações por Mês')

    st.pyplot(fig)

# Chama a função principal
if __name__ == '__main__':
    main()

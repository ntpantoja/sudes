import streamlit as st
import pandas as pd

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

# Chama a função principal
if __name__ == '__main__':
    main()

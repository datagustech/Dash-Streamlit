import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import time
import streamlit as st
import datetime as dt
import locale

df = pd.read_csv('dados_notas.csv', sep=',', decimal=',')
df['Data de Emissão'] = pd.to_datetime(df['Data de Emissão'])
df = df.sort_values('Data de Emissão')

#Definindo configurações da página
st.set_page_config(
    page_title="Dashboard Controladoria - Chappa",
    page_icon='logo_chappa.png',
    layout='wide',
    initial_sidebar_state='expanded')
# Configurando o estilo dos gráficos    
sns.set(style='darkgrid')

with st.sidebar:
    st.image('logo_chappa_maior.png', use_column_width='PNG')
    with st.spinner("Carregando..."):
        time.sleep(0.7)
        add_selectbox = st.selectbox("O quê desejas consultar?", 
                     ("Últimos 5 meses", "Novembro", "Outubro", "Setembro", "Agosto", "Julho"))
    
        
if st.header('Dashboard - Controladoria Fiscal'):
    col1, col2,  = st.columns(2)
    col3, col4, col5 = st.columns(3)


if add_selectbox == 'Últimos 5 meses':
    
    col11, col21, col31 = st.columns(3)
    col41, col51, col61 = st.columns(3)
    with st.container(border=True):
        df_sem_duplicatas = df.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fat_mes = df_sem_duplicatas['Valor da Nota'].sum()

        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)

        col11.markdown(f'<p style="font-size:30px; text-align:center; margin-top:120px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Faturamento: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        
        filtered_value = df[df['Valor da Nota'] < 10000]
        # Criar o histograma interativo com Plotly Express
        fig = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais',
                           labels={'Valor da Nota' : 'Valores das Notas'})

        # Mostrar o gráfico interativo
        col21.plotly_chart(fig, use_container_width=True)
        
        # =========================================================================================================
        
        df['Data de Emissão'] = df['Data de Emissão'].dt.strftime('%m')
        meses_ordenados = ['07', '08', '09', '10', '11']  # Defina a ordem desejada
        df['Data de Emissão'] = pd.Categorical(df['Data de Emissão'], categories=meses_ordenados, ordered=True)
        count_by_month = df.groupby('Data de Emissão')['ID Nota Fiscal'].count().reset_index()

        # Criar o gráfico interativo com Plotly Express
        fig2 = px.line(count_by_month, x='Data de Emissão', y='ID Nota Fiscal', title='Distribuição de Notas Fiscais ao Longo do Tempo',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Data de Emissão': 'Mês'},
                    markers=True, line_shape='linear')

        # Mostrar o gráfico interativo
        col31.plotly_chart(fig2, use_container_width=True)
        
        # ===============================================================================================================================
        
        df_sem_duplicatas = df.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        # Criar o gráfico interativo com Plotly Express
        fig3 = px.bar(df_sem_duplicatas, x='UF do Cliente', title='Distribuição de Notas Fiscais por UF do Cliente',
                    labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                    category_orders={'UF do Cliente': df_sem_duplicatas['UF do Cliente'].value_counts().index})

        # Mostrar o gráfico interativo
        col41.plotly_chart(fig3)
        
        # ===============================================================================================================================

        df_sem_duplicatas = df.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        # Calcular a soma dos valores agrupados por 'UF do Cliente'
        soma_valores = df_sem_duplicatas.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores, x='UF do Cliente', y='Valor da Nota',
                    title='Comparação de Valores Totais das Notas por UF do Cliente',
                    labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                    category_orders={'UF do Cliente': soma_valores.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})

        # Mostrar o gráfico interativo
        col51.plotly_chart(fig4, use_container_width=False)
        
        # ===============================================================================================================================
        
        df_sem_duplicatas = df.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total = df_sem_duplicatas.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        # Calcular a participação em porcentagem de cada cliente no faturamento total
        faturamento_total['Participacao'] = faturamento_total['Valor da Nota'] / faturamento_total['Valor da Nota'].sum() * 100
        # Criar um gráfico de pizza interativo com Plotly Express
        fig5 = px.pie(faturamento_total, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'})
        # Adicionar rótulo de porcentagem na parte externa do gráfico
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        # Exibir o gráfico
        col61.plotly_chart(fig5, use_container_width=False)
        
        # df_sem_duplicatas = df.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        # fat_mes = df_sem_duplicatas['Valor da Nota'].sum()
        # col6.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:2px solid #ccc; border-radius:10px; padding:10px;">Faturamento: R$ {fat_mes:.2f}</p>', unsafe_allow_html=True)
        
# Seção específica para 'Julho'
if add_selectbox == 'Julho':
    # Código específico para o mês de julho
    df_julho = df[df['Data de Emissão'].dt.month == 7]
    df_sem_duplicatas_julho = df_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    with st.container(border=True):
        fat_mes = df_sem_duplicatas_julho['Valor da Nota'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)
        col1.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:50px;">Faturamento Julho: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        # Seção 1: Histograma dos Valores das Notas Fiscais
        filtered_value = df_sem_duplicatas_julho[df_sem_duplicatas_julho['Valor da Nota'] < 10000]
        fig1_julho = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais - Julho',
                                  labels={'Valor da Nota': 'Valores das Notas'})
        col2.plotly_chart(fig1_julho, use_container_width=True)
        
        # Seção 3: Distribuição de Notas Fiscais por UF do Cliente
        df_sem_duplicatas_julho = df_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fig3_julho = px.bar(df_sem_duplicatas_julho, x='UF do Cliente',
                            title='Distribuição de Notas Fiscais por UF do Cliente - Julho',
                            labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': df_sem_duplicatas_julho['UF do Cliente'].value_counts().index})
        col3.plotly_chart(fig3_julho)

        # Seção 4: Comparação de Valores Totais por UF do Cliente
        df_sem_duplicatas_julho = df_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_julho = df_sem_duplicatas_julho.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_julho = px.bar(soma_valores_julho, x='UF do Cliente', y='Valor da Nota',
                            title='Comparação de Valores Totais por UF do Cliente - Julho',
                            labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': soma_valores_julho.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})
        col4.plotly_chart(fig4_julho, use_container_width=False)

        # Seção 5: Participação dos Clientes no Faturamento Total
        faturamento_total_julho = df_sem_duplicatas_julho.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_julho['Participacao'] = faturamento_total_julho['Valor da Nota'] / faturamento_total_julho['Valor da Nota'].sum() * 100
        fig5_julho = px.pie(faturamento_total_julho, names='Cliente', values='Valor da Nota',
                            title='Participação dos Clientes no Faturamento Total - Julho',
                            hover_name='Cliente', hover_data=['Valor da Nota'],
                            labels={'Valor da Nota': 'Faturamento'})
        fig5_julho.update_traces(textposition='inside', textinfo='percent+label')
        col5.plotly_chart(fig5_julho, use_container_width=False)

# 
elif add_selectbox == 'Agosto':
    # Código específico para o mês de Agosto
    df_Agosto = df[df['Data de Emissão'].dt.month == 8]
    df_sem_duplicatas_Agosto = df_Agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    with st.container(border=True):
        fat_mes = df_sem_duplicatas_Agosto['Valor da Nota'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)
        col1.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:50px;">Faturamento Agosto: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        # Seção 1: Histograma dos Valores das Notas Fiscais
        filtered_value = df_sem_duplicatas_Agosto[df_sem_duplicatas_Agosto['Valor da Nota'] < 10000]
        fig1_Agosto = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais - Agosto',
                                labels={'Valor da Nota': 'Valores das Notas'})
        col2.plotly_chart(fig1_Agosto, use_container_width=True)
        
        # Seção 3: Distribuição de Notas Fiscais por UF do Cliente
        df_sem_duplicatas_Agosto = df_Agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fig3_Agosto = px.bar(df_sem_duplicatas_Agosto, x='UF do Cliente',
                            title='Distribuição de Notas Fiscais por UF do Cliente - Agosto',
                            labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': df_sem_duplicatas_Agosto['UF do Cliente'].value_counts().index})
        col3.plotly_chart(fig3_Agosto)

        # Seção 4: Comparação de Valores Totais por UF do Cliente
        df_sem_duplicatas_Agosto = df_Agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_Agosto = df_sem_duplicatas_Agosto.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_Agosto = px.bar(soma_valores_Agosto, x='UF do Cliente', y='Valor da Nota',
                            title='Comparação de Valores Totais por UF do Cliente - Agosto',
                            labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': soma_valores_Agosto.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})
        col4.plotly_chart(fig4_Agosto, use_container_width=False)

        # Seção 5: Participação dos Clientes no Faturamento Total
        faturamento_total_Agosto = df_sem_duplicatas_Agosto.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_Agosto['Participacao'] = faturamento_total_Agosto['Valor da Nota'] / faturamento_total_Agosto['Valor da Nota'].sum() * 100
        fig5_Agosto = px.pie(faturamento_total_Agosto, names='Cliente', values='Valor da Nota',
                            title='Participação dos Clientes no Faturamento Total - Agosto',
                            hover_name='Cliente', hover_data=['Valor da Nota'],
                            labels={'Valor da Nota': 'Faturamento'})
        fig5_Agosto.update_traces(textposition='inside', textinfo='percent+label')
        col5.plotly_chart(fig5_Agosto, use_container_width=False)
        
# Seção específica para 'Setembro'
elif add_selectbox == 'Setembro':
    # Código específico para o mês de Setembro
    df_setembro = df[df['Data de Emissão'].dt.month == 9]
    df_sem_duplicatas_setembro = df_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    with st.container(border=True):
        fat_mes = df_sem_duplicatas_setembro['Valor da Nota'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)
        col1.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:50px;">Faturamento Setembro: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        # Seção 1: Histograma dos Valores das Notas Fiscais
        filtered_value = df_sem_duplicatas_setembro[df_sem_duplicatas_setembro['Valor da Nota'] < 10000]
        fig1_setembro = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais - Setembro',
                                  labels={'Valor da Nota': 'Valores das Notas'})
        col2.plotly_chart(fig1_setembro, use_container_width=True)
        
        # Seção 3: Distribuição de Notas Fiscais por UF do Cliente
        df_sem_duplicatas_setembro = df_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fig3_setembro = px.bar(df_sem_duplicatas_setembro, x='UF do Cliente',
                            title='Distribuição de Notas Fiscais por UF do Cliente - Setembro',
                            labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': df_sem_duplicatas_setembro['UF do Cliente'].value_counts().index})
        col3.plotly_chart(fig3_setembro)

        # Seção 4: Comparação de Valores Totais por UF do Cliente
        df_sem_duplicatas_setembro = df_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_setembro = df_sem_duplicatas_setembro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_setembro = px.bar(soma_valores_setembro, x='UF do Cliente', y='Valor da Nota',
                            title='Comparação de Valores Totais por UF do Cliente - Setembro',
                            labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': soma_valores_setembro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})
        col4.plotly_chart(fig4_setembro, use_container_width=False)

        # Seção 5: Participação dos Clientes no Faturamento Total
        faturamento_total_setembro = df_sem_duplicatas_setembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_setembro['Participacao'] = faturamento_total_setembro['Valor da Nota'] / faturamento_total_setembro['Valor da Nota'].sum() * 100
        fig5_setembro = px.pie(faturamento_total_setembro, names='Cliente', values='Valor da Nota',
                            title='Participação dos Clientes no Faturamento Total - Setembro',
                            hover_name='Cliente', hover_data=['Valor da Nota'],
                            labels={'Valor da Nota': 'Faturamento'})
        fig5_setembro.update_traces(textposition='inside', textinfo='percent+label')
        col5.plotly_chart(fig5_setembro, use_container_width=False)

# Seção específica para 'Outubro'
elif add_selectbox == 'Outubro':
    # Código específico para o mês de Outubro
    df_outubro = df[df['Data de Emissão'].dt.month == 10]
    df_sem_duplicatas_outubro = df_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    with st.container(border=True):
        fat_mes = df_sem_duplicatas_outubro['Valor da Nota'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)
        col1.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:50px;">Faturamento Outubro: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        # Seção 1: Histograma dos Valores das Notas Fiscais
        filtered_value = df_sem_duplicatas_outubro[df_sem_duplicatas_outubro['Valor da Nota'] < 10000]
        fig1_outubro = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais - Outubro',
                                  labels={'Valor da Nota': 'Valores das Notas'})
        col2.plotly_chart(fig1_outubro, use_container_width=True)
        
        # Seção 3: Distribuição de Notas Fiscais por UF do Cliente
        df_sem_duplicatas_outubro = df_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fig3_outubro = px.bar(df_sem_duplicatas_outubro, x='UF do Cliente',
                            title='Distribuição de Notas Fiscais por UF do Cliente - Outubro',
                            labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': df_sem_duplicatas_outubro['UF do Cliente'].value_counts().index})
        col3.plotly_chart(fig3_outubro)

        # Seção 4: Comparação de Valores Totais por UF do Cliente
        df_sem_duplicatas_outubro = df_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_outubro = df_sem_duplicatas_outubro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_outubro = px.bar(soma_valores_outubro, x='UF do Cliente', y='Valor da Nota',
                            title='Comparação de Valores Totais por UF do Cliente - Outubro',
                            labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': soma_valores_outubro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})
        col4.plotly_chart(fig4_outubro, use_container_width=False)

        # Seção 5: Participação dos Clientes no Faturamento Total
        faturamento_total_outubro = df_sem_duplicatas_outubro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_outubro['Participacao'] = faturamento_total_outubro['Valor da Nota'] / faturamento_total_outubro['Valor da Nota'].sum() * 100
        fig5_outubro = px.pie(faturamento_total_outubro, names='Cliente', values='Valor da Nota',
                            title='Participação dos Clientes no Faturamento Total - Outubro',
                            hover_name='Cliente', hover_data=['Valor da Nota'],
                            labels={'Valor da Nota': 'Faturamento'})
        fig5_outubro.update_traces(textposition='inside', textinfo='percent+label')
        col5.plotly_chart(fig5_outubro, use_container_width=False)

# Seção específica para 'Novembro'
elif add_selectbox == 'Novembro':
    # Código específico para o mês de Novembro
    df_novembro = df[df['Data de Emissão'].dt.month == 11]
    df_sem_duplicatas_novembro = df_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    with st.container(border=True):
        fat_mes = df_sem_duplicatas_novembro['Valor da Nota'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_mes_formatado = locale.currency(fat_mes, grouping=True)
        col1.markdown(f'<p style="font-size:40px; text-align:center; margin-top:150px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:50px;">Faturamento Novembro: {fat_mes_formatado}</p>', unsafe_allow_html=True)
        # Seção 1: Histograma dos Valores das Notas Fiscais
        filtered_value = df_sem_duplicatas_novembro[df_sem_duplicatas_novembro['Valor da Nota'] < 10000]
        fig1_novembro = px.histogram(filtered_value, x='Valor da Nota', title='Distribuição dos Valores das Notas Fiscais - Novembro',
                                  labels={'Valor da Nota': 'Valores das Notas'})
        col2.plotly_chart(fig1_novembro, use_container_width=True)
        
        # Seção 3: Distribuição de Notas Fiscais por UF do Cliente
        df_sem_duplicatas_novembro = df_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        fig3_novembro = px.bar(df_sem_duplicatas_novembro, x='UF do Cliente',
                            title='Distribuição de Notas Fiscais por UF do Cliente - Novembro',
                            labels={'count': 'Número de Notas Fiscais', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': df_sem_duplicatas_novembro['UF do Cliente'].value_counts().index})
        col3.plotly_chart(fig3_novembro)

        # Seção 4: Comparação de Valores Totais por UF do Cliente
        df_sem_duplicatas_novembro = df_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_novembro = df_sem_duplicatas_novembro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_novembro = px.bar(soma_valores_novembro, x='UF do Cliente', y='Valor da Nota',
                            title='Comparação de Valores Totais por UF do Cliente - Novembro',
                            labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                            category_orders={'UF do Cliente': soma_valores_novembro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']})
        col4.plotly_chart(fig4_novembro, use_container_width=False)

        # Seção 5: Participação dos Clientes no Faturamento Total
        faturamento_total_novembro = df_sem_duplicatas_novembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_novembro['Participacao'] = faturamento_total_novembro['Valor da Nota'] / faturamento_total_novembro['Valor da Nota'].sum() * 100
        fig5_novembro = px.pie(faturamento_total_novembro, names='Cliente', values='Valor da Nota',
                            title='Participação dos Clientes no Faturamento Total - Novembro',
                            hover_name='Cliente', hover_data=['Valor da Nota'],
                            labels={'Valor da Nota': 'Faturamento'})
        fig5_novembro.update_traces(textposition='inside', textinfo='percent+label')
        col5.plotly_chart(fig5_novembro, use_container_width=False)

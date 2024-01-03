import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import streamlit as st  


df_importation = pd.read_csv('dados_notas.csv', sep=',', decimal=',')

df_usable = df_importation

situacao = ['Substituida', 'Cancelada', 'Canceladas']
df_usable.drop(df_usable[df_usable['Situacao'].isin(situacao)].index, inplace=True)
# Tratamento inicial
if 'Situacao' in df_importation.columns:
    situacao = ['Substituida', 'Cancelada', 'Canceladas']
    df_importation.drop(df_importation[df_importation['Situacao'].isin(situacao)].index, inplace=True)
else:
    st.warning("A coluna 'Situacao' não foi encontrada no DataFrame.")

prestadores_excluir = ['OFFICIUM COWORKING E SERVICOS DE ESCRITORIO LTDA', 'ATTENZA CONSULTORIA CONTABIL LTDA']
df_usable.drop(df_usable[df_usable['Prestador'].isin(prestadores_excluir)].index, inplace=True)

tomadores_excluir = 'MOBSERVICE INOVACAO E TECNOLOGIA EM LOGISTICA LTDA'
df_usable.drop(df_usable[df_usable['Cliente'] == tomadores_excluir].index, inplace=True)

df_usable['Cliente'] = df_usable['Cliente'].replace({
    'TRANSPORTE LUFT LTDA': 'TRANSPORTES LUFT LTDA',
    'TRANSPORTES LUFT LTDA': 'TRANSPORTES LUFT LTDA'
})

df_usable['Data de Emissao'] = pd.to_datetime(df_usable['Data de Emissao'], format='%d/%m/%Y')
df_usable['Mes_ano'] = df_usable['Data de Emissao'].dt.to_period('M')


#Definindo configurações da página
st.set_page_config(
    page_title="Dashboard Controladoria - Chappa",
    page_icon='logo_chappa.png',
    layout='wide',
    initial_sidebar_state='expanded',
    )

with st.sidebar:
    st.image('logo_chapa_brasil.png')
    with st.spinner("Carregando..."):
        time.sleep(0.7)
        add_selectbox = st.selectbox("O quê desejas consultar?", 
                     ("Infos 2023", "Dezembro", "Novembro", "Outubro", "Setembro", "Agosto", "Julho", "Junho",
                      "Maio", "Abril", "Março", "Fevereiro", "Janeiro",
                      "Participação Clientes", "Crescimento Clientes", "Acompanhar Carteira de Clientes"))
        def abrir_radio():
            with st.sidebar:
                add_radio = st.radio(
                        "Clientes",
                        ('G2L LOGISTICA LTDA', 
                        'SILVESTRIN FRUTAS LTDA', 
                        'TOMASI LOGISTICA LTDA', 
                        'RODOVIARIO BEDIN LIMITADA',
                        'SUED EMPREENDIMENTOS E AGRO-NEGOCIOS LTDA',
                        'TRANSPORTES SILVEIRA GOMES LTDA',
                        'TRANSPORTES LUFT LTDA',
                        'PATRUS TRANSPORTES LTDA',
                        'Transpanorama Transportes',
                        'TRANSPORTES MARVEL S.A.',
                        'COOPERATIVA SANTA CLARA LTDA')
                    )
            return add_radio
        
        def abrir_radio_meses():
            with st.sidebar:
                add_radio = st.radio(
                    'Meses',
                    ('Janeiro',
                     'Fevereiro',
                     'Março',
                     'Abril',
                     'Maio',
                     'Junho',
                     'Julho',
                     'Agosto',
                     'Setembro',
                     'Outubro',
                     'Novembro',
                     'Dezembro')
                )
            return add_radio
        
if st.header('Dashboard - Controladoria Fiscal'):
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)


if add_selectbox == 'Infos 2023':
    col11, col21, col31 = st.columns(3)
    col41, col51, col61 = st.columns(3)
    with st.container(border=True):
        fat_GMV = df_usable['Valor Total'].sum()
        
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado = "R${:,.2f}".format(fat_GMV)

        col11.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado}</p>', unsafe_allow_html=True)

# =======================================================================
       
        df_receita = df_usable

        df_receita = df_receita[df_receita['Tributavel'] == 'S']
        fat_RECEITA = df_receita['Valor para Receita'].sum()

        # Formatação do valor usando a formatação de moeda
        receita_formatado = "R${:,.2f}".format(fat_RECEITA)

        col21.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado}</p>', unsafe_allow_html=True)
        
# =======================================================================

        quant_clientes = df_usable['Cliente'].nunique()

        col31.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)

# ======================================================================    
   
        df_usable['Data de Emissao'] = df_usable['Data de Emissao'].dt.strftime('%m')
        meses_ordenados = ['01','02','03','04','05','06','07','08','09','10','11','12']  # Defina a ordem desejada
        df_usable['Data de Emissao'] = pd.Categorical(df_usable['Data de Emissao'], categories=meses_ordenados, ordered=True)
        count_by_month = df_usable.groupby('Data de Emissao')['ID Nota Fiscal'].count().reset_index()

        # Criar o gráfico de linha com chuveirinho
        fig2 = px.line(count_by_month, x='Data de Emissao', y='ID Nota Fiscal', title='Distribuição de Notas Fiscais ao Longo do Tempo',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Data de Emissao': 'Mês'},
                    markers=True, line_shape='linear', template='plotly_dark', # Adicionei template para um layout escuro
                    hover_name='ID Nota Fiscal', hover_data={'Data de Emissao': False, 'ID Nota Fiscal': True}) # Adicionei hover data para exibir informações
        
        # Configurar chuveirinho (área sombreada)
        fig2.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))


        # Atualizar o layout para ocultar as linhas de grade do fundo
        fig2.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )


        # Mostrar o gráfico interativo
        col41.plotly_chart(fig2, use_container_width=True)
        
#         =======================================================================

        # Calcular a soma dos valores agrupados por 'UF do Cliente'
        df_sem_duplicatas = df_usable.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores = df_sem_duplicatas.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col51.plotly_chart(fig4, use_container_width=False)
        
#         =======================================================================
        
        df_sem_duplicatas = df_usable.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total = df_sem_duplicatas.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        # Calcular a participação em porcentagem de cada cliente no faturamento total
        faturamento_total['Participacao'] = faturamento_total['Valor da Nota'] / faturamento_total['Valor da Nota'].sum() * 100
        # Criar um gráfico de pizza interativo com Plotly Express
        fig5 = px.pie(faturamento_total, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no GMV',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        # Adicionar rótulo de porcentagem na parte externa do gráfico
        fig5.update_traces(textposition='inside', textinfo='percent+label')
        # Exibir o gráfico
        col61.plotly_chart(fig5, use_container_width=False)

# Seção específica para 'Janeiro'
if add_selectbox == 'Janeiro':
    df_usable_janeiro = df_usable[df_usable['Mes_ano'] == '2023-01']
    
    with st.container(border=True): 
        fat_GMV_janeiro = df_usable_janeiro['Valor Total'].sum()
        fat_GMV_formatado_janeiro = "R${:,.2f}".format(fat_GMV_janeiro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_janeiro}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_janeiro = df_usable_janeiro[df_usable_janeiro['Tributavel'] == 'S']
        fat_RECEITA_janeiro = df_receita_janeiro['Valor para Receita'].sum()
        receita_formatado_janeiro = "R${:,.2f}".format(fat_RECEITA_janeiro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_janeiro}</p>', unsafe_allow_html=True)

    quant_clientes_janeiro = df_usable_janeiro['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_janeiro}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_janeiro['Data de Emissao'] = pd.to_datetime(df_usable_janeiro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_janeiro['Dia do Mês'] = df_usable_janeiro['Data de Emissao'].dt.day
        count_by_day_janeiro = df_usable_janeiro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_janeiro = px.line(count_by_day_janeiro, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Janeiro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_janeiro.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_janeiro.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_janeiro, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_janeiro = df_usable_janeiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_janeiro = df_sem_duplicatas_janeiro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_janeiro = px.bar(soma_valores_janeiro, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Janeiro',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_janeiro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_janeiro, use_container_width=False)

    with st.container(border=True):    
        df_janeiro = df_usable[df_usable['Mes_ano'] == '2023-01']
        df_sem_duplicatas_janeiro = df_janeiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_janeiro = df_sem_duplicatas_janeiro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_janeiro['Participacao'] = faturamento_total_janeiro['Valor da Nota'] / faturamento_total_janeiro['Valor da Nota'].sum() * 100
        fig5_janeiro = px.pie(faturamento_total_janeiro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Janeiro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_janeiro.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_janeiro, use_container_width=False)

# Seção específica para 'Fevereiro'
if add_selectbox == 'Fevereiro':
    df_usable_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
    
    with st.container(border=True): 
        fat_GMV_fevereiro = df_usable_fevereiro['Valor Total'].sum()
        fat_GMV_formatado_fevereiro = "R${:,.2f}".format(fat_GMV_fevereiro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_fevereiro}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_fevereiro = df_usable_fevereiro[df_usable_fevereiro['Tributavel'] == 'S']
        fat_RECEITA_fevereiro = df_receita_fevereiro['Valor para Receita'].sum()
        receita_formatado_fevereiro = "R${:,.2f}".format(fat_RECEITA_fevereiro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_fevereiro}</p>', unsafe_allow_html=True)

    quant_clientes_fevereiro = df_usable_fevereiro['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_fevereiro}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_fevereiro['Data de Emissao'] = pd.to_datetime(df_usable_fevereiro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_fevereiro['Dia do Mês'] = df_usable_fevereiro['Data de Emissao'].dt.day
        count_by_day_fevereiro = df_usable_fevereiro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_fevereiro = px.line(count_by_day_fevereiro, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Fevereiro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_fevereiro.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_fevereiro.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_fevereiro, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_fevereiro = df_usable_fevereiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_fevereiro = df_sem_duplicatas_fevereiro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_fevereiro = px.bar(soma_valores_fevereiro, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Fevereiro',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_fevereiro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_fevereiro, use_container_width=False)

    with st.container(border=True):    
        df_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
        df_sem_duplicatas_fevereiro = df_fevereiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_fevereiro = df_sem_duplicatas_fevereiro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_fevereiro['Participacao'] = faturamento_total_fevereiro['Valor da Nota'] / faturamento_total_fevereiro['Valor da Nota'].sum() * 100
        fig5_fevereiro = px.pie(faturamento_total_fevereiro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Fevereiro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_fevereiro.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_fevereiro, use_container_width=False)

# Seção específica para 'Março'
if add_selectbox == 'Março':
    df_usable_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
    
    with st.container(border=True): 
        fat_GMV_marco = df_usable_marco['Valor Total'].sum()
        fat_GMV_formatado_marco = "R${:,.2f}".format(fat_GMV_marco)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_marco}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_marco = df_usable_marco[df_usable_marco['Tributavel'] == 'S']
        fat_RECEITA_marco = df_receita_marco['Valor para Receita'].sum()
        receita_formatado_marco = "R${:,.2f}".format(fat_RECEITA_marco)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_marco}</p>', unsafe_allow_html=True)

    quant_clientes_marco = df_usable_marco['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_marco}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_marco['Data de Emissao'] = pd.to_datetime(df_usable_marco['Data de Emissao'], format='%d/%m/%Y')
        df_usable_marco['Dia do Mês'] = df_usable_marco['Data de Emissao'].dt.day
        count_by_day_marco = df_usable_marco.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_marco = px.line(count_by_day_marco, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Março',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_marco.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_marco.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_marco, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_marco = df_usable_marco.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_marco = df_sem_duplicatas_marco.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_marco = px.bar(soma_valores_marco, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Março',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_marco.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_marco, use_container_width=False)

    with st.container(border=True):    
        df_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
        df_sem_duplicatas_marco = df_marco.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_marco = df_sem_duplicatas_marco.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_marco['Participacao'] = faturamento_total_marco['Valor da Nota'] / faturamento_total_marco['Valor da Nota'].sum() * 100
        fig5_marco = px.pie(faturamento_total_marco, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Março)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_marco.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_marco, use_container_width=False)

# Seção específica para 'Abril'
if add_selectbox == 'Abril':
    df_usable_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
    
    with st.container(border=True): 
        fat_GMV_abril = df_usable_abril['Valor Total'].sum()
        fat_GMV_formatado_abril = "R${:,.2f}".format(fat_GMV_abril)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_abril}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_abril = df_usable_abril[df_usable_abril['Tributavel'] == 'S']
        fat_RECEITA_abril = df_receita_abril['Valor para Receita'].sum()
        receita_formatado_abril = "R${:,.2f}".format(fat_RECEITA_abril)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_abril}</p>', unsafe_allow_html=True)

    quant_clientes_abril = df_usable_abril['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_abril}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_abril['Data de Emissao'] = pd.to_datetime(df_usable_abril['Data de Emissao'], format='%d/%m/%Y')
        df_usable_abril['Dia do Mês'] = df_usable_abril['Data de Emissao'].dt.day
        count_by_day_abril = df_usable_abril.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_abril = px.line(count_by_day_abril, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Abril',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_abril.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_abril.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_abril, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_abril = df_usable_abril.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_abril = df_sem_duplicatas_abril.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_abril = px.bar(soma_valores_abril, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Abril',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_abril.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_abril, use_container_width=False)

    with st.container(border=True):    
        df_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
        df_sem_duplicatas_abril = df_abril.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_abril = df_sem_duplicatas_abril.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_abril['Participacao'] = faturamento_total_abril['Valor da Nota'] / faturamento_total_abril['Valor da Nota'].sum() * 100
        fig5_abril = px.pie(faturamento_total_abril, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Abril)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_abril.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_abril, use_container_width=False)

# Seção específica para 'Maio'
if add_selectbox == 'Maio':
    df_usable_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
    
    with st.container(border=True): 
        fat_GMV_maio = df_usable_maio['Valor Total'].sum()
        fat_GMV_formatado_maio = "R${:,.2f}".format(fat_GMV_maio)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_maio}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_maio = df_usable_maio[df_usable_maio['Tributavel'] == 'S']
        fat_RECEITA_maio = df_receita_maio['Valor para Receita'].sum()
        receita_formatado_maio = "R${:,.2f}".format(fat_RECEITA_maio)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_maio}</p>', unsafe_allow_html=True)

    quant_clientes_maio = df_usable_maio['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_maio}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_maio['Data de Emissao'] = pd.to_datetime(df_usable_maio['Data de Emissao'], format='%d/%m/%Y')
        df_usable_maio['Dia do Mês'] = df_usable_maio['Data de Emissao'].dt.day
        count_by_day_maio = df_usable_maio.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_maio = px.line(count_by_day_maio, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Maio',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_maio.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_maio.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_maio, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_maio = df_usable_maio.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_maio = df_sem_duplicatas_maio.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_maio = px.bar(soma_valores_maio, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Maio',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_maio.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_maio, use_container_width=False)

    with st.container(border=True):    
        df_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
        df_sem_duplicatas_maio = df_maio.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_maio = df_sem_duplicatas_maio.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_maio['Participacao'] = faturamento_total_maio['Valor da Nota'] / faturamento_total_maio['Valor da Nota'].sum() * 100
        fig5_maio = px.pie(faturamento_total_maio, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Maio)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_maio.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_maio, use_container_width=False)

# Seção específica para 'Junho'
if add_selectbox == 'Junho':
    df_usable_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
    
    with st.container(border=True): 
        fat_GMV_junho = df_usable_junho['Valor Total'].sum()
        fat_GMV_formatado_junho = "R${:,.2f}".format(fat_GMV_junho)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_junho}</p>', unsafe_allow_html=True)

    with st.container(border=True):    
        df_receita_junho = df_usable_junho[df_usable_junho['Tributavel'] == 'S']
        fat_RECEITA_junho = df_receita_junho['Valor para Receita'].sum()
        receita_formatado_junho = "R${:,.2f}".format(fat_RECEITA_junho)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_junho}</p>', unsafe_allow_html=True)

    quant_clientes_junho = df_usable_junho['Cliente'].nunique()
    col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes_junho}</p>', unsafe_allow_html=True)
    with st.container(border=True):    
        df_usable_junho['Data de Emissao'] = pd.to_datetime(df_usable_junho['Data de Emissao'], format='%d/%m/%Y')
        df_usable_junho['Dia do Mês'] = df_usable_junho['Data de Emissao'].dt.day
        count_by_day_junho = df_usable_junho.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig_junho = px.line(count_by_day_junho, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Junho',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig_junho.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig_junho.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig_junho, use_container_width=True)     

    with st.container(border=True):    
        df_sem_duplicatas_junho = df_usable_junho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_junho = df_sem_duplicatas_junho.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4_junho = px.bar(soma_valores_junho, x='UF do Cliente', y='Valor da Nota',
                title='Comparação de Valores Totais das Notas por UF do Cliente em Junho',
                labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
                category_orders={'UF do Cliente': soma_valores_junho.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4_junho, use_container_width=False)

    with st.container(border=True):    
        df_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
        df_sem_duplicatas_junho = df_junho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_junho = df_sem_duplicatas_junho.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_junho['Participacao'] = faturamento_total_junho['Valor da Nota'] / faturamento_total_junho['Valor da Nota'].sum() * 100
        fig5_junho = px.pie(faturamento_total_junho, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Junho)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5_junho.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5_junho, use_container_width=False)
    
# Seção específica para 'Julho'        
if add_selectbox == 'Julho':
    # Código específico para o mês de julho
    df_usable_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_julho = df_usable_julho['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_julho = "R${:,.2f}".format(fat_GMV_julho)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_julho}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_julho = df_usable_julho[df_usable_julho['Tributavel'] == 'S']
        fat_RECEITA_julho = df_receita_julho['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_julho = "R${:,.2f}".format(fat_RECEITA_julho)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_julho}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_julho['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_julho['Data de Emissao'] = pd.to_datetime(df_usable_julho['Data de Emissao'], format='%d/%m/%Y')
        df_usable_julho['Dia do Mês'] = df_usable_julho['Data de Emissao'].dt.day
        count_by_day = df_usable_julho.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Julho',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_julho = df_usable_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_julho = df_sem_duplicatas_julho.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_julho, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_julho.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)
        
        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
        df_sem_duplicatas_julho = df_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_julho = df_sem_duplicatas_julho.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_julho['Participacao'] = faturamento_total_julho['Valor da Nota'] / faturamento_total_julho['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_julho, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Julho)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)

# Seção específica para 'Agosto'
if add_selectbox == 'Agosto':
    # Código específico para o mês de julho
    df_usable_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_agosto = df_usable_agosto['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_agosto = "R${:,.2f}".format(fat_GMV_agosto)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_agosto}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_agosto = df_usable_agosto[df_usable_agosto['Tributavel'] == 'S']
        fat_RECEITA_agosto = df_receita_agosto['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_agosto = "R${:,.2f}".format(fat_RECEITA_agosto)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_agosto}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_agosto['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_agosto['Data de Emissao'] = pd.to_datetime(df_usable_agosto['Data de Emissao'], format='%d/%m/%Y')
        df_usable_agosto['Dia do Mês'] = df_usable_agosto['Data de Emissao'].dt.day
        count_by_day = df_usable_agosto.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Agosto',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_agosto = df_usable_agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_agosto = df_sem_duplicatas_agosto.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_agosto, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_agosto.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
        df_sem_duplicatas_agosto = df_agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_agosto = df_sem_duplicatas_agosto.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_agosto['Participacao'] = faturamento_total_agosto['Valor da Nota'] / faturamento_total_agosto['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_agosto, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Agosto)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)
                
# Seção específica para 'Setembro'
if add_selectbox == 'Setembro':
    # Código específico para o mês de julho
    df_usable_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_setembro = df_usable_setembro['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_setembro = "R${:,.2f}".format(fat_GMV_setembro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_setembro}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_setembro = df_usable_setembro[df_usable_setembro['Tributavel'] == 'S']
        fat_RECEITA_setembro = df_receita_setembro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_setembro = "R${:,.2f}".format(fat_RECEITA_setembro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_setembro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_setembro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_setembro['Data de Emissao'] = pd.to_datetime(df_usable_setembro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_setembro['Dia do Mês'] = df_usable_setembro['Data de Emissao'].dt.day
        count_by_day = df_usable_setembro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Setembro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_setembro = df_usable_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_setembro = df_sem_duplicatas_setembro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_setembro, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_setembro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
        df_sem_duplicatas_setembro = df_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_setembro = df_sem_duplicatas_setembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_setembro['Participacao'] = faturamento_total_setembro['Valor da Nota'] / faturamento_total_setembro['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_setembro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Setembro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)

# Seção específica para 'Outubro'
if add_selectbox == 'Outubro':
    df_usable_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_outubro = df_usable_outubro['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_outubro = "R${:,.2f}".format(fat_GMV_outubro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_outubro}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_outubro = df_usable_outubro[df_usable_outubro['Tributavel'] == 'S']
        fat_RECEITA_outubro = df_receita_outubro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_outubro = "R${:,.2f}".format(fat_RECEITA_outubro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_outubro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_outubro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_outubro['Data de Emissao'] = pd.to_datetime(df_usable_outubro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_outubro['Dia do Mês'] = df_usable_outubro['Data de Emissao'].dt.day
        count_by_day = df_usable_outubro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Outubro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_outubro = df_usable_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_outubro = df_sem_duplicatas_outubro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_outubro, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_outubro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
        df_sem_duplicatas_outubro = df_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_outubro = df_sem_duplicatas_outubro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_outubro['Participacao'] = faturamento_total_outubro['Valor da Nota'] / faturamento_total_outubro['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_outubro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Outubro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)

# Seção específica para 'Novembro'
if add_selectbox == 'Novembro':
    df_usable_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_novembro = df_usable_novembro['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_novembro = "R${:,.2f}".format(fat_GMV_novembro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_novembro}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_novembro = df_usable_novembro[df_usable_novembro['Tributavel'] == 'S']
        fat_RECEITA_novembro = df_receita_novembro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_novembro = "R${:,.2f}".format(fat_RECEITA_novembro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_novembro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_novembro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_novembro['Data de Emissao'] = pd.to_datetime(df_usable_novembro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_novembro['Dia do Mês'] = df_usable_novembro['Data de Emissao'].dt.day
        count_by_day = df_usable_novembro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Outubro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_novembro = df_usable_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_novembro = df_sem_duplicatas_novembro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_novembro, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_novembro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
        df_sem_duplicatas_novembro = df_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_novembro = df_sem_duplicatas_novembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_novembro['Participacao'] = faturamento_total_novembro['Valor da Nota'] / faturamento_total_novembro['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_novembro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Novembro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)

# Seção específica para 'Novembro'
if add_selectbox == 'Dezembro':
    df_usable_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
    
# ==============================================================

    with st.container(border=True): 
        fat_GMV_dezembro = df_usable_dezembro['Valor Total'].sum()
        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado_dezembro = "R${:,.2f}".format(fat_GMV_dezembro)
        col1.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado_dezembro}</p>', unsafe_allow_html=True)
 
# ==============================================================   

    with st.container(border=True):    
        df_receita_dezembro = df_usable_dezembro[df_usable_dezembro['Tributavel'] == 'S']
        fat_RECEITA_dezembro = df_receita_dezembro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_dezembro = "R${:,.2f}".format(fat_RECEITA_dezembro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_dezembro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_dezembro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_dezembro['Data de Emissao'] = pd.to_datetime(df_usable_dezembro['Data de Emissao'], format='%d/%m/%Y')
        df_usable_dezembro['Dia do Mês'] = df_usable_dezembro['Data de Emissao'].dt.day
        count_by_day = df_usable_dezembro.groupby('Dia do Mês')['ID Nota Fiscal'].count().reset_index()
        fig = px.line(count_by_day, x='Dia do Mês', y='ID Nota Fiscal', title='Quantidade de Notas Fiscais por Dia em Outubro',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Dia do Mês': 'Dia do Mês'},
                    markers=True, line_shape='linear', template='plotly_dark',
                    hover_name='ID Nota Fiscal', hover_data={'Dia do Mês': True, 'ID Nota Fiscal': True})
        fig.update_traces(fill='tozeroy', fillcolor='rgba(95,158,160,0.6)', line=dict(color='rgba(128,128,128,1.0)'))
        fig.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True)
        )
        col4.plotly_chart(fig, use_container_width=True)     

# ==============================================================

        df_sem_duplicatas_dezembro = df_usable_dezembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        soma_valores_dezembro = df_sem_duplicatas_dezembro.groupby('UF do Cliente')['Valor da Nota'].sum().reset_index()
        fig4 = px.bar(soma_valores_dezembro, x='UF do Cliente', y='Valor da Nota',
              title='Comparação de Valores Totais das Notas por UF do Cliente',
              labels={'Valor da Nota': 'Valor Total', 'UF do Cliente': 'UF do Cliente'},
              category_orders={'UF do Cliente': soma_valores_dezembro.sort_values('Valor da Nota', ascending=False)['UF do Cliente']},
              template='plotly_dark',
              color_discrete_sequence=px.colors.qualitative.T10)

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
        df_sem_duplicatas_dezembro = df_dezembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        faturamento_total_dezembro = df_sem_duplicatas_dezembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
        faturamento_total_dezembro['Participacao'] = faturamento_total_dezembro['Valor da Nota'] / faturamento_total_dezembro['Valor da Nota'].sum() * 100
        fig5 = px.pie(faturamento_total_dezembro, names='Cliente', values='Valor da Nota', 
                    title='Participação dos Clientes no Faturamento Total (Dezembro)',
                    hover_name='Cliente', hover_data=['Valor da Nota'],
                    labels={'Valor da Nota': 'Faturamento'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=.5)
        fig5.update_traces(textposition='inside', textinfo='percent+label')

        col6.plotly_chart(fig5, use_container_width=False)
        
if add_selectbox == 'Participação Clientes':
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11, col12 = st.columns(3)

    # Janeiro
    df_Janeiro = df_usable[df_usable['Mes_ano'] == '2023-01']
    df_sem_duplicatas_Janeiro = df_Janeiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Janeiro = df_sem_duplicatas_Janeiro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Janeiro['Participacao'] = faturamento_total_Janeiro['Valor da Nota'] / faturamento_total_Janeiro['Valor da Nota'].sum() * 100
    fig1 = px.pie(faturamento_total_Janeiro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Janeiro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig1.update_traces(textposition='inside', textinfo='percent+label')

    col1.plotly_chart(fig1, use_container_width=False)  
    
    # Fevereiro
    df_Fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
    df_sem_duplicatas_Fevereiro = df_Fevereiro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Fevereiro = df_sem_duplicatas_Fevereiro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Fevereiro['Participacao'] = faturamento_total_Fevereiro['Valor da Nota'] / faturamento_total_Fevereiro['Valor da Nota'].sum() * 100
    fig2 = px.pie(faturamento_total_Fevereiro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Fevereiro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig2.update_traces(textposition='inside', textinfo='percent+label')

    col2.plotly_chart(fig2, use_container_width=False)  
    
    # Marco
    df_Marco = df_usable[df_usable['Mes_ano'] == '2023-03']
    df_sem_duplicatas_Marco = df_Marco.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Marco = df_sem_duplicatas_Marco.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Marco['Participacao'] = faturamento_total_Marco['Valor da Nota'] / faturamento_total_Marco['Valor da Nota'].sum() * 100
    fig3 = px.pie(faturamento_total_Marco, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Marco)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig3.update_traces(textposition='inside', textinfo='percent+label')

    col3.plotly_chart(fig3, use_container_width=False)  
        
    # Abril
    df_Abril = df_usable[df_usable['Mes_ano'] == '2023-04']
    df_sem_duplicatas_Abril = df_Abril.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Abril = df_sem_duplicatas_Abril.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Abril['Participacao'] = faturamento_total_Abril['Valor da Nota'] / faturamento_total_Abril['Valor da Nota'].sum() * 100
    fig4 = px.pie(faturamento_total_Abril, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Abril)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig4.update_traces(textposition='inside', textinfo='percent+label')

    col4.plotly_chart(fig4, use_container_width=False)  
    
    # Maio
    df_Maio = df_usable[df_usable['Mes_ano'] == '2023-05']
    df_sem_duplicatas_Maio = df_Maio.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Maio = df_sem_duplicatas_Maio.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Maio['Participacao'] = faturamento_total_Maio['Valor da Nota'] / faturamento_total_Maio['Valor da Nota'].sum() * 100
    fig5 = px.pie(faturamento_total_Maio, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Maio)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig5.update_traces(textposition='inside', textinfo='percent+label')

    col5.plotly_chart(fig5, use_container_width=False)   
    
    # Junho
    df_Junho = df_usable[df_usable['Mes_ano'] == '2023-06']
    df_sem_duplicatas_Junho = df_Junho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_Junho = df_sem_duplicatas_Junho.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_Junho['Participacao'] = faturamento_total_Junho['Valor da Nota'] / faturamento_total_Junho['Valor da Nota'].sum() * 100
    fig6 = px.pie(faturamento_total_Junho, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Junho)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig6.update_traces(textposition='inside', textinfo='percent+label')

    col6.plotly_chart(fig6, use_container_width=False)
    
    # Julho
    df_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
    df_sem_duplicatas_julho = df_julho.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_julho = df_sem_duplicatas_julho.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_julho['Participacao'] = faturamento_total_julho['Valor da Nota'] / faturamento_total_julho['Valor da Nota'].sum() * 100
    fig7 = px.pie(faturamento_total_julho, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Julho)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig7.update_traces(textposition='inside', textinfo='percent+label')

    col7.plotly_chart(fig7, use_container_width=False)
    
    # Agosto
    df_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
    df_sem_duplicatas_agosto = df_agosto.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_agosto = df_sem_duplicatas_agosto.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_agosto['Participacao'] = faturamento_total_agosto['Valor da Nota'] / faturamento_total_agosto['Valor da Nota'].sum() * 100
    fig8 = px.pie(faturamento_total_agosto, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Agosto)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig8.update_traces(textposition='inside', textinfo='percent+label')

    col8.plotly_chart(fig8, use_container_width=False)
        
    # Setembro
    df_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
    df_sem_duplicatas_setembro = df_setembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_setembro = df_sem_duplicatas_setembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_setembro['Participacao'] = faturamento_total_setembro['Valor da Nota'] / faturamento_total_setembro['Valor da Nota'].sum() * 100
    fig9 = px.pie(faturamento_total_setembro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Setembro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig9.update_traces(textposition='inside', textinfo='percent+label')

    col9.plotly_chart(fig9, use_container_width=False)
    
    # Outubro
    df_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
    df_sem_duplicatas_outubro = df_outubro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_outubro = df_sem_duplicatas_outubro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_outubro['Participacao'] = faturamento_total_outubro['Valor da Nota'] / faturamento_total_outubro['Valor da Nota'].sum() * 100
    fig10 = px.pie(faturamento_total_outubro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Outubro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig10.update_traces(textposition='inside', textinfo='percent+label')

    col10.plotly_chart(fig10, use_container_width=False)
    
    # Novembro
    df_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
    df_sem_duplicatas_novembro = df_novembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_novembro = df_sem_duplicatas_novembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_novembro['Participacao'] = faturamento_total_novembro['Valor da Nota'] / faturamento_total_novembro['Valor da Nota'].sum() * 100
    fig11 = px.pie(faturamento_total_novembro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Novembro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig11.update_traces(textposition='inside', textinfo='percent+label')

    col11.plotly_chart(fig11, use_container_width=False)

    # Dezembro
    df_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
    df_sem_duplicatas_dezembro = df_dezembro.drop_duplicates(subset='ID Nota Fiscal', keep='first')
    faturamento_total_dezembro = df_sem_duplicatas_dezembro.groupby('Cliente')['Valor da Nota'].sum().reset_index()
    faturamento_total_dezembro['Participacao'] = faturamento_total_dezembro['Valor da Nota'] / faturamento_total_dezembro['Valor da Nota'].sum() * 100
    fig12 = px.pie(faturamento_total_dezembro, names='Cliente', values='Valor da Nota', 
                title='Participação dos Clientes no Faturamento Total (Dezembro)',
                hover_name='Cliente', hover_data=['Valor da Nota'],
                labels={'Valor da Nota': 'Faturamento'},
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=.5)
    fig12.update_traces(textposition='inside', textinfo='percent+label')

    col12.plotly_chart(fig12, use_container_width=False)
        
        
if add_selectbox == 'Crescimento Clientes':
    selecionar = abrir_radio()
    def abreviar_valor(valor):
        if valor >= 1e6:
            return f"{valor / 1e6:.1f}M"
        elif valor >= 1e3:
            return f"{valor / 1e3:.1f}K"
        else:
            return f"{valor:.0f}"

    def criar_graph(selecionar):
        cliente_selecionado = selecionar
        df_sem_duplicatas = df_usable.drop_duplicates(subset='ID Nota Fiscal', keep='first')
        df_cliente_mes = df_sem_duplicatas[df_sem_duplicatas['Cliente'] == cliente_selecionado]
        df_faturamento_mensal = df_cliente_mes.groupby('Mes_ano')['Valor da Nota'].sum().reset_index()
        df_faturamento_mensal['Mes_ano'] = df_faturamento_mensal['Mes_ano'].astype(str)
        # Adicionar coluna com valores abreviados
        df_faturamento_mensal['Valor_abreviado'] = df_faturamento_mensal['Valor da Nota'].apply(abreviar_valor)

        fig = px.bar(df_faturamento_mensal, x='Mes_ano', y='Valor da Nota',
                    text='Valor_abreviado',
                    title=f'Faturamento Mensal para o Cliente {cliente_selecionado}',
                    labels={'Valor da Nota': 'Faturamento', 'Mes_ano': 'Mês e Ano'},
                    template='plotly_dark',
                    color_discrete_sequence=px.colors.qualitative.Set3)

        # Adicionar rótulos com os valores abreviados
        fig.update_traces(texttemplate='%{text}', textposition='outside')

        # Adicionar uma linha que percorre as barras
        linha_tropica = go.Scatter(
            x=df_faturamento_mensal['Mes_ano'],
            y=df_faturamento_mensal['Valor da Nota'],
            mode='lines',
            line=dict(color='gray', width=3),
            name='Linearidade'
        )

        fig.add_trace(linha_tropica)

        fig.update_layout(height=800, width=1200)
        # Exibir o gráfico
        st.plotly_chart(fig, use_container_width=False)
        
    if selecionar == 'G2L LOGISTICA LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'SILVESTRIN FRUTAS LTDA':
        criar_graph(selecionar)
    
    if selecionar == 'TOMASI LOGISTICA LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'RODOVIARIO BEDIN LIMITADA':
        criar_graph(selecionar)
        
    if selecionar == 'SUED EMPREENDIMENTOS E AGRO-NEGOCIOS LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'TRANSPORTES SILVEIRA GOMES LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'TRANSPORTES LUFT LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'PATRUS TRANSPORTES LTDA':
        criar_graph(selecionar)
        
    if selecionar == 'Transpanorama Transportes':
        criar_graph(selecionar)
    
    if selecionar == 'TRANSPORTES MARVEL S.A.':
        criar_graph(selecionar)
        
    if selecionar == 'COOPERATIVA SANTA CLARA LTDA':
        criar_graph(selecionar)

if add_selectbox == 'Acompanhar Carteira de Clientes':
    selecionar = abrir_radio_meses()
    col1, col2, col5 = st.columns(3)
    col6, col7, col10 = st.columns(3)
    col11, col12, col15 = st.columns(3)
    col16, col17, col20 = st.columns(3)
    col51, col52, col53, col54 = st.columns(4)
    col21, col22, col23, col24 = st.columns(4)
    col25, col26, col27, col28 = st.columns(4)    

    if selecionar == 'Janeiro':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_janeiro = df_usable[df_usable['Mes_ano'] == '2023-01']
        df_usable_janeiro = df_usable_janeiro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_janeiro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> Sem Dados</p>', unsafe_allow_html=True)    
        
        # =============================================
        
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> Sem Dados</p>', unsafe_allow_html=True) 
    
    if selecionar == 'Fevereiro':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
        df_usable_fevereiro = df_usable_fevereiro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_fevereiro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_janeiro = df_usable[df_usable['Mes_ano'] == '2023-01']
        df_usable_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
        clientes_nao_retidos = df_usable_janeiro[~df_usable_janeiro['Cliente'].isin(df_usable_fevereiro['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
        quant_cliente_fevereiro = df_usable_fevereiro['Cliente'].nunique()
        quant_clientes_janeiro = df_usable_janeiro['Cliente'].nunique()
        porcentagem = ((quant_cliente_fevereiro - quant_clientes_janeiro) / quant_clientes_janeiro) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
    if selecionar == 'Março':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
        df_usable_marco = df_usable_marco['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_marco}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_fevereiro = df_usable[df_usable['Mes_ano'] == '2023-02']
        df_usable_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
        clientes_nao_retidos = df_usable_fevereiro[~df_usable_fevereiro['Cliente'].isin(df_usable_marco['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
        quant_cliente_marco = df_usable_marco['Cliente'].nunique()
        quant_clientes_fevereiro = df_usable_fevereiro['Cliente'].nunique()
        porcentagem = ((quant_cliente_marco - quant_clientes_fevereiro) / quant_clientes_fevereiro) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
    if selecionar == 'Abril':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
        df_usable_abril = df_usable_abril['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_abril}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_marco = df_usable[df_usable['Mes_ano'] == '2023-03']
        df_usable_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
        clientes_nao_retidos = df_usable_marco[~df_usable_marco['Cliente'].isin(df_usable_abril['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
        quant_cliente_abril = df_usable_abril['Cliente'].nunique()
        quant_clientes_marco = df_usable_marco['Cliente'].nunique()
        porcentagem = ((quant_cliente_abril - quant_clientes_marco) / quant_clientes_marco) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
    if selecionar == 'Maio':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
        df_usable_maio = df_usable_maio['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_maio}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_abril = df_usable[df_usable['Mes_ano'] == '2023-04']
        df_usable_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
        clientes_nao_retidos = df_usable_abril[~df_usable_abril['Cliente'].isin(df_usable_maio['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
        quant_cliente_maio = df_usable_maio['Cliente'].nunique()
        quant_clientes_abril = df_usable_abril['Cliente'].nunique()
        porcentagem = ((quant_cliente_maio - quant_clientes_abril) / quant_clientes_abril) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
        
    if selecionar == 'Junho':
        
        # =============================================   
        
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
        df_usable_junho = df_usable_junho['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_junho}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_maio = df_usable[df_usable['Mes_ano'] == '2023-05']
        df_usable_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
        clientes_nao_retidos = df_usable_maio[~df_usable_maio['Cliente'].isin(df_usable_junho['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
        quant_cliente_junho = df_usable_junho['Cliente'].nunique()
        quant_clientes_maio = df_usable_maio['Cliente'].nunique()
        porcentagem = ((quant_cliente_junho - quant_clientes_maio) / quant_clientes_maio) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
        
    if selecionar == 'Julho':
        
        # =============================================   
            
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
        df_usable_julho = df_usable_julho['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_julho}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_junho = df_usable[df_usable['Mes_ano'] == '2023-06']
        df_usable_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
        clientes_nao_retidos = df_usable_junho[~df_usable_junho['Cliente'].isin(df_usable_julho['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
        quant_cliente_julho = df_usable_julho['Cliente'].nunique()
        quant_clientes_junho = df_usable_junho['Cliente'].nunique()
        porcentagem = ((quant_cliente_julho - quant_clientes_junho) / quant_clientes_junho) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)   
        
    if selecionar == 'Agosto':
  
        # =============================================   
             
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)


        # ============================================
        
        df_usable_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
        df_usable_agosto = df_usable_agosto['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_agosto}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_julho = df_usable[df_usable['Mes_ano'] == '2023-07']
        df_usable_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
        clientes_nao_retidos = df_usable_julho[~df_usable_julho['Cliente'].isin(df_usable_agosto['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
        quant_cliente_agosto = df_usable_agosto['Cliente'].nunique()
        quant_clientes_julho = df_usable_julho['Cliente'].nunique()
        porcentagem = ((quant_cliente_agosto - quant_clientes_julho) / quant_clientes_julho) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
               
    if selecionar == 'Setembro':
  
        # =============================================   
             
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)

        # ============================================
        
        df_usable_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
        df_usable_setembro = df_usable_setembro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_setembro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_agosto = df_usable[df_usable['Mes_ano'] == '2023-08']
        df_usable_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
        clientes_nao_retidos = df_usable_agosto[~df_usable_agosto['Cliente'].isin(df_usable_setembro['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
        quant_cliente_setembro = df_usable_setembro['Cliente'].nunique()
        quant_clientes_agosto = df_usable_agosto['Cliente'].nunique()
        porcentagem = ((quant_cliente_setembro - quant_clientes_agosto) / quant_clientes_agosto) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True) 
    
    if selecionar == 'Outubro':
  
        # =============================================   
             
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)

        # ============================================
        
        df_usable_outubro = df_usable[df_usable['Mes_ano'] == '2023-11']
        df_usable_outubro = df_usable_outubro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_outubro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_setembro = df_usable[df_usable['Mes_ano'] == '2023-09']
        df_usable_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
        clientes_nao_retidos = df_usable_setembro[~df_usable_setembro['Cliente'].isin(df_usable_outubro['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
        quant_cliente_outubro = df_usable_outubro['Cliente'].nunique()
        quant_clientes_setembro = df_usable_setembro['Cliente'].nunique()
        porcentagem = ((quant_cliente_outubro - quant_clientes_setembro) / quant_clientes_setembro) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
        
    if selecionar == 'Novembro':
  
        # =============================================   
             
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)

        # ============================================
        
        df_usable_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
        df_usable_novembro = df_usable_novembro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_novembro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
        df_usable_outubro = df_usable[df_usable['Mes_ano'] == '2023-10']
        clientes_nao_retidos = df_usable_outubro[~df_usable_outubro['Cliente'].isin(df_usable_novembro['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
        quant_cliente_novembro = df_usable_novembro['Cliente'].nunique()
        quant_clientes_outubro = df_usable_outubro['Cliente'].nunique()
        porcentagem = ((quant_cliente_novembro - quant_clientes_outubro) / quant_clientes_outubro) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)
        
    if selecionar == 'Dezembro':
  
        # =============================================   
             
        quant_clientes = df_usable['Cliente'].nunique()
        col1.subheader(f"Número total de clientes até Dezembro:")
        col6.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {quant_clientes}</p>', unsafe_allow_html=True)
        
        # =============================================  
        
        col51.divider()
        col52.divider()
        col53.divider()  
        col54.divider()   
        df_contagem_clientes = df_usable.groupby('Mes_ano')['Cliente'].nunique().reset_index()
        df_contagem_clientes = df_contagem_clientes.sort_values('Mes_ano')
        df_contagem_clientes['Mes_ano'] = pd.to_datetime(df_contagem_clientes['Mes_ano'].dt.to_timestamp())
        col22.subheader("Clientes por Mês:")
        fig = px.bar(df_contagem_clientes, x='Mes_ano', y='Cliente',
                    labels={'Cliente': 'Quantidade de Clientes', 'Mes_ano' : 'Mês e Ano'},
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    text='Cliente',  # Adicionando o texto acima de cada barra
                    height=480)
        fig.update_traces(texttemplate='%{text}', textposition='inside')
        col26.plotly_chart(fig)

        # ============================================
        
        df_usable_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
        df_usable_dezembro = df_usable_dezembro['Cliente'].nunique()
        col5.subheader(f"Número de clientes em {selecionar}:")
        col10.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;"> {df_usable_dezembro}</p>', unsafe_allow_html=True)
        
        # =============================================
        
        df_usable_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
        df_usable_novembro = df_usable[df_usable['Mes_ano'] == '2023-11']
        clientes_nao_retidos = df_usable_novembro[~df_usable_novembro['Cliente'].isin(df_usable_dezembro['Cliente'])]
        clientes_nao_retidos = clientes_nao_retidos[['Cliente']].drop_duplicates()   
        col11.subheader(f"Clientes que estavam no mês anterior, mas não estão mais em {selecionar}:")
        col16.table(data=clientes_nao_retidos)     
        
        # =============================================
        
        df_usable_dezembro = df_usable[df_usable['Mes_ano'] == '2023-12']
        quant_cliente_dezembro = df_usable_dezembro['Cliente'].nunique()
        quant_clientes_novembro = df_usable_novembro['Cliente'].nunique()
        porcentagem = ((quant_cliente_dezembro - quant_clientes_novembro) / quant_clientes_novembro) * 100
        col15.subheader(f"Porcentagem de Crescimento de Clientes em {selecionar}:")
        col20.markdown(f'<p style="font-size:30px; text-align:center; margin-top:5px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:5px; padding:40px;">{porcentagem:,.2f}%</p>', unsafe_allow_html=True)   
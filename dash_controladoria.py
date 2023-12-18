import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import streamlit as st  

df_importation = pd.read_csv('dados_notas.csv', sep=',', decimal=',', encoding='utf-8')

df_usable = df_importation

situacao = ['Substituida', 'Cancelada', 'Canceladas']
df_usable.drop(df_usable[df_usable['Situacao'].isin(situacao)].index, inplace=True)
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

df_usable['Data de Emissão'] = pd.to_datetime(df_usable['Data de Emissão'], format='%d/%m/%Y')
df_usable['Mes_ano'] = df_usable['Data de Emissão'].dt.to_period('M')


#Definindo configurações da página
st.set_page_config(
    page_title="Dashboard Controladoria - Chappa",
    page_icon='logo_chappa.png',
    layout='wide',
    initial_sidebar_state='expanded')


st.markdown(
    """
        <style>
            body {
                color: white;
                background-color: #1E1E1E;
            }
            .st-dg .st-cg .st-ch .st-ci .st-cj .st-cm .st-cn {
                color: white;
            }
        </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.image('logo_chappa_maior.png', use_column_width='PNG')
    with st.spinner("Carregando..."):
        time.sleep(0.7)
        add_selectbox = st.selectbox("O quê desejas consultar?", 
                     ("Últimos 5 meses", "Novembro", "Outubro", "Setembro", "Agosto", "Julho", "Crescimento Clientes"))
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
        
if st.header('Dashboard - Controladoria Fiscal'):
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)


if add_selectbox == 'Últimos 5 meses':
    col11, col21, col31 = st.columns(3)
    col41, col51, col61 = st.columns(3)
    with st.container(border=True):
        fat_GMV = df_usable['Valor Total'].sum()

        # Formatação do valor usando a formatação de moeda
        fat_GMV_formatado = "R${:,.2f}".format(fat_GMV)

        col11.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">GMV: {fat_GMV_formatado}</p>', unsafe_allow_html=True)

# =======================================================================
       
        df_receita = df_usable

        df_receita = df_receita[df_receita['Tributável'] == 'S']
        fat_RECEITA = df_receita['Valor para Receita'].sum()

        # Formatação do valor usando a formatação de moeda
        receita_formatado = "R${:,.2f}".format(fat_RECEITA)

        col21.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado}</p>', unsafe_allow_html=True)
        
# =======================================================================

        quant_clientes = df_usable['Cliente'].nunique()

        col31.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)

# ======================================================================    
   
        df_usable['Data de Emissão'] = df_usable['Data de Emissão'].dt.strftime('%m')
        meses_ordenados = ['07', '08', '09', '10', '11']  # Defina a ordem desejada
        df_usable['Data de Emissão'] = pd.Categorical(df_usable['Data de Emissão'], categories=meses_ordenados, ordered=True)
        count_by_month = df_usable.groupby('Data de Emissão')['ID Nota Fiscal'].count().reset_index()

        # Criar o gráfico de linha com chuveirinho
        fig2 = px.line(count_by_month, x='Data de Emissão', y='ID Nota Fiscal', title='Distribuição de Notas Fiscais ao Longo do Tempo',
                    labels={'ID Nota Fiscal': 'Quantidade de Notas Fiscais', 'Data de Emissão': 'Mês'},
                    markers=True, line_shape='linear', template='plotly_dark', # Adicionei template para um layout escuro
                    hover_name='ID Nota Fiscal', hover_data={'Data de Emissão': False, 'ID Nota Fiscal': True}) # Adicionei hover data para exibir informações
        
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
              template='plotly_dark')

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
        df_receita_julho = df_usable_julho[df_usable_julho['Tributável'] == 'S']
        fat_RECEITA_julho = df_receita_julho['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_julho = "R${:,.2f}".format(fat_RECEITA_julho)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_julho}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_julho['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_julho['Data de Emissão'] = pd.to_datetime(df_usable_julho['Data de Emissão'], format='%d/%m/%Y')
        df_usable_julho['Dia do Mês'] = df_usable_julho['Data de Emissão'].dt.day
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
              template='plotly_dark')
        
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
        df_receita_agosto = df_usable_agosto[df_usable_agosto['Tributável'] == 'S']
        fat_RECEITA_agosto = df_receita_agosto['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_agosto = "R${:,.2f}".format(fat_RECEITA_agosto)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_agosto}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_agosto['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_agosto['Data de Emissão'] = pd.to_datetime(df_usable_agosto['Data de Emissão'], format='%d/%m/%Y')
        df_usable_agosto['Dia do Mês'] = df_usable_agosto['Data de Emissão'].dt.day
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
              template='plotly_dark')

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
        df_receita_setembro = df_usable_setembro[df_usable_setembro['Tributável'] == 'S']
        fat_RECEITA_setembro = df_receita_setembro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_setembro = "R${:,.2f}".format(fat_RECEITA_setembro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_setembro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_setembro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_setembro['Data de Emissão'] = pd.to_datetime(df_usable_setembro['Data de Emissão'], format='%d/%m/%Y')
        df_usable_setembro['Dia do Mês'] = df_usable_setembro['Data de Emissão'].dt.day
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
              template='plotly_dark')

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
        df_receita_outubro = df_usable_outubro[df_usable_outubro['Tributável'] == 'S']
        fat_RECEITA_outubro = df_receita_outubro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_outubro = "R${:,.2f}".format(fat_RECEITA_outubro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_outubro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_outubro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_outubro['Data de Emissão'] = pd.to_datetime(df_usable_outubro['Data de Emissão'], format='%d/%m/%Y')
        df_usable_outubro['Dia do Mês'] = df_usable_outubro['Data de Emissão'].dt.day
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
              template='plotly_dark')

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
        df_receita_novembro = df_usable_novembro[df_usable_novembro['Tributável'] == 'S']
        fat_RECEITA_novembro = df_receita_novembro['Valor para Receita'].sum()
        # Formatação do valor usando a formatação de moeda
        receita_formatado_novembro = "R${:,.2f}".format(fat_RECEITA_novembro)
        col2.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Receita: {receita_formatado_novembro}</p>', unsafe_allow_html=True)

# ==============================================================

        quant_clientes = df_usable_novembro['Cliente'].nunique()

        col3.markdown(f'<p style="font-size:30px; text-align:center; margin-top:100px; font-family:sans-serif; font-weight:bold; border:8px solid #ccc; border-radius:10px; padding:80px;">Clientes: {quant_clientes}</p>', unsafe_allow_html=True)
        
# =============================================================

        df_usable_novembro['Data de Emissão'] = pd.to_datetime(df_usable_novembro['Data de Emissão'], format='%d/%m/%Y')
        df_usable_novembro['Dia do Mês'] = df_usable_novembro['Data de Emissão'].dt.day
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
              template='plotly_dark')

        col5.plotly_chart(fig4, use_container_width=False)

# ===========================================================

        df_novembro = df_usable[df_usable['Mes_ano'] == '2023-10']
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

        # Criar o gráfico de barras com valores abreviados
        fig = px.bar(df_faturamento_mensal, x='Mes_ano', y='Valor da Nota',
                    text='Valor_abreviado',  # Utilizar os valores abreviados para o texto no gráfico
                    title=f'Faturamento Mensal para o Cliente {cliente_selecionado}',
                    labels={'Valor da Nota': 'Faturamento', 'Mes_ano': 'Mês e Ano'},
                    template='plotly_dark')

        # Adicionar rótulos com os valores abreviados
        fig.update_traces(texttemplate='%{text}', textposition='outside')

        # Adicionar uma linha que percorre as barras
        linha_tropica = go.Scatter(
            x=df_faturamento_mensal['Mes_ano'],
            y=df_faturamento_mensal['Valor da Nota'],
            mode='lines',
            line=dict(color='gray', width=3),
            name='Linha Tropica'
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
    

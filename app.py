import streamlit as st
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="SpyIA - Análise de Concorrência",
    page_icon="🔍",
    layout="wide"
)

# Configura o Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Estilos CSS customizados
st.markdown("""
<style>
    .big-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .action-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("🔍 SpyIA - Análise de Concorrência com IA")
st.markdown("### Descubra o que seus concorrentes estão fazendo")
st.caption("🤖 Powered by Google Gemini 2.5")

# Sidebar para inputs
with st.sidebar:
    st.header("📋 Dados da Análise")
    
    empresa_principal = st.text_input("Nome da Sua Empresa")
    tipo_negocio = st.text_input("Tipo de Negócio", placeholder="Ex: Pizzaria, Loja de Roupas...")
    cidade = st.text_input("Cidade", value="Bacabal")
    estado = st.text_input("Estado", value="MA")
    
    st.markdown("---")
    st.subheader("Concorrentes")
    
    concorrente1 = st.text_input("Concorrente 1")
    instagram1 = st.text_input("Instagram do Concorrente 1 (opcional)", placeholder="@username")
    
    concorrente2 = st.text_input("Concorrente 2")
    instagram2 = st.text_input("Instagram do Concorrente 2 (opcional)", placeholder="@username")
    
    concorrente3 = st.text_input("Concorrente 3 (opcional)")
    instagram3 = st.text_input("Instagram do Concorrente 3 (opcional)", placeholder="@username")
    
    st.markdown("---")
    faturamento_mensal = st.number_input("Seu faturamento mensal aproximado (R$)", min_value=0, value=10000, step=1000)
    
    analisar = st.button("🚀 Analisar Concorrência", type="primary")

# Função para buscar informações web
def buscar_info_empresa(nome_empresa, cidade, instagram=None):
    """Busca informações sobre a empresa na web com múltiplas estratégias"""
    
    resultados = []
    
    try:
        # Estratégia 1: Busca com Instagram se fornecido
        if instagram:
            query1 = f"instagram.com/{instagram.replace('@', '')} {nome_empresa}"
            resultados.append(f"🔎 Buscando: {query1}")
            
            jina_key = os.getenv("JINA_API_KEY")
            
            if jina_key:
                try:
                    search_url = f"https://s.jina.ai/{query1}"
                    headers = {
                        "Authorization": f"Bearer {jina_key}",
                        "X-Return-Format": "text"
                    }
                    
                    response = requests.get(search_url, headers=headers, timeout=20)
                    
                    if response.status_code == 200 and len(response.text) > 100:
                        resultados.append(f"✅ Dados encontrados via Instagram")
                        resultados.append(response.text[:4000])
                        return "\n".join(resultados)
                except Exception as e:
                    resultados.append(f"⚠️ Erro na busca do Instagram: {str(e)[:100]}")
        
        # Estratégia 2: Busca geral
        query2 = f"{nome_empresa} {cidade} contato telefone endereço"
        resultados.append(f"🔎 Buscando: {query2}")
        
        jina_key = os.getenv("JINA_API_KEY")
        
        if jina_key:
            try:
                search_url = f"https://s.jina.ai/{query2}"
                headers = {
                    "Authorization": f"Bearer {jina_key}",
                    "X-Return-Format": "text"
                }
                
                response = requests.get(search_url, headers=headers, timeout=20)
                
                if response.status_code == 200 and len(response.text) > 100:
                    resultados.append(f"✅ Dados encontrados via busca geral")
                    resultados.append(response.text[:3000])
                    return "\n".join(resultados)
                else:
                    resultados.append(f"⚠️ Busca retornou poucos dados (status: {response.status_code})")
            except Exception as e:
                resultados.append(f"⚠️ Erro na busca geral: {str(e)[:100]}")
        
        # Se chegou aqui, não conseguiu dados
        resultados.append(f"\n❌ DADOS NÃO IDENTIFICADOS")
        resultados.append(f"Possíveis razões:")
        resultados.append(f"- Instagram inexistente ou privado")
        resultados.append(f"- Baixa presença digital")
        resultados.append(f"- Nome comercial diferente do buscado")
        
        if instagram:
            resultados.append(f"\n💡 Recomendação: Verificar se o Instagram @{instagram.replace('@', '')} está correto")
        
        return "\n".join(resultados)
            
    except Exception as e:
        return f"❌ Erro ao coletar dados de {nome_empresa}: {str(e)}\n\nIsso será informado no relatório para análise manual."
        
# Função para análise TURBINADA com Gemini
def analisar_com_ia_turbinado(empresa_principal, concorrentes_info, tipo_negocio, faturamento):
    """Análise completa e acionável"""
    
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""Você é um consultor de negócios ALTAMENTE PRAGMÁTICO especializado em pequenas empresas brasileiras.

EMPRESA: {empresa_principal}
TIPO: {tipo_negocio}
FATURAMENTO MENSAL: R$ {faturamento:,.2f}

DADOS COLETADOS DOS CONCORRENTES:
{concorrentes_info}

Crie um relatório EXTREMAMENTE PRÁTICO e ACIONÁVEL seguindo ESTA ESTRUTURA EXATA:

## 📊 PANORAMA COMPETITIVO
Escreva 3-4 linhas diretas sobre o cenário. Seja específico e use dados quando disponíveis.

## 🔍 ANÁLISE DOS CONCORRENTES

Para cada concorrente, crie uma análise estruturada assim:

### [NOME DO CONCORRENTE]

**Presença Digital:**
- Instagram: [número de seguidores se disponível, ou "Não identificado"]
- Frequência de posts: [estimativa baseada nos dados]
- Tipo de conteúdo: [descrever brevemente]
- Engajamento aparente: [Alto/Médio/Baixo baseado nas informações]

**Pontos Fortes Identificados:**
- [liste 2-3 pontos ESPECÍFICOS baseados nos dados coletados]

**Vulnerabilidades:**
- [liste 2-3 pontos ESPECÍFICOS onde eles estão fracos]

**Estratégias Observadas:**
- [identifique 2-3 táticas que estão usando]

---

## 💎 5 OPORTUNIDADES DE OURO

Liste 5 oportunidades MUITO ESPECÍFICAS, cada uma com:
- **Oportunidade:** [nome curto]
- **Por quê:** [explicação rápida]
- **Impacto esperado:** [Alto/Médio - seja realista]

## ⚡ PLANO DE AÇÃO IMEDIATO (Próximas 24-48h)

Crie uma lista de 5 ações que podem ser feitas HOJE/AMANHÃ:

1. **[Ação específica]** - Tempo estimado: [X minutos/horas] | Custo: R$ [X] ou Grátis
2. **[Ação específica]** - Tempo estimado: [X minutos/horas] | Custo: R$ [X] ou Grátis
3. [continue...]

## 📅 ESTRATÉGIA 30 DIAS

Liste 5 ações para os próximos 30 dias, mais elaboradas:

**Semana 1:**
- [ação específica com passo a passo resumido]

**Semana 2:**
- [ação específica]

**Semana 3-4:**
- [ações específicas]

## 💰 PROJEÇÃO DE IMPACTO FINANCEIRO

Com base no faturamento atual de R$ {faturamento:,.2f}/mês:

**Se implementar 100% do plano:**
- Aumento de visibilidade: [X]%
- Novos clientes potenciais/mês: [número realista]
- Aumento de faturamento estimado: R$ [valor] a R$ [valor]
- ROI em 90 dias: [percentual]%

**Se implementar 50% do plano:**
- [números mais conservadores]

## 🚨 AMEAÇAS URGENTES

Liste 2-3 coisas que os concorrentes estão fazendo que representam RISCO REAL para {empresa_principal}:

1. **[Ameaça]** - Nível: 🔴 Alto / 🟡 Médio / 🟢 Baixo
   Por quê: [explicação]
   Contramedida: [o que fazer]

## 🎯 SEUS 3 PRÓXIMOS PASSOS (Ordem de prioridade)

1. **[Ação prioritária #1]**
   - Por quê fazer primeiro: [razão]
   - Como fazer: [resumo rápido]
   - Meta: [resultado esperado]

2. **[Ação #2]**
   [mesma estrutura]

3. **[Ação #3]**
   [mesma estrutura]

---

REGRAS IMPORTANTES:
- Use dados REAIS dos concorrentes quando disponíveis
- Se não tiver dados, seja HONESTO e diga "não identificado" 
- Números e projeções devem ser REALISTAS, não otimistas demais
- Toda recomendação deve ter COMO FAZER (mesmo que resumido)
- Foque em ações que uma pequena empresa PODE executar sozinha
- Use emojis moderadamente para destacar seções
- Seja DIRETO. Sem enrolação ou texto de enchimento."""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.8,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8000,
            },
            safety_settings=[
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        
        return response.text
        
    except Exception as e:
        return f"⚠️ Erro ao gerar análise: {str(e)}"

# Interface principal
if analisar:
    if not empresa_principal or not concorrente1:
        st.error("⚠️ Preencha pelo menos o nome da sua empresa e um concorrente!")
    else:
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("⚠️ API Key do Google Gemini não configurada!")
            st.stop()

        # Header da análise
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 Cidade", cidade)
        with col2:
            st.metric("🏢 Tipo", tipo_negocio)
        with col3:
            st.metric("💰 Faturamento", f"R$ {faturamento_mensal:,.0f}")
        
        st.markdown("---")

        with st.spinner("🔍 Coletando inteligência competitiva..."):
            
            concorrentes_lista = []
            instagrams = []
            
            if concorrente1:
                concorrentes_lista.append(concorrente1)
                instagrams.append(instagram1)
            if concorrente2:
                concorrentes_lista.append(concorrente2)
                instagrams.append(instagram2)
            if concorrente3:
                concorrentes_lista.append(concorrente3)
                instagrams.append(instagram3)
            
            info_concorrentes = f"Cidade: {cidade}, {estado}\n\n"
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, concorrente in enumerate(concorrentes_lista):
                instagram = instagrams[idx] if idx < len(instagrams) else None
                
                status_text.text(f"🔎 Investigando: {concorrente}...")
                progress_bar.progress((idx + 1) / len(concorrentes_lista))
                
                info = buscar_info_empresa(concorrente, cidade, instagram)
                info_concorrentes += f"\n\n{'='*60}\nCONCORRENTE: {concorrente}\n"
                if instagram:
                    info_concorrentes += f"Instagram: {instagram}\n"
                info_concorrentes += f"{'='*60}\n{info}\n"
            
            status_text.empty()
            progress_bar.empty()
        
        with st.spinner("🤖 Gerando análise estratégica com IA..."):
            analise = analisar_com_ia_turbinado(
                empresa_principal, 
                info_concorrentes, 
                tipo_negocio, 
                faturamento_mensal
            )
        
        # Mostra resultado
        st.success("✅ Análise Estratégica Concluída!")
        
        # Destaque visual
        st.markdown('<div class="success-box">📈 <strong>Relatório profissional gerado!</strong> Role para baixo para ver todas as seções.</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Exibe a análise
        st.markdown(analise)
        
        st.markdown("---")
        
        # Seção de call-to-action
        st.markdown('<div class="action-box">💡 <strong>Quer ajuda para implementar essas estratégias?</strong><br>Entre em contato para consultoria personalizada: <strong>[SEU CONTATO]</strong></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botões de download
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Baixar Relatório (TXT)",
                data=analise,
                file_name=f"spyia_analise_{empresa_principal.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            markdown_content = f"""# SpyIA - Análise Estratégica de Concorrência

**Empresa:** {empresa_principal}
**Tipo:** {tipo_negocio}
**Cidade:** {cidade}, {estado}
**Faturamento Mensal:** R$ {faturamento_mensal:,.2f}
**Data:** {datetime.now().strftime('%d/%m/%Y')}

---

{analise}

---

*Relatório gerado por SpyIA - Inteligência Competitiva com IA*
*Para consultoria personalizada, entre em contato.*
"""
            st.download_button(
                label="📄 Baixar Relatório (MD)",
                data=markdown_content,
                file_name=f"spyia_analise_{empresa_principal.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col3:
            # Botão para nova análise
            if st.button("🔄 Nova Análise", use_container_width=True):
                st.rerun()
        
        # Informação extra
        st.markdown("---")
        st.info("💡 **Próximo passo:** Implemente as ações imediatas e agende um acompanhamento em 30 dias para medir resultados!")
        
        # Feedback
        st.markdown("---")
        st.markdown("### 📊 Esta análise foi útil?")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔥 Excelente!", use_container_width=True):
                st.balloons()
                st.success("Ótimo! Implemente as ações e volte para contar os resultados!")
        with col2:
            if st.button("👍 Muito útil", use_container_width=True):
                st.success("Que bom! Boa sorte na implementação!")
        with col3:
            if st.button("😐 OK", use_container_width=True):
                st.info("Obrigado! Estamos sempre melhorando.")
        with col4:
            if st.button("👎 Fraco", use_container_width=True):
                st.warning("Sentimos muito! Entre em contato para melhorarmos.")

else:
    # Tela inicial melhorada
    st.markdown('<div class="action-box">👈 <strong>Preencha os dados na barra lateral e descubra como superar sua concorrência!</strong></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 O que você vai descobrir:
        
        ✅ **Análise profunda dos concorrentes**
        - Presença digital real
        - Estratégias identificadas
        - Pontos fracos para explorar
        
        ✅ **Plano de ação imediato**
        - Ações para fazer HOJE
        - Estratégia para 30 dias
        - Prioridades claras
        
        ✅ **Projeção financeira**
        - Impacto no faturamento
        - ROI estimado
        - Metas realistas
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Diferenciais do SpyIA:
        
        💎 **Dados reais, não suposições**
        - Análise de redes sociais
        - Presença digital dos concorrentes
        - Informações verificáveis
        
        ⚡ **Ações práticas**
        - Passo a passo para implementar
        - Estimativa de tempo e custo
        - Resultados esperados
        
        🎯 **Foco em resultados**
        - Projeções financeiras realistas
        - Ameaças e oportunidades
        - Próximos passos priorizados
        """)
    
    st.markdown("---")
    
    # Exemplos de casos
    with st.expander("📈 Veja exemplos de insights que você vai receber"):
        st.markdown("""
        **Exemplo de insight real:**
        
        > 🔍 "Seu concorrente X posta 5x por semana no Instagram às 19h, horário de maior engajamento. 
        > Você não tem presença digital. **Oportunidade:** Dominando o Instagram local, você pode capturar 
        > 30-50 novos clientes/mês, gerando R$ 4.500 adicionais."
        
        **Exemplo de ação imediata:**
        
        > ⚡ "Crie perfil business no Instagram HOJE - Tempo: 30 min | Custo: Grátis
        > 1. Acesse instagram.com/business
        > 2. Configure perfil com suas informações
        > 3. Adicione: localização, horário, WhatsApp
        > 4. Poste primeira foto usando o template que fornecemos"
        """)
    
    st.markdown("---")
    st.markdown("**💼 Desenvolvido para pequenos empresários que querem crescer de verdade**")
    st.caption("🔐 Seus dados são processados com segurança • 🤖 Powered by Google Gemini 2.5")

# Footer
st.markdown("---")
st.caption(f"SpyIA v2.0 - Inteligência Competitiva com IA • © {datetime.now().year}")
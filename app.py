import streamlit as st
import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv

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

# Título
st.title("🔍 SpyIA - Análise de Concorrência com IA")
st.markdown("### Descubra o que seus concorrentes estão fazendo")
st.caption("🤖 Powered by Google Gemini")

# Sidebar para inputs
with st.sidebar:
    st.header("📋 Dados da Análise")
    
    empresa_principal = st.text_input("Nome da Sua Empresa")
    tipo_negocio = st.text_input("Tipo de Negócio", placeholder="Ex: Pizzaria, Loja de Roupas...")
    cidade = st.text_input("Cidade", value="Bacabal")
    
    st.markdown("---")
    st.subheader("Concorrentes")
    
    concorrente1 = st.text_input("Concorrente 1")
    concorrente2 = st.text_input("Concorrente 2")
    concorrente3 = st.text_input("Concorrente 3 (opcional)")
    
    analisar = st.button("🚀 Analisar Concorrência", type="primary")

# Função para buscar informações com Jina AI
def buscar_info_empresa(nome_empresa, cidade):
    """Busca informações sobre a empresa na web"""
    try:
        query = f"{nome_empresa} {cidade} instagram facebook"
        
        # Usando Jina AI Reader para buscar
        jina_key = os.getenv("JINA_API_KEY")
        
        if not jina_key:
            return f"Buscando informações sobre {nome_empresa} em {cidade}..."
        
        search_url = f"https://s.jina.ai/{query}"
        headers = {
            "Authorization": f"Bearer {jina_key}",
            "X-Return-Format": "text"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.text[:3000]
        else:
            return f"Informações limitadas sobre {nome_empresa}"
            
    except Exception:
        return f"Coletando dados disponíveis sobre {nome_empresa} na região de {cidade}"

# Função para analisar com Gemini
def analisar_com_ia(empresa_principal, concorrentes_info, tipo_negocio):
    """Usa Google Gemini para analisar a concorrência"""
    
    # ✅ CORREÇÃO AQUI: nome do modelo atualizado
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""Você é um analista de mercado especializado em pequenas e médias empresas brasileiras.

EMPRESA ANALISADA: {empresa_principal}
TIPO DE NEGÓCIO: {tipo_negocio}

DADOS DOS CONCORRENTES:
{concorrentes_info}

Faça uma análise profissional e prática seguindo esta estrutura EXATA:

## 1. RESUMO EXECUTIVO
Escreva 3-4 linhas sobre o cenário competitivo identificado.

## 2. ANÁLISE DE CADA CONCORRENTE
Para cada concorrente mencionado, identifique:
- Principais pontos fortes
- Principais pontos fracos
- Estratégias identificadas

## 3. OPORTUNIDADES IDENTIFICADAS
Liste 5 oportunidades específicas para {empresa_principal}.

## 4. RECOMENDAÇÕES PRÁTICAS
Liste 5 ações concretas para os próximos 30 dias.

## 5. PONTOS DE ATENÇÃO
Ameaças competitivas reais.

## 6. PRÓXIMOS PASSOS
Liste 3 ações prioritárias.

IMPORTANTE:
- Seja direto
- Foco em ações práticas
- Se faltar dados, use lógica baseada no tipo de negócio
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 4096,
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
        return f"⚠️ Erro ao gerar análise: {str(e)}\n\nVerifique se sua API Key do Gemini está configurada corretamente."

# Interface principal
if analisar:
    if not empresa_principal or not concorrente1:
        st.error("⚠️ Preencha pelo menos o nome da sua empresa e um concorrente!")
    else:
        # Verifica API Key
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("⚠️ API Key do Google Gemini não configurada! Adicione no arquivo .env")
            st.stop()

        with st.spinner("🔍 Coletando informações dos concorrentes..."):
            
            concorrentes = [c for c in [concorrente1, concorrente2, concorrente3] if c]
            info_concorrentes = ""
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, concorrente in enumerate(concorrentes):
                status_text.text(f"📊 Analisando: {concorrente}...")
                progress_bar.progress((idx + 1) / len(concorrentes))
                
                info = buscar_info_empresa(concorrente, cidade)
                info_concorrentes += f"\n\n--- CONCORRENTE: {concorrente} ---\n{info}\n"
            
            status_text.empty()
            progress_bar.empty()
        
        with st.spinner("🤖 Analisando com Google Gemini AI..."):
            analise = analisar_com_ia(empresa_principal, info_concorrentes, tipo_negocio)
        
        st.success("✅ Análise Concluída!")
        
        st.markdown("---")
        st.markdown(analise)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Baixar Relatório (TXT)",
                data=analise,
                file_name=f"spyia_analise_{empresa_principal.replace(' ', '_')}.txt",
                mime="text/plain"
            )
        
        with col2:
            markdown_content = f"""# SpyIA - Análise de Concorrência

**Empresa:** {empresa_principal}
**Tipo:** {tipo_negocio}
**Cidade:** {cidade}

---

{analise}

---

*Relatório gerado por SpyIA - Análise de Concorrência com IA*
"""
            st.download_button(
                label="📄 Baixar Relatório (MD)",
                data=markdown_content,
                file_name=f"spyia_analise_{empresa_principal.replace(' ', '_')}.md",
                mime="text/markdown"
            )
        
        st.info("💡 Use essas informações para planejar suas próximas ações!")
        
        st.markdown("---")
        st.markdown("### 📊 Esta análise foi útil?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👍 Muito útil"):
                st.success("Obrigado pelo feedback!")
        with col2:
            if st.button("😐 Mais ou menos"):
                st.info("Vamos melhorar!")
        with col3:
            if st.button("👎 Precisa melhorar"):
                st.warning("Obrigado! Vamos aprimorar.")

else:
    st.info("👈 Preencha os dados na barra lateral e clique em **Analisar Concorrência**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Como funciona?
        1. Digite sua empresa e os concorrentes
        2. Clique para analisar
        3. Receba relatório completo

        ### 📊 O que você descobre:
        - Pontos fortes e fracos
        - Estratégias dos concorrentes
        - Oportunidades de mercado
        - Recomendações práticas
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Vantagens do SpyIA:
        - Análise rápida
        - IA do Google Gemini
        - Relatórios profissionais
        - Ideal para pequenos negócios
        """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido para empreendedores de Bacabal**")

# Footer
st.markdown("---")
st.caption("🔒 Seus dados são processados de forma segura.")
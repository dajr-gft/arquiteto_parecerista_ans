import os
import io
from genai_framework.decorators import file_input_route
from genai_framework.models import FileInput
from google.genai import Client
from google.genai import types
 
try:
    import pandas as pd
except ImportError:
    pd = None
 
@file_input_route("analisar_planilha_parecer")
def analisar_planilha_parecer(file: FileInput):
    """
    Analisa planilhas Excel (.xlsx, .xls) ou CSV e gera parecer arquitetural.
    Converte o conteúdo da planilha para texto estruturado antes de enviar ao agente.
    """
    if pd is None:
        return {
            "error": "Biblioteca pandas não instalada. Execute: pip install pandas openpyxl",
            "filename": file.filename
        }, 500
   
    # Validar extensões aceitas
    allowed_extensions = [".xlsx", ".xls", ".csv"]
    file_ext = os.path.splitext(file.filename.lower())[1]
   
    if file_ext not in allowed_extensions:
        return {
            "error": f"Tipo de arquivo não suportado. Aceitos: {', '.join(allowed_extensions)}",
            "filename": file.filename
        }, 400
   
    # Processar planilha e converter para texto
    try:
        # Criar buffer em memória com o conteúdo do arquivo
        file_buffer = io.BytesIO(file.content)
       
        # Ler planilha baseado na extensão
        if file_ext == '.csv':
            df = pd.read_csv(file_buffer, encoding='utf-8')
            texto_convertido = _converter_dataframe_para_texto(df)
        else:  # .xlsx ou .xls
            # Ler todas as abas
            excel_file = pd.ExcelFile(file_buffer)
            texto_convertido = ""
           
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                texto_convertido += f"\n\n=== ABA: {sheet_name} ===\n\n"
                texto_convertido += _converter_dataframe_para_texto(df)
       
        # Limitar tamanho do texto para evitar token overflow
        if len(texto_convertido) > 15000:
            texto_convertido = texto_convertido[:15000] + "\n\n[... conteúdo truncado devido ao tamanho ...]"
       
    except Exception as e:
        return {
            "error": f"Erro ao processar planilha: {str(e)}",
            "filename": file.filename,
            "dica": "Verifique se o arquivo está corrompido ou se o formato é válido"
        }, 400
   
    # Inicializar cliente Vertex AI
    client = Client(
        vertexai=True,
        project=os.getenv('PROJECT_ID'),
        location=os.getenv('LOCATION')
    )
   
    # Prompt especializado para análise de planilhas
    prompt = f"""Você é um Arquiteto Parecerista da ANS (Agência Nacional de Saúde).
 
Analise a planilha técnica abaixo e gere um parecer arquitetural considerando:
 
1. **Análise de Dados**: Avaliar a estrutura e qualidade dos dados apresentados
2. **Conformidade Técnica**: Verificar se os dados estão de acordo com especificações técnicas
3. **Riscos Identificados**: Identificar inconsistências, dados faltantes ou problemáticos
4. **Viabilidade**: Avaliar se os dados suportam a implementação proposta
5. **Recomendações**: Sugerir correções ou melhorias nos dados
 
**Planilha a analisar**:
Nome: {file.filename}
Tipo: {file_ext.upper()}
---
{texto_convertido}
---
 
Gere um parecer estruturado em formato JSON com os seguintes campos:
- parecer_final: "FAVORÁVEL", "FAVORÁVEL COM RESSALVAS" ou "DESFAVORÁVEL"
- justificativa: texto explicativo sobre a análise dos dados
- problemas_identificados: lista de problemas encontrados na planilha
- recomendacoes: lista de recomendações para correção/melhoria
- metricas: objeto com estatísticas relevantes (total de linhas, colunas, etc.)
"""
   
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2500,
            ),
        )
       
        return {
            "filename": file.filename,
            "status": "success",
            "analise": response.text.strip(),
            "tipo_documento": file_ext,
            "tamanho_bytes": len(file.content),
            "preview_texto": texto_convertido[:500] + "..." if len(texto_convertido) > 500 else texto_convertido
        }
       
    except Exception as e:
        return {
            "error": f"Erro ao gerar parecer: {str(e)}",
            "filename": file.filename
        }, 500
 
 
def _converter_dataframe_para_texto(df: 'pd.DataFrame') -> str:
    """
    Converte um DataFrame do pandas para texto estruturado e legível.
   
    Args:
        df: DataFrame do pandas a ser convertido
       
    Returns:
        String com o conteúdo da planilha formatado
    """
    texto = []
   
    # Informações gerais
    texto.append(f"Total de linhas: {len(df)}")
    texto.append(f"Total de colunas: {len(df.columns)}")
    texto.append(f"Colunas: {', '.join(df.columns.tolist())}\n")
   
    # Estatísticas básicas para colunas numéricas
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        texto.append("--- Estatísticas de Colunas Numéricas ---")
        for col in numeric_cols:
            texto.append(f"{col}: min={df[col].min()}, max={df[col].max()}, média={df[col].mean():.2f}")
        texto.append("")
   
    # Valores ausentes
    missing = df.isnull().sum()
    if missing.any():
        texto.append("--- Valores Ausentes ---")
        for col, count in missing[missing > 0].items():
            texto.append(f"{col}: {count} valores ausentes ({count/len(df)*100:.1f}%)")
        texto.append("")
   
    # Conteúdo da tabela (primeiras linhas)
    texto.append("--- Conteúdo da Planilha (primeiras 20 linhas) ---")
    texto.append(df.head(20).to_string(index=True))
   
    return "\n".join(texto)
 
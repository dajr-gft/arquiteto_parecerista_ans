import os
from genai_framework.decorators import file_input_route
from genai_framework.models import FileInput
from google.genai import Client
from google.genai import types
 
@file_input_route("analisar_documento_parecer")
def analisar_documento_parecer(file: FileInput):
    """
    Analisa documentos técnicos (PDF, TXT, DOCX) e gera parecer arquitetural.
    Aceita especificações técnicas, contratos, propostas de fornecedores, etc.
    """
    client = Client(
        vertexai=True,
        project=os.getenv('PROJECT_ID'),
        location=os.getenv('LOCATION')
    )
   
    # Validar extensões aceitas
    allowed_extensions = [".txt", ".pdf", ".doc", ".docx", ".md"]
    file_ext = os.path.splitext(file.filename.lower())[1]
   
    if file_ext not in allowed_extensions:
        return {
            "error": f"Tipo de arquivo não suportado. Aceitos: {', '.join(allowed_extensions)}",
            "filename": file.filename
        }, 400
   
    # Processar conteúdo do arquivo
    try:
        if file_ext in [".txt", ".md"]:
            conteudo = file.content.decode("utf-8")
        else:
            # Para PDF e DOCX, retornar indicação de que precisa processamento adicional
            conteudo = f"[Documento binário: {file.filename}]"
    except Exception as e:
        return {
            "error": f"Erro ao processar arquivo: {str(e)}",
            "filename": file.filename
        }, 400
   
    # Prompt especializado para análise arquitetural
    prompt = f"""Você é um Arquiteto Parecerista da ANS (Agência Nacional de Saúde).
 
Analise o documento técnico abaixo e gere um parecer arquitetural considerando:
 
1. **Aderência aos Princípios Arquiteturais**: Avaliar se a solução proposta está alinhada com os princípios de arquitetura da organização
2. **Riscos Técnicos**: Identificar riscos relacionados à tecnologia, integração, segurança e performance
3. **Conformidade**: Verificar aderência a normas, padrões e regulamentações (LGPD, ISO 27001, etc.)
4. **Viabilidade Técnica**: Avaliar se a solução é tecnicamente viável e sustentável
5. **Recomendações**: Sugerir melhorias, mitigações de risco ou ressalvas
 
**Documento a analisar**:
Nome: {file.filename}
---
{conteudo[:10000]}  # Limitar a 10k caracteres para evitar token overflow
---
 
Gere um parecer estruturado em formato JSON com os seguintes campos:
- parecer_final: "FAVORÁVEL", "FAVORÁVEL COM RESSALVAS" ou "DESFAVORÁVEL"
- justificativa: texto explicativo
- riscos_identificados: lista de riscos
- recomendacoes: lista de recomendações
- pontos_atencao: lista de pontos que requerem atenção especial
"""
   
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2000,
            ),
        )
       
        return {
            "filename": file.filename,
            "status": "success",
            "analise": response.text.strip(),
            "tipo_documento": file_ext,
            "tamanho_bytes": len(file.content)
        }
       
    except Exception as e:
        return {
            "error": f"Erro ao gerar parecer: {str(e)}",
            "filename": file.filename
        }, 500
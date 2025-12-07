"""
Mock Tools for BV ANS Agent Evaluation

These tools provide mock data from the mock folder to enable
comprehensive agent evaluation with realistic context.
"""

from pathlib import Path
from typing import Dict, Any


class MockDataProvider:
    """Provides mock data for agent evaluation."""

    def __init__(self):
        """Initialize mock data provider."""
        self.mock_dir = Path(__file__).parent.parent.parent.parent / 'src' / 'mock'
        self._load_mock_data()

    def _load_mock_data(self):
        """Load mock data from files."""
        # Load entendimento da demanda
        demanda_file = self.mock_dir / 'entendimento_demanda.txt'
        if demanda_file.exists():
            with open(demanda_file, 'r', encoding='utf-8') as f:
                self.entendimento_demanda = f.read()
        else:
            self.entendimento_demanda = ""

        # Load respostas do fornecedor
        respostas_file = self.mock_dir / 'respostas_fornecedor.txt'
        if respostas_file.exists():
            with open(respostas_file, 'r', encoding='utf-8') as f:
                self.respostas_fornecedor = f.read()
        else:
            self.respostas_fornecedor = ""

    def get_entendimento_demanda(self) -> str:
        """
        Get mock data for 'Entendimento da Demanda'.

        Returns:
            Complete understanding of business demand document
        """
        return self.entendimento_demanda

    def get_respostas_fornecedor(self) -> str:
        """
        Get mock data for 'Respostas do Fornecedor'.

        Returns:
            Complete vendor responses document
        """
        return self.respostas_fornecedor

    def enrich_document_query(self, query: str, document_type: str = "technical") -> str:
        """
        Enrich a document analysis query with mock context data.

        Args:
            query: Original query
            document_type: Type of document ('technical', 'commercial', 'proposal')

        Returns:
            Enriched query with mock context
        """
        # Add both documents as context
        enriched = f"""{query}

---

## CONTEXTO ADICIONAL FORNECIDO

### 📋 ENTENDIMENTO DA DEMANDA (Documento Obrigatório Fornecido)

{self.entendimento_demanda[:3000]}

### 📝 RESPOSTAS DO FORNECEDOR (Documento Obrigatório Fornecido)

{self.respostas_fornecedor[:3000]}

---

**IMPORTANTE**: Os dois documentos obrigatórios foram fornecidos acima. 
Proceda IMEDIATAMENTE com a análise comparativa completa dos 8 pilares.
"""
        return enriched


# Global instance
_mock_provider = None


def get_mock_provider() -> MockDataProvider:
    """Get or create mock data provider instance."""
    global _mock_provider
    if _mock_provider is None:
        _mock_provider = MockDataProvider()
    return _mock_provider


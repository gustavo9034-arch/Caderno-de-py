def get_security_text():
    return """
=== Conceitos de Segurança da Informação ===

1. Controle de Acesso:
Restringe a entrada no sistema apenas para usuários autenticados através de variáveis de sessão.

2. Tratamento de Senhas:
As senhas nunca são salvas em texto limpo. O projeto utiliza criptografia SHA-256 através do módulo 'hashlib'.

3. Validação de Dados:
Evita riscos de SQL Injection limpando caracteres especiais perigosos antes de processar as consultas.
"""
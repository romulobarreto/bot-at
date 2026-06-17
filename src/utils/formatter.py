"""
Formatação de mensagens.
"""

from datetime import datetime


def formatar_data(valor):
    if not valor:
        return "-"

    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return valor


def limpar_numero(valor):
    if valor is None:
        return "-"

    texto = str(valor)

    # remove .0 no final
    if texto.endswith(".0"):
        texto = texto[:-2]

    return texto


def formatar_cadastro(row) -> str:
    return f"""🏠 Unidade Consumidora: {row['INSTALACAO']}
⚡️ Status Comercial: {row['STATUS']}

👤 Cliente: {row['CLIENTE']}
📇 Documento: {row['DOCUMENTO']}

📝 Início de Contrato: {formatar_data(row['INICIO_CONTRATO'])}
📝 Fim de Contrato: {formatar_data(row['FIM_CONTRATO'])}

📍 Endereço: {row['ENDERECO']}
🌁 Município: {row['MUNICIPIO']}
📑 Regional: {row['REGIONAL']}

🔌 Tipo de Ligação: {row['FASE']}
🏷️ Classe: {row['CLASSE']}

📟 Medidor: {row['MEDIDOR']}
⚙️ GD: {row['MMGD']}
🛒 Fornecedor: {row['FORNECEDOR']}
🗓️ Ano: {row['ANO']}

🔍 Data Última Inspeção: {formatar_data(row['DATA_FISCALIZACAO'])}
🎯 Resultado: {limpar_numero(row['IRREG'])}
"""


def formatar_equipamento(row) -> str:
    return f"""🏠 Unidade Consumidora: {row['INSTALACAO']}

📟 Tipo do Equipamento: {row['EQUIPAMENTO']}
🏷️ Número: {row['NUM_EQUIPAMENTO']}

🛒 Fabricante: {row['FABRICANTE']}
🗓️ Ano: {row['ANO']}

⚡️ RTC - RTP: {row['RTC_RTP']}
🧤 Classe de Isolação: {row['CLASSE_ISOLACAO']}

1️⃣⚡️ Corrente Primária: {row['PRIM_CORRENTE']}
2️⃣⚡️ Corrente Secundária: {row['SEC_CORRENTE']}

1️⃣⚡️ Tensão Primária: {row['PRIM_TENSAO']}
2️⃣⚡️ Tensão Secundária: {row['SEC_TENSAO']}

📑 Classificação: {row['CLASSIFICACAO']}
"""


def gerar_imagem_tabela(df):
    import matplotlib.pyplot as plt
    from io import BytesIO

    colunas = [
        "MES",
        "CONSUMO_ATIVO_FP",
        "CONSUMO_ATIVO_NP",
        "LEITURA",
        "DEMANDA_LIDA_FP",
        "DEMANDA_LIDA_NP",
        "DEMANDA_CONT_FP",
        "DEMANDA_CONT_NP",
    ]

    df = df[colunas].copy()
    df = df.sort_values("MES", ascending=False)
    df = df.fillna("")

    df["MES"] = df["MES"].astype(str)

    # 🔥 altura dinâmica
    altura = max(2, len(df) * 0.5)

    fig, ax = plt.subplots(figsize=(14, altura))
    ax.axis("off")

    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center"
    )

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)

    # 🔥 estilos
    for (row, col), cell in tabela.get_celld().items():

        if row == 0:
            # header
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor("#1f4e79")  # azul escuro
        else:
            # linhas alternadas
            if row % 2 == 0:
                cell.set_facecolor("#f2f2f2")
            else:
                cell.set_facecolor("white")

    tabela.auto_set_column_width(list(range(len(colunas))))

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()

    buffer.seek(0)
    return buffer

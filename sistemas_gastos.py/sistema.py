import os
import json
from datetime import datetime

# Nome do arquivo para persistência dos dados
ARQUIVO_DADOS = "gastos_pessoais.json"


def limpar_tela():
    """Limpa o prompt de comando do Windows."""
    os.system("cls")


def carregar_dados():
    """Carrega os lançamentos salvos no arquivo JSON."""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def salvar_dados(lancamentos):
    """Salva a lista de lançamentos no arquivo JSON."""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(lancamentos, f, ensure_ascii=False, indent=4)


def cadastrar_lancamento(lancamentos):
    """Cadastra uma nova receita ou despesa."""
    limpar_tela()
    print("=" * 45)
    print("        CADASTRAR NOVO LANÇAMENTO        ")
    print("=" * 45)

    print("Tipo de lançamento:")
    print("1. Receita (+)")
    print("2. Despesa (-)")
    tipo_opcao = input("Escolha a opção (1 ou 2): ").strip()

    if tipo_opcao == "1":
        tipo = "Receita"
    elif tipo_opcao == "2":
        tipo = "Despesa"
    else:
        print("\n[!] Opção inválida! Operação cancelada.")
        input("\nPressione ENTER para continuar...")
        return

    descricao = input("Descrição (ex: Salário, Aluguel): ").strip()
    categoria = input("Categoria (ex: Alimentação, Moradia, Lazer): ").strip().title()

    try:
        valor = float(input("Valor (R$): ").replace(",", "."))
        if valor <= 0:
            print("\n[!] O valor deve ser maior que zero.")
            input("\nPressione ENTER para continuar...")
            return
    except ValueError:
        print("\n[!] Valor numérico inválido.")
        input("\nPressione ENTER para continuar...")
        return

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    novo_item = {
        "id": len(lancamentos) + 1,
        "tipo": tipo,
        "descricao": descricao if descricao else "Sem Descrição",
        "categoria": categoria if categoria else "Geral",
        "valor": valor,
        "data": data_atual
    }

    lancamentos.append(novo_item)
    salvar_dados(lancamentos)

    print(f"\n[✓] {tipo} cadastrada com sucesso!")
    input("\nPressione ENTER para continuar...")


def consultar_lancamentos(lancamentos):
    """Exibe o histórico de todos os lançamentos cadastrados."""
    limpar_tela()
    print("=" * 70)
    print("                 HISTÓRICO DE LANÇAMENTOS                 ")
    print("=" * 70)

    if not lancamentos:
        print("\nNenhum lançamento registrado até o momento.")
    else:
        print(f"{'ID':<4} | {'Data':<16} | {'Tipo':<8} | {'Categoria':<15} | {'Valor (R$)':<10} | {'Descrição'}")
        print("-" * 70)

        for item in lancamentos:
            sinal = "+" if item["tipo"] == "Receita" else "-"
            valor_fmt = f"{sinal} R$ {item['valor']:.2f}"
            print(f"{item['id']:<4} | {item['data']:<16} | {item['tipo']:<8} | {item['categoria']:<15} | {valor_fmt:<10} | {item['descricao']}")

    print("=" * 70)
    input("\nPressione ENTER para continuar...")


def calcular_saldo_e_estatisticas(lancamentos):
    """Calcula receitas, despesas, saldo total e a categoria com maior gasto."""
    limpar_tela()
    print("=" * 45)
    print("         RESUMO FINANCEIRO E SALDO         ")
    print("=" * 45)

    if not lancamentos:
        print("\nNenhum lançamento registrado para calcular.")
        input("\nPressione ENTER para continuar...")
        return

    total_receitas = 0.0
    total_despesas = 0.0
    gastos_por_categoria = {}

    for item in lancamentos:
        if item["tipo"] == "Receita":
            total_receitas += item["valor"]
        elif item["tipo"] == "Despesa":
            total_despesas += item["valor"]
            cat = item["categoria"]
            gastos_por_categoria[cat] = gastos_por_categoria.get(cat, 0.0) + item["valor"]

    saldo = total_receitas - total_despesas

    print(f"Total de Receitas (+): R$ {total_receitas:.2f}")
    print(f"Total de Despesas (-): R$ {total_despesas:.2f}")
    print("-" * 45)
    print(f"Saldo Total:           R$ {saldo:.2f}")
    print("=" * 45)

    # Identificar a categoria com maior gasto
    if gastos_por_categoria:
        categoria_maior_gasto = max(gastos_por_categoria, key=gastos_por_categoria.get)
        valor_maior_gasto = gastos_por_categoria[categoria_maior_gasto]

        print("\n--- ANÁLISE DE MAIOR GASTO ---")
        print(f"Categoria com maior gasto: {categoria_maior_gasto}")
        print(f"Total gasto na categoria: R$ {valor_maior_gasto:.2f}")
    else:
        print("\nNenhuma despesa registrada para análise por categoria.")

    print("=" * 45)
    input("\nPressione ENTER para continuar...")


def menu_principal():
    """Menu interativo do sistema."""
    lancamentos = carregar_dados()

    while True:
        limpar_tela()
        print("=============================================")
        print("      SISTEMA DE GASTOS PESSOAIS (CMD)       ")
        print("=============================================")
        print(" 1. Cadastrar Lançamento (Receita / Despesa)")
        print(" 2. Consultar Todos os Lançamentos")
        print(" 3. Calcular Saldo e Maior Gasto")
        print(" 4. Sair do Sistema")
        print("=============================================")

        opcao = input("Digite a opção desejada (1-4): ").strip()

        if opcao == "1":
            cadastrar_lancamento(lancamentos)
        elif opcao == "2":
            consultar_lancamentos(lancamentos)
        elif opcao == "3":
            calcular_saldo_e_estatisticas(lancamentos)
        elif opcao == "4":
            print("\nEncerrando o sistema... Até mais!")
            break
        else:
            print("\nOpção inválida! Escolha um número de 1 a 4.")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    menu_principal()
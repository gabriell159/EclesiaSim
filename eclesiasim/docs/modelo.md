# Definição do modelo (`modelo.py`)

Este documento detalha como é a criação do ambiente e como os agentes atuam sobre ele. Esse é o motor central do projeto.

## 📌 Principais atribuições

### 1. Inicialização da População
Responsável por criar o ambiente onde os agentes atuarão (rede de contatos) e definir quantos agentes começarão em cada estado, baseando-se nos parâmetros iniciais.

### 2. Ciclo de Vida
Coordena a passagem do tempo na simulação. A cada "rodada", o modelo ordena que os agentes interajam e atualizem seus estados.

### 3. Coleta de Resultados
Monitora o que acontece durante a simulação para gerar os dados (tabelas e gráficos) que serão exibidos na interface.

---

## 🔗 Integração
O modelo atua como o "maestro":
* **Com os Agentes:** Ele utiliza as regras definidas em `agentes.py` para processar as interações.
* **Com a Calibração:** Ele é chamado repetidamente pelo arquivo `calibracao.py` para testar se os parâmetros sugeridos pelo Algoritmo Genético são eficazes.
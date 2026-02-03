# Definição da calibração (`calibracao.py`)

Este documento descreve o funcionamento do módulo de otimização, que utiliza **Algoritmos Genéticos** para ajustar o simulador à realidade.

## 📌 Principais atribuições

### 1. Evolução de Parâmetros (DEAP)
Utiliza a biblioteca **DEAP** para automatizar a busca pelos parâmetros ideais. Em vez de você testar manualmente, o código "evolui" até encontrar os números que melhor explicam o crescimento.

### 2. Configuração do Algoritmo
Define as regras do processo evolutivo, incluindo:
* **Tamanho da População:** Quantas combinações de parâmetros são testadas por vez.
* **Número de Gerações:** Quantas vezes o processo de seleção vai se repetir.
* **Mutação e Crossover:** Probabilidades de variação para garantir que o algoritmo explore novas possibilidades.

### 3. Função de Aptidão (Fitness)
É o critério de qualidade. O algoritmo compara a curva gerada pela simulação com os dados reais informados. 
* **Objetivo:** Minimizar o erro (diferença) entre o simulado e o real.

### 4. Extração do "Melhor Indivíduo"
Ao final de todas as gerações, o módulo identifica e salva a melhor configuração encontrada, permitindo que a simulação final seja a mais precisa possível.

## Processo Técnico (GA)
O fluxo segue o padrão clássico de Algoritmos Genéticos:
1. **Avaliação:** Roda o `modelo.py` com os parâmetros atuais.
2. **Seleção:** Mantém os parâmetros que deram resultados mais realistas.
3. **Variação:** Aplica mutação para testar novos cenários.

---
## 🔗 Integração
A calibração é a camada externa que orquestra o aprendizado do sistema:
* **Com o Modelo:** Ela executa o `modelo.py` múltiplas vezes em paralelo ou sequência para validar cada "indivíduo" (conjunto de parâmetros).
* **Com os Agentes:** Ela define os valores numéricos que regem as probabilidades de transição entre os estados dos agentes.
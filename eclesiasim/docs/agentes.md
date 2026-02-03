# Definição dos agentes (`agentes.py`)
Este documento está diretamente relacionado com a criação/funcionamento dos agentes.

## 📌Principais atribuições

### 1. Criação dos agentes
Define como um agente é criado e também seu estado inicial (**Não crente**, **Entusiasta**, **Discípulo** e **Inativo**).

### 2. Comportamento
Regras de como um agente interage com outros agentes ou interage com o ambiente.

### 3. Atributos
Características que alteram a "personalidade" do agente, tais como:
* **Probabilidade de conversão**
* **Conexão com outros agentes**

---
## 🔗 Integração
Os agentes sao instanciados e gerenciados pelo arquivo de modelo (modelo.py). É o modelo que coordena o ciclo de vida e a atualização dos estados de cada agente a cada iteração.
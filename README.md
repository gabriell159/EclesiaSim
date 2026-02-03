# EclesiaSim

O EclesiaSim é um projeto que tem como objetivo unir Modelagem Baseada em Agentes (MBA) e Dinâmica de sistemas (DS) para analisar, de forma comparativa, crescimento e evasão em algumas congregaçoes nordestinas.

## 🏗️ Arquitetura 

O projeto segue uma arquitetura modular, organizada em camadas de responsabilidade: Definição de Agentes, Ambiente de Simulação e Camada de Otimização (Calibração)

## 🛠️ Tecnologias e Ferramentas

* **Python 3.13**
* **Mesa**: Framework para Modelagem Baseada em Agentes.
* **DEAP**: Framework para Algoritmos Genéticos (Calibração).
* **Pandas**: Processamento e análise dos dados históricos.
* **NetworkX (2.8.8)**: Modelagem de redes complexas e conexões entre agentes.
* **Matplotlib (3.10.6) / Numpy (2.3.3)**: Suporte matemático e visualização.

Para instalar as dependências, utilize o comando abaixo:

```bash
     pip install -r requirements.txt
```

## 📖 Documentação 

A documentacão detalhada de cada arquivo pode ser encontrada abaixo:
* 👥 [**Agentes**](eclesiasim/docs/agentes.md)
* ⚙️ [**Modelo**](eclesiasim/docs/modelo.md)
* 🧬 [**Calibração**](eclesiasim/docs/calibracao.md)

## 💻 Como Executar
Para executar uma bateria de testes e calibração, rode o comando:

---
    python calibracao.py
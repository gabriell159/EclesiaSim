from mesa import Model
from mesa.experimental.devs.simulator import ABMSimulator
import networkx as nx
from mesa.datacollection import DataCollector
from agentes import FielAgent

NAO_CRENTE = "NAO_CRENTE"
ENTUSIASTA = "ENTUSIASTA"
DISCIPULO = "DISCIPULO"
INATIVO = "INATIVO"

def coletar_estoques(model):
    estados = [a.estado for a in model.fiel_agents]
    return {
        "NAO_CRENTE": estados.count(NAO_CRENTE),
        "ENTUSIASTA": estados.count(ENTUSIASTA),
        "DISCIPULO": estados.count(DISCIPULO),
        "INATIVO": estados.count(INATIVO),
        "TOTAL_VERIFICADO": len(model.fiel_agents),
    }


class EclesiaSimModel(Model):
    def __init__(self, num_agentes=1000, topologia_rede="pequeno-mundo",proporcao_inicial=0.05,p_saida = 0.01, probabilidade_p=0.1, tau = 12, delta = 3, beta = 0.05, seed = None):

        super().__init__(seed=seed)
        self.num_agentes = num_agentes
        self.schedule = ABMSimulator()
        self.running = True
        self.topologia_rede = topologia_rede
        self.fiel_agents = []
        self.proporcao_inicial = proporcao_inicial
        self.p_saida = p_saida
        self.tau = tau
        self.delta = delta
        self.beta = beta

        self.datacollector = DataCollector(
            model_reporters={
                "NAO_CRENTE": lambda m: coletar_estoques(m)['NAO_CRENTE'],
                "ENTUSIASTA": lambda m: coletar_estoques(m)['ENTUSIASTA'],
                "DISCIPULO": lambda m: coletar_estoques(m)['DISCIPULO'],
                "INATIVO": lambda m: coletar_estoques(m)['INATIVO'],
                "TOTAL_VERIFICADO": lambda m: coletar_estoques(m)['TOTAL_VERIFICADO'],
            }
        )

        for i in range(self.num_agentes):
            if self.random.random() < self.proporcao_inicial:
                estado_inicial = ENTUSIASTA
            else:
                estado_inicial = NAO_CRENTE

            a = FielAgent(i, self, estado_inicial)
            self.fiel_agents.append(a)

        self.G = nx.Graph()
        self.G.add_nodes_from(range(self.num_agentes))

        if self.topologia_rede == "pequeno-mundo":
            self.G = nx.watts_strogatz_graph(n=self.num_agentes, k=4, p=probabilidade_p)
        elif self.topologia_rede == "estrela":
            self.G = nx.star_graph(self.num_agentes - 1)
        else:
            raise ValueError("Topologia de rede não reconhecida.")
        self.schedule.setup(self)

    def step(self):
        for agent in self.fiel_agents:
            agent.step()
        self.schedule.run_next_event()
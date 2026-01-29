from mesa import Agent

NAO_CRENTE = "NAO_CRENTE"
ENTUSIASTA = "ENTUSIASTA"
DISCIPULO = "DISCIPULO"
INATIVO = "INATIVO"


class FielAgent(Agent):
    def __init__(self, unique_id, model, estado_inicial):
        super().__init__(model)
        self.unique_id = unique_id
        self.model = model
        self.estado = estado_inicial

        if self.estado == ENTUSIASTA:
            self.tempo_entusiasta = 0
        else:
            self.tempo_entusiasta = -1

        self.grau_conexao = 0

    def atualizar_isolamento(self):
        if self.model.G.has_node(self.unique_id):
            self.grau_conexao = self.model.G.degree(self.unique_id)
        else:
            self.grau_conexao = 0

    def step(self):
        self.atualizar_isolamento()

        if self.estado in [ENTUSIASTA, DISCIPULO]:
            if self.random.random() < self.model.p_saida:
                self.estado = INATIVO
                self.tempo_entusiasta = -1
                return

        if self.estado in [ENTUSIASTA, DISCIPULO]:
            if self.grau_conexao <= self.model.delta:
                if self.random.random() < self.model.p_saida:
                    self.estado = INATIVO
                    self.tempo_entusiasta = -1
                    return

        if self.estado == ENTUSIASTA:
            self.tempo_entusiasta += 1
            if self.tempo_entusiasta >= self.model.tau:
                self.estado = DISCIPULO
                self.tempo_entusiasta = -1

        if self.estado == ENTUSIASTA:
            vizinhos_ids = list(self.model.G.neighbors(self.unique_id))
            for vizinho_id in vizinhos_ids:
                if vizinho_id < len(self.model.fiel_agents):
                    vizinho = self.model.fiel_agents[vizinho_id]
                else:
                    vizinho = None
                if vizinho and vizinho.estado == NAO_CRENTE:
                    if self.random.random() < self.model.beta:
                        vizinho.estado = ENTUSIASTA
                        vizinho.tempo_entusiasta = 0
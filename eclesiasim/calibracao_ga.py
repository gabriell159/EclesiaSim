import numpy as np
import math
from deap import base, creator, tools
import warnings

warnings.filterwarnings("ignore")

from modelo import EclesiaSimModel

BOUNDS = [(0.001, 0.20), (1.0, 60.0), (1.0, 10.0), (0.01, 0.25), (0.0, 0.05)]

NUM_PASSOS = 120
SERIE_ALVO = np.linspace(40,600, NUM_PASSOS)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

def gerar_parametro_aleatorio(index):
    low, high = BOUNDS[index]
    return np.random.uniform(low, high)

toolbox.register("attr_beta", gerar_parametro_aleatorio, 0)
toolbox.register("attr_tau", gerar_parametro_aleatorio, 1)
toolbox.register("attr_delta", gerar_parametro_aleatorio, 2)
toolbox.register("attr_prop", gerar_parametro_aleatorio, 3)
toolbox.register("attr_psaida", gerar_parametro_aleatorio, 4)

toolbox.register(
    "individual",
    tools.initCycle,
    creator.Individual,
    (toolbox.attr_beta, toolbox.attr_tau, toolbox.attr_delta, toolbox.attr_prop, toolbox.attr_psaida),
    n=1
)

SIMULACAO_SEED = 42
NUM_REPETICOES = 3


def calcular_rmse(simulado, real):
    if len(simulado) != len(real):
        return float('inf')

    erros_quadrados = [(s - r) ** 2 for s, r in zip(simulado, real)]
    mean_squared_error = sum(erros_quadrados) / len(erros_quadrados)
    rmse = math.sqrt(mean_squared_error)

    return rmse


def avaliar_fitness(individual):
    beta_float, tau_float, delta_float, prop_float, psaida_float = individual

    beta_float = np.clip(beta_float, BOUNDS[0][0], BOUNDS[0][1])
    tau_float = np.clip(tau_float, BOUNDS[1][0], BOUNDS[1][1])
    delta_float = np.clip(delta_float, BOUNDS[2][0], BOUNDS[2][1])
    prop_float = np.clip(prop_float, BOUNDS[3][0], BOUNDS[3][1])
    psaida_float = np.clip(psaida_float, BOUNDS[4][0], BOUNDS[4][1])

    tau = max(1, int(round(tau_float)))
    delta = max(1, int(round(delta_float)))

    if beta_float <= 0.0001:
        print(f"[AVISO] Beta inválido: {beta_float:.6f}")
        return float('inf'),

    all_rmses = []

    for i in range(NUM_REPETICOES):
        try:
            # Cria e roda o modelo
            modelo = EclesiaSimModel(
                num_agentes=1000,
                topologia_rede="pequeno-mundo",
                tau=tau,
                beta=beta_float,
                delta=delta,
                proporcao_inicial=prop_float,
                p_saida=psaida_float,
                seed=SIMULACAO_SEED + i
            )

            modelo.datacollector.collect(modelo)

            for step in range(NUM_PASSOS - 1):  # Roda 119 vezes
                modelo.step()
                modelo.datacollector.collect(modelo)

            dados_df = modelo.datacollector.get_model_vars_dataframe()

            if 'ENTUSIASTA' not in dados_df or 'DISCIPULO' not in dados_df:
                print(f"[ERRO] Variáveis esperadas não encontradas no DataCollector.")
                return float('inf'),

            membresia_simulada = dados_df['ENTUSIASTA'] + dados_df['DISCIPULO']

            if len(membresia_simulada) != len(SERIE_ALVO):
                print(f"[ERRO] Tamanho diferente: simulado={len(membresia_simulada)} | esperado={len(SERIE_ALVO)}")
                return float('inf'),

            rmse = calcular_rmse(membresia_simulada.values, SERIE_ALVO)
            all_rmses.append(rmse)

        except Exception as e:
            print(f"[ERRO] Falha na simulação com parâmetros {individual}: {e}")
            return float('inf'),

    return (np.mean(all_rmses),)

toolbox.register("evaluate", avaliar_fitness)

POPULATION_SIZE = 100
NUM_GENERATIONS = 10
CXPB = 0.7
MUTPB = 0.4


toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1.5, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def main_ga():
    pop = toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)

    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    hof.update(pop)

    log = tools.Logbook()
    record = stats.compile(pop)
    log.record(gen=0, **record)
    print(f"--- Geração 0 (Inicial) --- RMSE Mínimo: {record['min']:.2f}")

    for gen in range(1, NUM_GENERATIONS + 1):

        offspring = toolbox.select(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if np.random.rand() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

            if np.random.rand() < MUTPB:
                toolbox.mutate(child1)
                del child1.fitness.values
            if np.random.rand() < MUTPB:
                toolbox.mutate(child2)
                del child2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        hof.update(pop)

        record = stats.compile(pop)
        log.record(gen=gen, **record)
        print(f"--- Geração {gen} --- RMSE Mínimo: {record['min']:.2f}")

    melhor_solucao = hof[0]
    return melhor_solucao, log


if __name__ == "__main__":
    melhor_params, logbook = main_ga()

    beta_final = np.clip(melhor_params[0], BOUNDS[0][0], BOUNDS[0][1])
    tau_final = np.clip(melhor_params[1], BOUNDS[1][0], BOUNDS[1][1])
    delta_final = np.clip(melhor_params[2], BOUNDS[2][0], BOUNDS[2][1])
    prop_final = np.clip(melhor_params[3], BOUNDS[3][0], BOUNDS[3][1])
    psaida_final = np.clip(melhor_params[4], BOUNDS[4][0], BOUNDS[4][1])

    print("\n--- CALIBRAÇÃO CONCLUÍDA ---")
    print(f"RMSE Final Mínimo: {melhor_params.fitness.values[0]:.2f}")
    print(f"Melhores Parâmetros Encontrados:")
    print(f"\nBeta (Conversão): {beta_final * 100:.2f}%")
    print(f"Tau (Entusiasmo, meses): {int(round(tau_final))}")
    print(f"Delta (Isolamento, conexões): {int(round(delta_final))}")
    print(f"Proporção Inicial de Entusiastas: {prop_final * 100:.2f}%")
    print(f"Taxa de Saída (Secularização): {psaida_final * 100:.2f}%")

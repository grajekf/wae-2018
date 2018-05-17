
def budget_stopcondition_generator(budget):
    def stopconditon(population, fitness, **kwargs):
        current_uses = kwargs["current_uses"]
        return current_uses >= budget
    return stopconditon

def patience_stopcondition_generator(patience):
    def stopconditon(population, fitness, **kwargs):
        generation = kwargs["generation"]
        max_fitness = max(fitness)
        if max_fitness > stopconditon.best_fitness:
            stopconditon.best_fitness = max_fitness
            stopconditon.best_generation = generation
        return generation - stopconditon.best_generation > patience
    
    stopconditon.best_fitness = 0.0
    stopconditon.best_generation = 0
    return stopconditon
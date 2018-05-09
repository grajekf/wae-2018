
def budget_stopcondition_generator(budget):
    def stopconditon(population, fitness, **kwargs):
        current_uses = kwargs["current_uses"]
        return current_uses >= budget
    return stopconditon
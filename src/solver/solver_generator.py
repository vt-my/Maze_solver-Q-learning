from src.solver.solver import SolverOneStep


class SolverGenerator(object):
    # The solver factory
    @staticmethod
    def generate(cfg):
        return SolverOneStep(cfg)

import time
import cProfile
from functools import reduce

from famapy.metamodels.fm_metamodel.models import FeatureModel, FMConfiguration, Feature
from famapy.metamodels.fm_metamodel.transformations import FeatureIDEParser
from famapy.metamodels.fm_metamodel.utils import AAFMsHelper

from montecarlo4fms.problems.defective_configurations.models import ConfigurationStateCompletion
from montecarlo4fms.algorithms import MonteCarloAlgorithms

RESULT_FILE = "output_results/p1_results.txt"
INPUT_PATH = "montecarlo4fms/problems/defective_configurations/input_fms/"
OUTPUT_PATH = "montecarlo4fms/problems/defective_configurations/output_fms/"
FM_NAME = "aafms_framework"

def algorithm(montecarlo, initial_state):

    n = 0
    state = initial_state
    print(f"step ", end='', flush=True)
    while state.reward() <= 0 and state.get_actions():
        print(f"{n}.", end='', flush=True)
        new_state = montecarlo.run(state)
        state = new_state
        n += 1
    return state, montecarlo

def main():
    print("Problem 1: Completion of partial configurations.")
    print("-----------------------------------------------")

    with open(RESULT_FILE, 'w+') as file:
        file.write("Run, Algorithm, Iterations, Time, Features in Config, Valid Config, Reward, Nodes, Configuration\n")

    fide_parser = FeatureIDEParser(INPUT_PATH + FM_NAME + ".xml")
    fm = fide_parser.transform()

    required_features_names = ['Glucose']
    required_features = [fm.get_feature_by_name(f) for f in required_features_names]

    initial_state = ConfigurationStateCompletion(configuration=FMConfiguration(), feature_model=fm, aafms_helper=AAFMsHelper(fm), required_features=required_features)

    #ss = SearchSpace(initial_state=initial_state, max_depth=20)

    runs = 3
    iterations = 100
    for r in range(1,runs+1):
        montecarlo = MonteCarloAlgorithms.uct_iterations_maxchild_random_expansion(iterations=iterations)

        print(f"Run {r} for {type(montecarlo).__name__} with {iterations} iterations.")
        start = time.time()
        state, montecarlo = algorithm(montecarlo, initial_state)
        end = time.time()
        print(f"Done!")

        with open(RESULT_FILE, 'a+') as file:
            file.write(f"{r}, {type(montecarlo).__name__}, {iterations}, {end-start}, {len(state.configuration.elements)}, {state.is_valid_configuration}, {state.reward()}, {len(montecarlo.tree)}, {[str(f) for f in state.configuration.elements if state.configuration.elements[f]]}\n")

if __name__ == '__main__':
    cProfile.run("main()")
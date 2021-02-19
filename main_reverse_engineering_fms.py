from famapy.metamodels.fm_metamodel.models import FeatureModel, FMConfiguration, Feature
from famapy.metamodels.fm_metamodel.transformations import FeatureIDEParser, UVLWritter
from famapy.metamodels.fm_metamodel.utils import AAFMsHelper

from montecarlo4fms.models import StateFM
from montecarlo4fms.algorithms import MCTSIterations, MCIterations


if __name__ == '__main__':
    print("Reverse engineering problem")

    # Read the feature model
    fide_parser = FeatureIDEParser("input_fms/pizzas.xml")
    fm = fide_parser.transform()

    print(f"#Features: {len(fm.get_features())} -> {[str(f) for f in fm.get_features()]}")

    # Get configurations
    aafms_helper = AAFMsHelper(fm)
    configurations = aafms_helper.get_configurations()

    nc = 1
    for c in configurations:
        print(f"config {nc}: {[str(f) for f in c]}")
        nc += 1
    print(f"#Configurations: {len(configurations)}")

    iterations = 100000
    montecarlo = MCIterations(iterations=iterations)
    print(f"Running {type(montecarlo).__name__} with {iterations} iterations.")

    initial_state = StateFM(FeatureModel(None), configurations)

    n = 0
    state = initial_state
    while not state.is_terminal():
        print(f"State {n}: {[str(f) for f in state.feature_model.get_features()]} -> {state.reward()}")
        new_state = montecarlo.run(state)
        montecarlo.print_MC_values()
        state = new_state
        n += 1

    print(f"Final State {n}: {[str(f) for f in state.feature_model.get_features()]} -> {state.reward()}")

    aafms_helper = AAFMsHelper(state.feature_model)
    new_configurations = aafms_helper.get_configurations()

    print(f"#Features: {len(state.feature_model.get_features())} -> {[str(f) for f in state.feature_model.get_features()]}")

    nc = 1
    for c in new_configurations:
        print(f"config {nc}: {[str(f) for f in c]}")
        nc += 1
    print(f"#Configurations: {len(new_configurations)}")

    print(f"Final State {n}: {[str(f) for f in state.feature_model.get_features()]} -> {state.reward()}")

    path = "output_fms/" + state.feature_model.root.name + "." + UVLWritter.get_destination_extension()
    uvl_writter = UVLWritter(path=path, source_model=state.feature_model)
    uvl_model = uvl_writter.transform()

    print(f"UVL model saved in: {path}")

    #
    # while not state.is_terminal():
    #     n += 1
    #     print(f"State {n}: {[str(f) for f in state.feature_model.get_features()]} -> {state.reward()}")
    #     ns = 1
    #     # for s in state.find_successors():
    #     #     print(f"Suc {ns}: {[str(f) for f in s.feature_model.get_features()]} -> {s.reward()}")
    #     #     ns += 1
    #
    #
    #     #aafms_helper = AAFMsHelper(state.feature_model)
    #     #print(aafms_helper.is_valid_configuration(configurations[0]))
    #     state = mcts.run(state)

    #print(f"Final state: {state}")


    # path = "output_fms/" + state.feature_model.root.name + "." + UVLWritter.get_destination_extension()
    # print(path)
    # uvl_writter = UVLWritter(path=path, source_model=state.feature_model)
    # uvl_model = uvl_writter.transform()
    #
    # aafms_helper = AAFMsHelper(state.feature_model)
    # new_configurations = aafms_helper.get_configurations()
    # print(f"Contained all configurations?: {all(c in new_configurations for c in configurations)}")


    #
    #
    # actions = initial_state.get_actions()
    #
    # print([str(a) for a in actions])
    #
    # successors = initial_state.find_successors()
    # print(successors)
    #
    # ss2 = successors[0].find_successors()
    # print(len(ss2))
    #
    # ss3 = ss2[0].find_successors()
    # print(len(ss3))

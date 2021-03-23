from famapy.core.transformations import TextToModel

from famapy.metamodels.pysat_metamodel.models.pysat_model import PySATModel


class CNFReader(TextToModel):
    """
    Read a CNF formula representing a feature model.
    The expected format is the generated by FeatureIDE as Textual Symbols:
    (feature1) and (not feature2 or feature3) and (not feature4 or feature5) and...
    """

    @staticmethod
    def get_source_extension() -> str:
        return 'txt'

    def __init__(self, path: str):
        self._path = path
        self.counter = 1
        self.destination_model = PySATModel()
        self.cnf = self.destination_model.cnf

    def transform(self) -> PySATModel:
        self._read_clauses(self._path)
        return self.destination_model

    def _add_feature(self, feature_name):
        if feature_name not in self.destination_model.variables.keys():
            self.destination_model.variables[feature_name] = self.counter
            self.destination_model.features[self.counter] = feature_name
            self.counter += 1

    def _read_clauses(self, filepath: str):
        with open(filepath) as file:
            cnf_line = file.readline()
            clauses = list(map(lambda c: c[1:len(c)-1], cnf_line.split(' and ')))  # Remove initial and final parenthesis
            clauses[len(clauses)-1] = clauses[len(clauses)-1][:-1]  # Remove final parenthesis of last clause (because of '\n')
            for c in clauses:
                tokens = c.split(' ')
                tokens = list(filter(lambda t: t != 'or', tokens))
                logic_not = False
                cnf_clause = []
                for feature in tokens:
                    if feature == 'not':
                        logic_not = True
                    else:
                        self._add_feature(feature)
                        if logic_not:
                            cnf_clause.append(-1*self.destination_model.variables[feature])
                        else:
                            cnf_clause.append(self.destination_model.variables[feature])
                        logic_not = False
                self.destination_model.add_constraint(cnf_clause)

class Analyzer:
    def __init__(self, source_type, path):
        self.source_type = source_type
        self.path = path

    def run(self):
        print("RUN!")


class VerifyAnalyzer(Analyzer):
    def run(self):
        print('Starting verification for: %s %s', self.source_type, self.path)


class FixAnalyzer(Analyzer):
    def run(self):
        print('Starting fix for: %s %s', self.source_type, self.path)

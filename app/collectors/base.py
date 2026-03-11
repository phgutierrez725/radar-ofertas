class BaseCollector:
    def __init__(self, source_name: str):
        self.source_name = source_name

    def collect(self):
        raise NotImplementedError("O coletor precisa implementar o método collect().")

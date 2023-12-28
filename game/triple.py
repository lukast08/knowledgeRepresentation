class Triple:
    def __init__(self, predicate_uri, object_uri, literal=False) -> None:
        self.predicate_uri = predicate_uri
        self.object_uri = object_uri
        self.literal = literal

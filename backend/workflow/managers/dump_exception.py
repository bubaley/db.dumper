class DumpException(Exception):
    def __init__(self, name: str, text: str | None):
        self.name: str = name
        self.text: str | None = text

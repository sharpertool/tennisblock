class BlockDateConverter:
    regex = '\d{4}-\d{1,2}-\d{1,2}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


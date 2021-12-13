from io import BytesIO


class ImageEndpoint:
    def __init__(
        self,
        endpoint: str, # just something like "oil" or "frostedglass"
        **options
    ):
        self.endpoint = endpoint
        self.options = options

    def __repr__(self) -> str:
        fmt = "<ImageEndpoint endpoint={0.endpoint!r}>"
        return fmt.format(self)

    @classmethod
    def build(cls, endpoint: str, **options):
        endpoint = endpoint.lower()

        if endpoint.startswith("/image/"):
            endpoint = endpoint.replace("/image/", "")
        elif endpoint.startswith("/image"):
            endpoint = endpoint.replace("/image", "")

        endpoint = endpoint.replace("/", "") # remove any extra slashes that may exist

        return cls(endpoint, **options)

    
class Image:
    def __init__(self, _bytes: bytes, _format: str):
        self.raw = _bytes
        self.format = _format
        self.io = BytesIO(_bytes)
        
        if self.io.seekable():
            self.io.seek(0)

    def __repr__(self) -> str:
        fmt = "<Image format={0.format!r} size={0.size!r}>"
        return fmt.format(self)

    @property
    def size(self) -> int:
        return self.io.__sizeof__()

    def write(self, fp: str):
        with open(fp, "wb+") as f:
            f.write(self.raw)
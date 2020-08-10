from dataclasses import dataclass


@dataclass
class Product:
    name: str
    std_name: str
    code: str
    rel_href: str
    abs_href: str
    base_url: str
    seed_url: str
    desc: str

    def __lt__(self, other):
        return self.code < other.code

from dataclasses import dataclass


@dataclass
class Product:
    name: str
    std_name: str
    rel_href: str
    abs_href: str
    base_url: str
    seed_url: str
    desc: str

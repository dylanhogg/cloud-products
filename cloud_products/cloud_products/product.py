from dataclasses import dataclass


@dataclass
class Product:
    name: str
    std_name: str
    code: str
    rel_href: str
    abs_href: str
    abs_href_faq: str
    base_url: str
    seed_url: str
    desc: str

    def __lt__(self, other):
        return self.code < other.code

    def to_dict(self):
        return {
            "name": self.name,
            "std_name": self.std_name,
            "code": self.code,
            "rel_href": self.rel_href,
            "abs_href": self.abs_href,
            "abs_href_faq": self.abs_href_faq,
            "base_url": self.base_url,
            "seed_url": self.seed_url,
            "desc": self.desc,
        }

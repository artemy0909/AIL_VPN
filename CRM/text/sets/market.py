from dataclasses import dataclass
from ..dynamic import start


@dataclass
class Start:
    hello_customer: callable = start.hello_customer

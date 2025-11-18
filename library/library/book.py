from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils
import random

@dataclass
class Book:
	name: str
	type: str
	stock: int
	id: str = field(default_factory=RandomUtils.generate_random_id)


	@property
	def search_string(self):
		return f"{self.name}{self.type}"
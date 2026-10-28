"""Модель движения капель, независимая от интерфейса."""
from dataclasses import dataclass
import random


@dataclass
class Drop:
    """Капля с координатами и глубиной от 0 до 1."""

    x: float
    y: float
    depth: float

    @property
    def speed(self):
        """Вернуть скорость в пикселях в секунду."""
        return 120 + 360 * self.depth

    @property
    def length(self):
        """Вернуть длину капли с учетом глубины."""
        return 5 + 15 * self.depth


class RainModel:
    """Хранить капли и обновлять их положение."""

    def __init__(self, width=900, height=560, count=180, seed=None):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
        self.drops = []
        self.set_count(count)

    def set_count(self, count):
        """Установить количество капель."""
        count = max(0, int(count))
        self.drops = self.drops[:count]
        while len(self.drops) < count:
            self.drops.append(Drop(
                self.rng.uniform(0, self.width),
                self.rng.uniform(-20, self.height),
                self.rng.random(),
            ))

    def update(self, dt, speed=1.0):
        """Сдвинуть капли за dt секунд и вернуть вышедшие за край наверх."""
        for drop in self.drops:
            drop.y += drop.speed * dt * speed
            if drop.y - drop.length > self.height:
                drop.y = -drop.length
                drop.x = self.rng.uniform(0, self.width)

    def reset(self):
        """Заново распределить капли по полю."""
        count = len(self.drops)
        self.drops.clear()
        self.set_count(count)

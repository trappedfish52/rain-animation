"""Проверки движения, глубины и повторного появления капель."""
import unittest

from src.model import Drop, RainModel


class RainTests(unittest.TestCase):
    """Проверить математическую модель без графического окна."""

    def test_depth(self):
        """Близкая капля больше и быстрее дальней."""
        far, near = Drop(0, 0, 0), Drop(0, 0, 1)
        self.assertGreater(near.speed, far.speed)
        self.assertGreater(near.length, far.length)

    def test_movement(self):
        """Перемещение зависит от времени и множителя скорости."""
        model = RainModel(count=1, seed=1)
        drop = model.drops[0]
        drop.y = 0
        model.update(0.1, 2)
        self.assertAlmostEqual(drop.y, drop.speed * 0.2)
        model.update(1, 0)
        self.assertAlmostEqual(drop.y, drop.speed * 0.2)

    def test_recycle(self):
        """Капля за нижним краем появляется над верхним."""
        model = RainModel(count=1, seed=1)
        drop = model.drops[0]
        drop.y = model.height + drop.length + 1
        model.update(0)
        self.assertEqual(drop.y, -drop.length)
        self.assertTrue(0 <= drop.x <= model.width)

    def test_density_and_reset(self):
        """Изменение плотности и сброс сохраняют нужное число капель."""
        model = RainModel(count=20, seed=1)
        model.set_count(50)
        self.assertEqual(len(model.drops), 50)
        model.set_count(10)
        model.reset()
        self.assertEqual(len(model.drops), 10)


if __name__ == "__main__":
    unittest.main()

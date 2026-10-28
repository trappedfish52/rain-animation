"""Отрисовка капель на Canvas."""


class Renderer:
    """Обновлять существующие линии без очистки всего холста."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.items = []

    def draw(self, drops):
        """Нарисовать текущее состояние модели."""
        while len(self.items) > len(drops):
            self.canvas.delete(self.items.pop())
        while len(self.items) < len(drops):
            self.items.append(self.canvas.create_line(0, 0, 0, 0))
        for item, drop in zip(self.items, drops):
            brightness = int(100 + 155 * drop.depth)
            color = f"#{brightness // 2:02x}{brightness:02x}ff"
            self.canvas.coords(
                item, drop.x, drop.y, drop.x, drop.y - drop.length
            )
            self.canvas.itemconfigure(
                item, fill=color, width=1 + 2 * drop.depth
            )

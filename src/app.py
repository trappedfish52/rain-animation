"""Окно, управление и цикл анимации tkinter."""
import time
import tkinter as tk
from tkinter import ttk

from src.model import RainModel
from src.renderer import Renderer


class App:
    """Приложение с анимацией дождя и настройками."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дождь — Садритдинов Эльдар — ПИ25-3")
        self.root.resizable(False, False)
        self.model = RainModel()
        self.paused = False
        self.last_time = time.perf_counter()
        self.speed = tk.DoubleVar(value=1.0)
        self.count = tk.IntVar(value=180)
        ttk.Label(
            self.root, text="ДОЖДЬ  •  Простая анимация",
            font=("Arial", 18, "bold"), padding=12,
        ).pack(anchor="w")
        self.canvas = tk.Canvas(
            self.root, width=900, height=560,
            bg="#0b1424", highlightthickness=0,
        )
        self.canvas.pack()
        self.renderer = Renderer(self.canvas)
        panel = ttk.Frame(self.root, padding=12)
        panel.pack(fill="x")
        self.pause_button = ttk.Button(
            panel, text="Пауза", command=self.toggle_pause
        )
        self.pause_button.pack(side="left")
        ttk.Button(panel, text="Сброс", command=self.reset).pack(
            side="left", padx=8
        )
        ttk.Label(panel, text="Скорость").pack(side="left", padx=8)
        tk.Scale(
            panel, from_=0.2, to=3, resolution=0.1,
            orient="horizontal", variable=self.speed, length=160,
        ).pack(side="left")
        ttk.Label(panel, text="Капли").pack(side="left", padx=8)
        tk.Scale(
            panel, from_=20, to=500, resolution=10,
            orient="horizontal", variable=self.count, length=160,
            command=lambda value: self.model.set_count(float(value)),
        ).pack(side="left")
        ttk.Label(
            self.root,
            text="Пробел — пауза   •   R / К — сброс   •   Esc — выход\n"
                 "Садритдинов Эльдар Сайфиддинович | ПИ25-3",
            padding=10,
        ).pack(anchor="w")
        self.root.bind("<space>", self.toggle_pause)
        self.root.bind("<KeyPress>", self.on_key)
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.tick()

    def on_key(self, event):
        """Обработать сброс в русской и английской раскладках."""
        if event.char.lower() in ("r", "к"):
            self.reset()

    def toggle_pause(self, event=None):
        """Переключить паузу без накопления времени движения."""
        self.paused = not self.paused
        self.pause_button.config(
            text="Продолжить" if self.paused else "Пауза"
        )
        return "break"

    def reset(self):
        """Сбросить распределение капель."""
        self.model.reset()
        self.renderer.draw(self.model.drops)

    def tick(self):
        """Обновить модель и запланировать следующий кадр."""
        now = time.perf_counter()
        dt = min(now - self.last_time, 0.05)
        self.last_time = now
        if not self.paused:
            self.model.update(dt, self.speed.get())
        self.renderer.draw(self.model.drops)
        self.root.after(16, self.tick)

    def run(self):
        """Запустить главный цикл обработки событий."""
        self.root.mainloop()

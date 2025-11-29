# ------------------ FILE: oyunlar.py ------------------
"""
Oyun fonksiyonları: snake, ball, maria
"""
import tkinter as tk
from tkinter import Toplevel, Canvas, Label, messagebox
import random


def open_ball_game(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("Top Yakalama")
    win.geometry("400x300")
    score = [0]
    canvas = Canvas(win, width=400, height=300, bg="white")
    canvas.pack()
    ball = canvas.create_oval(180, 140, 220, 180, fill="red")
    def click_ball(event):
        if canvas.find_withtag("current"):
            score[0] += 1
            label.config(text=f"Score: {score[0]}")
            x = random.randint(0, 360)
            y = random.randint(0, 260)
            canvas.coords(ball, x, y, x+40, y+40)
    canvas.tag_bind(ball, "<Button-1>", click_ball)
    label = Label(win, text="Score: 0")
    label.pack()
    return win


def open_snake_game(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("Yılan Oyunu")
    win.geometry("400x400")
    canvas = Canvas(win, width=400, height=400, bg="black")
    canvas.pack()
    canvas.focus_set()
    snake = [(200,200)]
    snake_dir = "Right"
    food = [random.randrange(0,20)*20, random.randrange(0,20)*20]
    food_rect = canvas.create_rectangle(food[0], food[1], food[0]+20, food[1]+20, fill="green")
    def move_snake():
        nonlocal snake, snake_dir, food
        x, y = snake[-1]
        if snake_dir=="Right": x+=20
        elif snake_dir=="Left": x-=20
        elif snake_dir=="Up": y-=20
        elif snake_dir=="Down": y+=20
        if x < 0 or x >= 400 or y < 0 or y >= 400 or (x,y) in snake:
            messagebox.showinfo("Oyun Bitti", f"Skorunuz: {len(snake)}")
            win.destroy()
            return
        snake.append((x,y))
        canvas.delete("snake")
        for seg in snake:
            canvas.create_rectangle(seg[0], seg[1], seg[0]+20, seg[1]+20, fill="white", tag="snake")
        if x==food[0] and y==food[1]:
            food = [random.randrange(0,20)*20, random.randrange(0,20)*20]
            canvas.coords(food_rect, food[0], food[1], food[0]+20, food[1]+20)
        else:
            snake.pop(0)
        win.after(200, move_snake)
    def change_dir(event):
        nonlocal snake_dir
        opposite = {"Up":"Down", "Down":"Up", "Left":"Right", "Right":"Left"}
        if event.keysym in ["Up","Down","Left","Right"] and event.keysym != opposite.get(snake_dir):
            snake_dir = event.keysym
    win.bind("<Key>", change_dir)
    move_snake()
    return win


def open_maria_game(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("Maria'yı Kurtar")
    win.geometry("500x500")
    canvas = Canvas(win, width=500, height=500, bg="lightblue")
    canvas.pack()
    messagebox.showinfo("Başlangıç", "Maria arkadaşı Sely ile gezerken kayboldu! Hadi ipuçlarını bul ve Maria'yı kurtar!")
    paper_pieces = []
    positions = [(50,50), (200,100), (350,200)]
    text_message = "Sely, kurtar beni"
    for pos in positions:
        piece = canvas.create_rectangle(pos[0], pos[1], pos[0]+30, pos[1]+30, fill="yellow")
        paper_pieces.append(piece)
    collected = []
    def collect_piece(event):
        for piece in paper_pieces:
            coords = canvas.coords(piece)
            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                if piece not in collected:
                    collected.append(piece)
                    canvas.itemconfig(piece, fill="gray")
        if len(collected) == len(paper_pieces):
            messagebox.showinfo("İpucu Bulundu", f"Kağıt parçaları birleştirildi: '{text_message}'\nCanavarlar çıkıyor! Obby başlıyor...")
            start_obby()
    canvas.bind("<Button-1>", collect_piece)
    sely = canvas.create_rectangle(20, 450, 40, 470, fill="green")
    obstacles = []
    obstacle_speed = 5
    for y in range(50, 400, 100):
        obs = canvas.create_rectangle(100, y, 150, y+20, fill="red")
        obstacles.append(obs)
    def move_obby():
        for obs in obstacles:
            canvas.move(obs, obstacle_speed, 0)
            coords = canvas.coords(obs)
            if coords[2] >= 500 or coords[0] <= 0:
                canvas.move(obs, -obstacle_speed*10, 0)
            if check_collision(sely, obs):
                messagebox.showinfo("Obby", "Sely çarptı! Yeniden başla.")
                canvas.coords(sely, 20, 450, 40, 470)
        win.after(50, move_obby)
    def check_collision(rect1, rect2):
        x1,y1,x2,y2 = canvas.coords(rect1)
        a1,b1,a2,b2 = canvas.coords(rect2)
        return not (x2<a1 or x1>a2 or y2<b1 or y1>b2)
    boss_hp = [500]
    sely_lives = [5]
    boss = canvas.create_rectangle(200,50,300,150, fill="purple")
    boss_attacks = []
    def boss_attack():
        fireball = canvas.create_oval(250,150,270,170, fill="orange")
        boss_attacks.append(fireball)
        animate_fireball(fireball)
        if sely_lives[0] > 0 and boss_hp[0] > 0:
            win.after(1500, boss_attack)
    def animate_fireball(fireball):
        canvas.move(fireball, 0, 10)
        if canvas.coords(fireball)[3] >= 500:
            canvas.delete(fireball)
            if fireball in boss_attacks: boss_attacks.remove(fireball)
        else:
            if check_collision(sely, fireball):
                sely_lives[0] -= 1
                canvas.delete(fireball)
                if fireball in boss_attacks: boss_attacks.remove(fireball)
                if sely_lives[0] <= 0:
                    messagebox.showinfo("Oyun Bitti", "Sely öldü! Maria kurtulamadı.")
                    win.destroy()
                    return
            win.after(50, lambda: animate_fireball(fireball))
    def decrease_boss_hp(event):
        if boss_hp[0] > 0:
            boss_hp[0] -= 1
            if boss_hp[0] <= 0:
                messagebox.showinfo("Tebrikler!", "Boss yenildi! Maria kurtarıldı!")
                win.destroy()
    def start_boss_battle():
        messagebox.showinfo("Boss", "Boss ortaya çıktı! 30 saniye içinde 'S' tuşuna basarak saldırın!")
        win.bind("<KeyPress-s>", decrease_boss_hp)
        boss_attack()
    def start_obby():
        move_obby()
        win.after(1000, start_boss_battle)
    return win

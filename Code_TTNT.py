import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Danh sách khách mời
guest_list = ["Đạt","Hoàng","Hiếu","Thành","Hà","Dương","An","Lan"]
num_guests = len(guest_list)
table_size = 4  # Số khách tối đa mỗi bàn

# Ma trận điểm thân thiết
relationship_matrix = np.array([
    [0, 2000, 100, 500, 0, 700, 300, 900],
    [2000, 0, 100, 300, 500, 900, 700, 0],
    [100, 100, 0, 900, 300, 0, 500, 700],
    [500, 300, 900, 0, 2000, 700, 100, 100],
    [0, 500, 300, 2000, 0, 900, 700, 100],
    [700, 900, 0, 700, 900, 0, 500, 300],
    [300, 700, 500, 100, 700, 500, 0, 2000],
    [900, 0, 700, 100, 100, 300, 2000, 0]
])

def fitness_function(seating):
    """Tính tổng điểm thân thiết của sơ đồ chỗ ngồi."""
    score = 0
    for table in seating:
        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                score += relationship_matrix[guest_list.index(table[i])]
                [guest_list.index(table[j])]
    return score

def generate_population(size):
    """Tạo quần thể ban đầu."""
    population = []
    for _ in range(size):
        shuffled_guests = random.sample(guest_list, num_guests)
        seating = [shuffled_guests[i:i + table_size] for i in range(0,
        num_guests, table_size)]
        population.append(seating)
    return population

def order_crossover(parent1, parent2):
    """Order Crossover (OX) để giữ danh sách khách hợp lệ."""
    # Chuyển danh sách bàn thành danh sách khách phẳng
    flat_parent1 = sum(parent1, [])
    flat_parent2 = sum(parent2, [])

    cut1, cut2 = sorted(random.sample(range(num_guests), 2))
    child = [None] * num_guests
    child[cut1:cut2] = flat_parent1[cut1:cut2]

    remaining = [guest for guest in flat_parent2 
                if guest not in child]
    
    index = 0
    for i in range(num_guests):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1
    
    # Chia lại thành danh sách bàn
    return [child[i:i + table_size] for i in range(0,
    num_guests, table_size)]



def mutate(seating):
    """Hoán đổi hai khách giữa hai bàn để giữ số lượng cân bằng."""
    table1, table2 = random.sample(range(len(seating)), 2)
    idx1, idx2 = random.randint(0, table_size - 1),
    random.randint(0, table_size - 1)
    seating[table1][idx1], seating[table2][idx2]= seating[table2][idx2],
    seating[table1][idx1]
    return seating

def tournament_selection(population, k=3):
    """Chọn cá thể tốt nhất từ một nhóm ngẫu nhiên."""
    return max(random.sample(population, k), key=fitness_function)

def genetic_algorithm(generations=200, population_size=20):
    """Chạy giải thuật di truyền với các cải tiến."""
    population = generate_population(population_size)
    for _ in range(generations):
        population = sorted(population,
        key=lambda x: -fitness_function(x))
        new_population = population[:2]  # Chọn 2 cá thể tốt nhất
        while len(new_population) < population_size:
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = order_crossover(parent1, parent2)
            if random.random() < 0.1:
                child = mutate(child)
            new_population.append(child)
        population = new_population
    return population[0]

# Giao diện đồ họa
class SeatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tối ưu sắp xếp chỗ ngồi")
        self.root.geometry("500x400")
        
        self.label = tk.Label(root,
                            text="Bảng điểm thân thiết giữa các khách mời",
                            font=("Arial", 12, "bold"))
        self.label.pack(pady=5)
        
        self.table_frame = tk.Frame(root)
        self.table_frame.pack()
        
        for i in range(len(guest_list) + 1):
            for j in range(len(guest_list) + 1):
                if i == 0 and j == 0:
                    text = ""
                elif i == 0:
                    text = guest_list[j-1]
                elif j == 0:
                    text = guest_list[i-1]
                else:
                    text = str(relationship_matrix[i-1][j-1])
                tk.Label(self.table_frame, text=text,
                         width=6, borderwidth=1,
                         relief="solid").grid(row=i, column=j)
        
        self.button = tk.Button(root,
                                text="Sắp xếp chỗ ngồi tối ưu",
                                command=self.run_algorithm)
        self.button.pack(pady=10)
        
        self.result_label = tk.Label(root, text="",
                                    wraplength=400,
                                    justify="left")
        self.result_label.pack(pady=10)

    def run_algorithm(self):
        top_seating = genetic_algorithm()
        result_text = "Sơ đồ chỗ ngồi tối ưu:\n"
        for i, table in enumerate(top_seating):
            result_text += f"Bàn {i+1}: {', '.join(table)}\n"
        self.result_label.config(text=result_text)
        messagebox.showinfo("Kết quả", result_text)

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingApp(root)
    root.mainloop()

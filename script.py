from data import risks, events, probability, events_data, risks_data, lrer, risks_elimination, per, elper
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
er = []
vrer = []
selects = [
    [0] * (len(events_data[i])-1) for i in range(len(events_data))
]
choices = [0] * sum(len(sub[1:]) for sub in events_data)

def calculate_percent_11(risks_list):
    return (sum(risks_list) / 18) * 100 if len(risks_list) > 0 else 0

def calculate_percent_12(event_list):
    return (sum(event_list) / 46) * 100 if len(event_list) > 0 else 0


####################################################################
# 1.1 Визначення можливих джерел появи ризиків
def show_risk_table():
    table_window = tk.Toplevel(root)
    table_window.title("Таблиця джерел ризиків")
    table_window.geometry("800x400")

    tree = ttk.Treeview(table_window, columns=("Risk Source", "Probability"), show="headings")
    
    tree.heading("Risk Source", text="Джерело ризику")
    tree.heading("Probability", text="Імовірність")
    
    tree.column("Risk Source", width=400)
    tree.column("Probability", width=200, anchor="center")
    
    for i in range(len(risks_data)):
        for s in range(len(risks_data[i])):
            tmp = []
            tmp.append(risks_data[i][s])
            if s == 0:
                tmp.append(f"{calculate_percent_11(risks[i]):.2f}%")
            else: 
                tmp.append(risks[i][s-1])
            tree.insert("",tk.END, values=tmp)    

    tree.pack(expand=True, fill=tk.BOTH)


######################################################################
# 1.2 Ідентифікація потенційних ризикових подій

def show_risk_events_table():
    table_window = tk.Toplevel(root)
    table_window.title("Таблиця потенційних ризикових подій")
    table_window.geometry("800x500")

    tree = ttk.Treeview(table_window, columns=("Risk Event", "Probability"), show="headings")
    
    tree.heading("Risk Event", text="Ризикова подія")
    tree.heading("Probability", text="Імовірність")
    
    tree.column("Risk Event", width=400)
    tree.column("Probability", width=200, anchor="center")
    
    for i in range(len(events_data)):
        for s in range(len(events_data[i])):
            tmp = []
            tmp.append(events_data[i][s])

            if s == 0:
                tmp.append(f"{calculate_percent_12(events[i]):.2f}%")
            else: 
                tmp.append(events[i][s-1])
            tree.insert("",tk.END, values=tmp)     

    tree.pack(expand=True, fill=tk.BOTH)


######################################################################
# 2.1 Аналіз ризиків

def show_probability_table():
    table_window = tk.Toplevel(root)
    table_window.title("Таблиця ймовірності настання ризикових подій")
    table_window.geometry("1200x750")

    tree = ttk.Treeview(table_window, columns=("Risk Event", "Probability", "Probability 1", "Probability 2", "Probability 3", "Probability 4", "Probability 5", "Probability 6", "Probability 7", "Probability 8", "Probability 9", "Probability 10", "Er", "Lrer", "Vrer", "Priority"), show="headings")
    
    tree.heading("Risk Event", text="Подія")
    tree.heading("Probability", text="Ймов.")
    for i in range(1, 11):
        tree.heading(f"Probability {i}", text=f"{i}", anchor="center")
    tree.heading("Er", text="ER")
    tree.heading("Lrer", text="LRER")
    tree.heading("Vrer", text="VRER")
    tree.heading("Priority", text="Priority")

    tree.column("Risk Event", width=200)
    tree.column("Probability", width=120, anchor="center")
    for i in range(1, 11):
        tree.column(f"Probability {i}", width=20, anchor="center")
    tree.column("Er", width=30, anchor="center")
    tree.column("Lrer", width=30, anchor="center")
    tree.column("Vrer", width=30, anchor="center")
    tree.column("Priority", width=50, anchor="center")

    ers = []
    for i in range(len(probability)):
        tmp = []
        for s in range(len(probability[i])):
            tmp.append(calculate_er(probability[i][s]))
        ers.append(tmp)

    er = ers

    for i in range(len(lrer)):
        tmp = []
        for j in range(len(lrer[i])):
            tmp.append(lrer[i][j] * ers[i][j])  # Перемножуємо відповідні елементи
        vrer.append(tmp)

    all_vrer_values = [value for sublist in vrer for value in sublist]
    min_vrer = min(all_vrer_values)
    max_vrer = max(all_vrer_values)

    # Функція для визначення пріоритету
    def determine_priority(value):
        if 0.05 <= value < 0.23:
            return "Низький"
        elif 0.23 <= value < 0.41:
            return "Середній"
        elif 0.41 <= value < 0.6:
            return "Високий"
        return ""

    for s in range(len(events_data)):  
        for i in range(len(events_data[s])):  
            tmp = [] 
            tmp.append(events_data[s][i])
            if i != 0:
                tmp.append(events[s][i-1])
                for j in range(len(probability[s][i-1])):
                    tmp.append(probability[s][i-1][j])
                tmp.append(round(ers[s][i-1], 2))
                tmp.append(round(lrer[s][i-1], 2))
                tmp.append(round(vrer[s][i-1], 2))
                tmp.append(determine_priority(vrer[s][i-1]))
                tree.insert("", "end", values=tmp) 
            else:
                for i in range(0, 11):
                    tmp.append("")
                event_prob = round(calculate_event_probability(ers, s) * 100.00, 2)
                color = classify_probability(event_prob)
                tmp.append(f"{event_prob}%")
                item = tree.insert("", "end", values=tmp) 
                tree.tag_configure(f"row-{s}", background=color)
                tree.item(item, tags=(f"row-{s}",))

    tree.pack(expand=True, fill=tk.BOTH)
    label_info = tk.Label(table_window, text=(
        "[0.05; 0.23) - Низький\n"
        "[0.23; 0.41) - Середній\n"
        "[0.41; 0.6) - Високий\n"
        f"Min VRER: {min_vrer}\n"
        f"Max VRER: {max_vrer}"
    ), justify="left", font=("Arial", 10))
    label_info.pack(pady=10)


def calculate_er(probabilities):
        return 0.1 * sum(probabilities)

def calculate_event_probability(er, s):
    er_full = 0
    for i in range(len(er)):
        er_full += sum(er[i])
    return (1/er_full) * sum(er[s])
    
def classify_probability(probability):
    """Класифікує ймовірність і повертає рівень та колір."""
    if probability < 10:
        return "lightgreen"
    elif 10 <= probability <= 25:
        return "green"
    elif 25 < probability < 50:
        return "yellow"
    elif 50 <= probability < 75:
        return "lightred"
    else:
        return "red"
    
######################################################################
# 3 Заходи із зменшення або усунення ризику

def show_risks_elimination():
    table_window = tk.Toplevel(root)
    table_window.title("Заходи із зменшення або усунення ризику")
    table_window.geometry("1200x700")

    canvas = tk.Canvas(table_window)
    scrollbar = tk.Scrollbar(table_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    comboboxes = []
    for i in range(len(events_data)):
        row_boxes = []
        for j in range(len(events_data[i])):
            row = tk.Frame(scrollable_frame)
            row.pack(fill=tk.X, pady=15)

            label = tk.Label(row, text=events_data[i][j], width=60, anchor="w")
            label.pack(side=tk.LEFT)

            if j != 0:
                select = ttk.Combobox(row, values=risks_elimination, width=60)
                select.set(risks_elimination[0])  # За замовчуванням вибираємо перший елемент
                select.pack(side=tk.LEFT, padx=7)
                row_boxes.append(select)

        comboboxes.append(row_boxes)

    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    def save_choices():
        for i in range(len(comboboxes)):
            for j in range(len(comboboxes[i])):
                if comboboxes[i][j] is not None:
                    selected_value = comboboxes[i][j].get()
                    if selected_value in risks_elimination:
                        selects[i][j] = risks_elimination.index(selected_value)
        print(selects)  # Для тестування: вивести масив у консоль

    save_button = tk.Button(table_window, text="Зберегти вибори", command=save_choices)
    save_button.pack(pady=20)



######################################################################
# 4 Моніторинг ризиків розроблення ПЗ
    
def show_monitor_risks():
    table_window = tk.Toplevel(root)
    table_window.title("Моніторинг ризиків")
    table_window.geometry("1200x750")

    columns = ["Event"] + [f"per {i}" for i in range(1, 11)] + ["ERPER"]+ ["ELRER"] + ["EVRER"] + ["Priority"]
    tree = ttk.Treeview(table_window, columns=columns, show="headings")
    
    tree.heading("Event", text="Подія")
    for i in range(1, 11):
        tree.heading(f"per {i}", text=f"per {i}", anchor="center")
    tree.heading("ERPER", text="ERPER")
    tree.heading("ELRER", text="ELRER")
    tree.heading("EVRER", text="EVRER")
    tree.heading("Priority", text="Priority")

    tree.column("Event", width=200)
    for i in range(1, 11):
        tree.column(f"per {i}", width=30, anchor="center")
    tree.column("ERPER", width=40, anchor="center")
    tree.column("ELRER", width=40, anchor="center")
    tree.column("EVRER", width=40, anchor="center")
    tree.column("Priority", width=80, anchor="center")

    def determine_priority1(value):
        if 0.01 <= value < 0.25:
            return "Низький"
        elif 0.25 <= value < 0.49:
            return "Середній"
        elif 0.49 <= value < 0.74:
            return "Високий"
        return ""
    
    evper = []
    erper = []
    for i in range(len(per)):
        tmp = []
        for s in range(len(per[i])):
            tmp.append(calculate_er(per[i][s]))
        erper.append(tmp)

    for i in range(len(elper)):
        tmp = []
        for j in range(len(elper[i])):
            tmp.append(elper[i][j] * erper[i][j])  
        evper.append(tmp)

    all_evper_values = [value for sublist in evper for value in sublist]
    min_evper = min(all_evper_values)
    max_evper = max(all_evper_values)

    for s in range(len(events_data)):  
        for i in range(len(events_data[s])):  
            tmp = [] 
            tmp.append(events_data[s][i])
            if i != 0:
                for j in range(len(per[s][i-1])):
                    tmp.append(per[s][i-1][j])
                tmp.append(round(erper[s][i-1], 2))
                tmp.append(round(elper[s][i-1], 2))
                tmp.append(round(evper[s][i-1], 2))
                tmp.append(determine_priority1(evper[s][i-1]))
                tree.insert("", "end", values=tmp) 
            else:
                for i in range(0, 11):
                    tmp.append("")

    tree.pack(expand=True, fill=tk.BOTH)

    
    label_info = tk.Label(table_window, text=(
        "[0.01; 0.25) - Низький\n"
        "[0.25; 0.49) - Середній\n"
        "[0.49; 0.74) - Високий\n"
        f"Min VRER: {round(min_evper, 2)}\n"
        f"Max VRER: {round(max_evper, 2)}"
    ), justify="left", font=("Arial", 10))
    label_info.pack(pady=10)


######################################################################
# ініціалізацію, меню, кнопок і тд

def exit_app():
    root.quit()

root = tk.Tk()
root.title("Управління ризиками")

menu = tk.Menu(root)
root.config(menu=menu)

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Перегляд", menu=view_menu)

identify_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Ідентифікація ризиків", menu=identify_menu)
identify_menu.add_command(label="Визначення можливих джерел появи ризиків", command=show_risk_table)
identify_menu.add_command(label="Ідентифікація потенційних ризикових подій", command=show_risk_events_table)

analysis_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_command(label="Аналіз ризиків", command=show_probability_table)

planning_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Планування ризиків", menu=planning_menu)
planning_menu.add_command(label="Заходи із зменшення або усунення ризику", command=show_risks_elimination)

monitoring_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label="Моніторинг ризиків", menu=monitoring_menu)
monitoring_menu.add_command(label="Оцінювання ризиків", command=show_monitor_risks)

menu.add_command(label="Вихід", command=exit_app)

root.mainloop()

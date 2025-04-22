import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog

def round_to_nearest_plate(weight):
    plates = [45, 35, 25, 10, 5]
    bar_weight = 45
    if weight < bar_weight:
        return bar_weight

    remaining_weight = (weight - bar_weight) / 2
    total_weight = bar_weight
    used_plates = []

    for plate in plates:
        while remaining_weight >= plate:
            remaining_weight -= plate
            used_plates.append(plate)
            total_weight += plate * 2

    return total_weight

def generate_juggernaut_csv(bench_max, squat_max, deadlift_max, filename):
    training_max = {
        "Bench": bench_max * 0.9,
        "Squat": squat_max * 0.9,
        "Deadlift": deadlift_max * 0.9
    }

    waves = {
        "10s": [60, 70, 75],
        "8s": [60, 75, 80],
        "5s": [70, 75, 80, 85],
        "3s": [75, 80, 85, 90]
    }

    wave_structure = {
        "10s": [(4, 10), (3, 10), (1, 10), (3, 5)],
        "8s": [(4, 8), (3, 8), (1, 8), (3, 5)],
        "5s": [(5, 5), (3, 5), (1, 5), (3, 5)],
        "3s": [(6, 3), (3, 3), (1, 3), (3, 5)]
    }

    deload_percentages = [40, 50, 60]

    week_3_reps = {
        "10s": [(60, 3), (70, 1), (75, 10)],
        "8s": [(60, 3), (75, 1), (80, 8)],
        "5s": [(70, 2), (75, 2), (80, 1), (85, 5)],
        "3s": [(75, 1), (80, 1), (85, 1), (90, 3)]
    }

    csv_data = [["Wave", "Week", "Reps x Sets", "Bench (lbs)", "Squat (lbs)", "Deadlift (lbs)"]]

    for header in csv_data:
        for i in range(len(header)):
            header[i] = f"{header[i]:<60}"

    for wave in waves:
        csv_data.append([f"{wave:<15}", "", "", "", "", ""])
        for week in range(1, 5):
            if week != 3:
                sets, reps = wave_structure[wave][week - 1]
                rep_set_format = f"{reps} x {sets}"

                if week == 4:
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (deload_percentages[1] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (deload_percentages[1] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (deload_percentages[1] / 100))
                else:
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (waves[wave][week - 1] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (waves[wave][week - 1] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (waves[wave][week - 1] / 100))

                csv_data.append([f"{wave:<15}", f"Week {week}", f"{rep_set_format:<15}", f"{bench_weight:<15}", f"{squat_weight:<15}", f"{deadlift_weight:<15}"])
            else:
                for rep_set in week_3_reps[wave]:
                    rep_set_format = f"{rep_set[0]}% x {rep_set[1]} reps"
                    bench_weight = round_to_nearest_plate(training_max["Bench"] * (rep_set[0] / 100))
                    squat_weight = round_to_nearest_plate(training_max["Squat"] * (rep_set[0] / 100))
                    deadlift_weight = round_to_nearest_plate(training_max["Deadlift"] * (rep_set[0] / 100))

                    csv_data.append([f"{wave:<15}", f"Week 3", f"{rep_set_format:<15}", f"{bench_weight:<15}", f"{squat_weight:<15}", f"{deadlift_weight:<15}"])

        csv_data.append(["", "", "", "", "", ""])

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    messagebox.showinfo("Success", f"CSV file saved as:\n{filename}")

def calculate_max(weight, reps):
    try:
        weight = float(weight)
        reps = int(reps)
        return round(weight * (1 + (0.0333 * reps)), 2)
    except ValueError:
        return 0.0

def on_generate():
    try:
        bench = calculate_max(bench_weight.get(), bench_reps.get())
        squat = calculate_max(squat_weight.get(), squat_reps.get())
        deadlift = calculate_max(deadlift_weight.get(), deadlift_reps.get())

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save your Juggernaut Program"
        )

        if save_path:
            generate_juggernaut_csv(bench, squat, deadlift, save_path)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# UI Setup
root = tk.Tk()
root.title("Juggernaut Max Calculator")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="Estimated Max Calculator (Weight × Reps)").grid(column=0, columnspan=4, pady=(0, 10))

# Bench Input
ttk.Label(frame, text="Bench Weight").grid(column=0, row=1)
bench_weight = ttk.Entry(frame)
bench_weight.grid(column=1, row=1)

ttk.Label(frame, text="Reps").grid(column=2, row=1)
bench_reps = ttk.Entry(frame)
bench_reps.grid(column=3, row=1)

# Squat Input
ttk.Label(frame, text="Squat Weight").grid(column=0, row=2)
squat_weight = ttk.Entry(frame)
squat_weight.grid(column=1, row=2)

ttk.Label(frame, text="Reps").grid(column=2, row=2)
squat_reps = ttk.Entry(frame)
squat_reps.grid(column=3, row=2)

# Deadlift Input
ttk.Label(frame, text="Deadlift Weight").grid(column=0, row=3)
deadlift_weight = ttk.Entry(frame)
deadlift_weight.grid(column=1, row=3)

ttk.Label(frame, text="Reps").grid(column=2, row=3)
deadlift_reps = ttk.Entry(frame)
deadlift_reps.grid(column=3, row=3)

# Generate Button
ttk.Button(frame, text="Generate Juggernaut Program CSV", command=on_generate).grid(column=0, columnspan=4, pady=20)

root.mainloop()

import random

class Horse:
    def set_details(self, horse_id, horse_name, jockey_name, age, breed, race_record, group):
        self.horse_id = horse_id
        self.horse_name = horse_name
        self.jockey_name = jockey_name
        self.age = age
        self.breed = breed
        self.race_record = race_record
        self.group = group

def is_number(input_str):
    return input_str.isdigit()

def add_horse(horses, race_started):
    if race_started:
        print("Cannot add horse details after the race has started.")
        return

    horse = Horse()
    horse.horse_id = input("Enter Horse ID: ")
    horse.horse_name = input("Enter Horse Name: ")
    horse.jockey_name = input("Enter Jockey Name: ")

    while True:
        age = input("Enter Age: ")
        if is_number(age):
            break
        else:
            print("Age must contain only numbers. Please try again.")

    horse.age = age
    horse.breed = input("Enter Breed: ")
    horse.race_record = input("Enter Race Record: ")
    horse.group = input("Enter Group (A, B, C, D): ").upper()

    horses.append(horse)
    print("Horse details added successfully!")

def update_horse(horses):
    horse_id = input("Enter Horse ID to update: ")
    for horse in horses:
        if horse.horse_id == horse_id:
            horse.horse_name = input("Enter updated Horse Name: ") or horse.horse_name
            horse.jockey_name = input("Enter updated Jockey Name: ") or horse.jockey_name

            age = input("Enter updated Age (press Enter to skip): ")
            if age:
                while not is_number(age):
                    print("Age must contain only numbers. Please try again.")
                    age = input("Enter updated Age: ")
                horse.age = age

            horse.breed = input("Enter updated Breed: ") or horse.breed
            horse.race_record = input("Enter updated Race Record: ") or horse.race_record
            horse.group = input("Enter updated Group (A, B, C, D): ").upper() or horse.group

            print("Horse details updated successfully!")
            return
    print("Horse not found!")

def delete_horse(horses):
    horse_id = input("Enter Horse ID to delete: ")
    for horse in horses:
        if horse.horse_id == horse_id:
            horses.remove(horse)
            print("Horse details deleted successfully!")
            return
    print("Horse not found!")

def save_to_file(horses):
    with open("horse_details.txt", "w") as file:
        for horse in horses:
            file.write(f"{horse.horse_id},{horse.horse_name},{horse.jockey_name},{horse.age},{horse.breed},{horse.race_record},{horse.group}\n")
    print("Horse details saved to file!")

def load_from_file():
    horses = []
    try:
        with open("horse_details.txt", "r") as file:
            for line in file:
                data = line.strip().split(',')
                horse = Horse()
                horse.set_details(*data)
                horses.append(horse)
    except FileNotFoundError:
        pass
    return horses

def bubble_sort_horses(horses):
    n = len(horses)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if int(horses[j].horse_id) > int(horses[j + 1].horse_id):
                horses[j], horses[j + 1] = horses[j + 1], horses[j]

def view_horses(horses):
    if not horses:
        print("No horses registered.")
        return


    bubble_sort_horses(horses)

    print("Horse ID | Horse Name | Jockey Name | Age | Breed | Race Record | Group")
    for horse in horses:
        print(f"{horse.horse_id} | {horse.horse_name} | {horse.jockey_name} | {horse.age} | {horse.breed} | {horse.race_record} | {horse.group}")


    save_to_file(horses)

def select_horses_for_race(horses):
    selected_horses = {}
    groups = ['A', 'B', 'C', 'D']

    for group in groups:
        group_horses = [horse for horse in horses if horse.group == group]

        if group_horses:
            selected_horse = random.choice(group_horses)
            selected_horses[group] = selected_horse
        else:
            print(f"Not enough horses in Group {group} for the final round.")

    if selected_horses:
        print("Randomly selected horses for the race:")
        for group, horse in selected_horses.items():
            print(f"Group {group}: {horse.horse_name}")

    return selected_horses

def sort_race_results(results):
    # Custom sorting function
    sorted_results = []
    while results:
        min_horse, min_time = results[0]
        for horse, time in results:
            if time < min_time:
                min_horse, min_time = horse, time
        sorted_results.append((min_horse, min_time))
        results.remove((min_horse, min_time))
    return sorted_results

def simulate_race(selected_horses):
    race_results = {}

    global horse
    for group, horse in selected_horses.items():
        race_time = random.randint(0, 90)
        race_results[horse] = race_time

    global sorted_results
    sorted_results = sort_race_results(list(race_results.items()))

    print("Race Results:")
    for i, (horse, time) in enumerate(sorted_results[:3], start=1):
        print(f"Horse{i}: {horse.horse_name}\n {time}s (Place {i})")

    return sorted_results

def visualize_race_time(sorted_results):
    if sorted_results is None or not sorted_results:
        print("No race has been simulated yet.")
        return

    print("\nVisualizing Winning Horses:")
    for i, (horse, time) in enumerate(sorted_results[:3], start=1):
        print(f"\nGroup {horse.group}: {horse.horse_name}")
        print(f"{horse.horse_name}: {'*' * (time // 10 * 2)} {time}s ")

def main():
    horses = load_from_file()
    race_started = False
    selected_horses = None  

    while True:
        print("\nCommand Menu:")
        print("Type AHD for adding horse details.")
        print("Type UHD for updating horse details.")
        print("Type DHD for deleting horse details.")
        print("Type VHD for viewing the registered horses’ details table.")
        print("Type SDD for selecting four horses randomly for the major round.")
        print("Type WHD for displaying the Winning horses’ details.")
        print("Type VWH for Visualizing the time of the winning horses.")
        print("Type ESC to exit the program.")

        choice = input("Enter your choice: ").upper()

        if choice == 'AHD' and not race_started:
            add_horse(horses, race_started)
        elif choice == 'UHD' and not race_started:
            update_horse(horses)
        elif choice == 'DHD' and not race_started:
            delete_horse(horses)
        elif choice == 'VHD':
            view_horses(horses)
        elif choice == 'SDD' and not race_started:
            selected_horses = select_horses_for_race(horses)
            race_started = True
        elif choice == 'WHD' and race_started:
            sorted_results = simulate_race(selected_horses)
        elif choice == 'VWH' and race_started:
            visualize_race_time(sorted_results)
        elif choice == 'ESC':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

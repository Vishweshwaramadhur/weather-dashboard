from datetime import datetime

sevas = [
    {"name": "Shashwatha Pooja", "rupees": 1000},
    {"name": "Mahapooja", "rupees": 400},
    {"name": "Alankara Pooje", "rupees": 1000},
    {"name": "Ramanavami", "rupees": 300},
    {"name": "Somavara Pooje", "rupees": 100},
    {"name": "Panchamrutha Abhisheka", "rupees": 20},
    {"name": "Panchakajjaya", "rupees": 20},
    {"name": "Tulabara", "rupees": 51},
    {"name": "Vanamala", "rupees": 30},
    {"name": "Thulasidala", "rupees": 20},
    {"name": "Bonda Abhisheka", "rupees": 20},
    {"name": "Nithya Pooje", "rupees": 75},
    {"name": "Ganapathi Homam (Individual)", "rupees": 500},
    {"name": "Kumkuma Archana (Individual)", "rupees": 5},
    {"name": "Deepa Seva – Night", "rupees": 20},
    {"name": "Deepa Seva – Morning", "rupees": 20},
    {"name": "Kumkumarchana", "rupees": 10},
    {"name": "Karthika Pooja", "rupees": 100},
    {"name": "Pushpalankara Pooja", "rupees": 100},
    {"name": "Thottilu Magu", "rupees": 101},
    {"name": "Vahana Pooje", "rupees": 20},
    {"name": "Payasa", "rupees": 30}
]

def select_and_bill():
    print("\nSevas Available at Sri Ramanatha Temple:\n")
    for i, seva in enumerate(sevas, 1):
        print(f"{i}. {seva['name']} - ₹{seva['rupees']}")
    print()

    try:
        nums = input("Select seva numbers (e.g. 1,3,5): ")
        indexes = [int(n.strip()) - 1 for n in nums.split(",")]
        selected_sevas = [sevas[i] for i in indexes if 0 <= i < len(sevas)]

        if not selected_sevas:
            print("No valid seva numbers entered.")
            return

        # Get current date and time
        now = datetime.now()
        date_time = now.strftime("%d-%m-%Y %I:%M %p")

        print("\n==============================")
        print("  Sri Ramanatha Temple Seva Bill")
        print("==============================")
        print(f"🕒 Date & Time: {date_time}")
        print("------------------------------")
        
        total = 0
        for seva in selected_sevas:
            print(f"{seva['name']} - ₹{seva['rupees']}")
            total += seva["rupees"]
        
        print("------------------------------")
        print(f"Total Amount to Pay: ₹{total}")
        print("==============================\n")

    except Exception:
        print("❌ Invalid input. Please enter valid numbers like 1,2,3.")

def main():
    while True:
        print("\n--- Sri Ramanatha Temple Seva Manager ---")
        print("1. Select Seva and Get Bill")
        print("2. Exit")
        choice = input("Choose an option (1-2): ")

        if choice == "1":
            select_and_bill()
        elif choice == "2":
            print("🙏 Thank you! Visit again.")
            break
        else:
            print("Invalid option. Please select 1 or 2.")

if __name__ == "__main__":
    main()

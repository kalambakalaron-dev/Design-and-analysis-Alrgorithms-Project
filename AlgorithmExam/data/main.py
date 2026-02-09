import csv
import time
import os
import threading
import sys

def load_all_records(path):
    all_rows = []
    if not os.path.exists(path):
        print(f"\n[!] Error: File not found at {path}")
        print("[!] Make sure the CSV is in the 'data' folder.")
        return None
    
    try:
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_rows.append({
                    'ID': int(row['ID']),
                    'FirstName': row['FirstName'],
                    'LastName': row['LastName']
                })
        return all_rows
    except Exception as e:
        print(f"Error reading records: {e}")
        return None

def play_spinner(stop_event):
    chars = ['|', '/', '-', '\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\r[Status] Processing... {chars[i % 4]} ')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write('\r[Done] Task completed!            \n')

def bubble_sort(data, col):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j][col] > arr[j + 1][col]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def insertion_sort(data, col):
    arr = data.copy()
    for i in range(1, len(arr)):
        val = arr[i]
        pos = i - 1
        while pos >= 0 and arr[pos][col] > val[col]:
            arr[pos + 1] = arr[pos]
            pos -= 1
        arr[pos + 1] = val
    return arr

def merge_sort(data, col):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], col)
    right = merge_sort(data[mid:], col)
    return merge_logic(left, right, col)

def merge_logic(left, right, col):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][col] < right[j][col]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:]); res.extend(right[j:])
    return res

def record_lookup(data):
    print("\n--- RECORD SEARCH ---")
    query = input("Enter partial ID or Name: ").lower()
    
    matches = []
    for r in data:
        if query in str(r['ID']) or query in r['FirstName'].lower():
            matches.append(r)
        if len(matches) >= 5:
            break
            
    if not matches:
        print("No matching records found.")
        return

    print(f"\nSuggestions for '{query}':")
    for i, item in enumerate(matches, 1):
        print(f"[{i}] ID: {item['ID']} | {item['FirstName']} {item['LastName']}")
    
    pick = input("\nType a number to select (or 0 to cancel): ")
    if pick.isdigit() and 0 < int(pick) <= len(matches):
        s = matches[int(pick) - 1]
        print("\n" + "*"*30)
        print("      FULL RECORD")
        print("*"*30)
        print(f"ID:         {s['ID']}")
        print(f"FIRST NAME: {s['FirstName']}")
        print(f"LAST NAME:  {s['LastName']}")
        print("*"*30)
    else:
        print("Selection cancelled.")

def main():
    file_path = os.path.join("data", "generated_data (2).csv")
    
    print("---------------------------------------------")
    print("      Prelim Lab: Record Search & Sort       ")
    print("---------------------------------------------")
    
    master_list = load_all_records(file_path)
    if master_list is None:
        return

    while True:
        print("\n[MAIN MENU]")
        print("1. Record Search (Lookup)")
        print("2. Algorithm Stress Test (Benchmark)")
        print("3. Exit")
        
        choice = input("\nChoice: ")

        if choice == '1':
            record_lookup(master_list)
            input("\nPress Enter to return...")

        elif choice == '2':
            try:
                n_input = input("\nHow many records to process (N)? ")
                if not n_input.isdigit():
                    print("Error: You must enter a number (e.g., 1000).")
                    continue
                
                n = int(n_input)
                col = input("Sort by (ID, FirstName, or LastName): ")
                
                print("\nAlgorithms: A (Bubble), B (Insertion), C (Merge)")
                alg_choice = input("Choice: ").lower()

                sample = master_list[:n]
                stop = threading.Event()
                t = threading.Thread(target=play_spinner, args=(stop,))

                start_time = time.time()
                t.start()

                if alg_choice == 'a':
                    sorted_data = bubble_sort(sample, col)
                elif alg_choice == 'b':
                    sorted_data = insertion_sort(sample, col)
                elif alg_choice == 'c':
                    sorted_data = merge_sort(sample, col)
                else:
                    stop.set()
                    print("Invalid algorithm.")
                    continue

                stop.set()
                t.join()
                end_time = time.time()

                print("\n--- PREVIEW (TOP 5) ---")
                for r in sorted_data[:5]:
                    print(f"{r['ID']} | {r['FirstName']} {r['LastName']}")
                
                print(f"\nTime Taken: {end_time - start_time:.4f} seconds")
                input("\nPress Enter to return...")

            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '3':
            print("Closing system...")
            break

if __name__ == "__main__":
    main()
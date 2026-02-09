import csv
import time
import os

# --- DATA LAYER: LOADING AND SEARCHING ---

def load_database(file_path):
    """Loads the CSV data into a list of dictionaries for processing."""
    data_storage = []
    if not os.path.exists(file_path):
        print(f"\n[!] SYSTEM ERROR: The file '{file_path}' was not found.")
        print("[!] Please ensure the 'data' folder contains your CSV file.")
        return None
    
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data_storage.append({
                    'ID': int(row['ID']),
                    'FirstName': row['FirstName'],
                    'LastName': row['LastName']
                })
        return data_storage
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def find_matches(dataset, user_query):
    """Filters data based on ID prefix or Name and returns top 5 results."""
    matches = []
    query_clean = str(user_query).strip().lower()
    
    for record in dataset:
        # Check if ID starts with query OR if FirstName contains the query
        if str(record['ID']).startswith(query_clean) or query_clean in record['FirstName'].lower():
            matches.append(record)
        
        # We limit to 5 results to keep the numbering system simple
        if len(matches) >= 5:
            break
    return matches


# --- ALGORITHM LAYER: THE CORE REQUIREMENTS ---

def bubble_sort_logic(arr, col_name):
    """Standard O(n^2) Bubble Sort implementation."""
    temp_list = arr.copy()
    size = len(temp_list)
    for i in range(size):
        for j in range(0, size - i - 1):
            if temp_list[j][col_name] > temp_list[j + 1][col_name]:
                # Perform the swap
                temp_list[j], temp_list[j + 1] = temp_list[j + 1], temp_list[j]
    return temp_list

def insertion_sort_logic(arr, col_name):
    """Standard O(n^2) Insertion Sort implementation."""
    temp_list = arr.copy()
    for i in range(1, len(temp_list)):
        key_item = temp_list[i]
        j = i - 1
        while j >= 0 and temp_list[j][col_name] > key_item[col_name]:
            temp_list[j + 1] = temp_list[j]
            j -= 1
        temp_list[j + 1] = key_item
    return temp_list

def merge_sort_logic(arr, col_name):
    """Optimized O(n log n) Merge Sort implementation."""
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_side = merge_sort_logic(arr[:mid], col_name)
    right_side = merge_sort_logic(arr[mid:], col_name)
    
    return merge_helper(left_side, right_side, col_name)

def merge_helper(left, right, col_name):
    sorted_arr = []
    left_idx = right_idx = 0
    
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx][col_name] < right[right_idx][col_name]:
            sorted_arr.append(left[left_idx])
            left_idx += 1
        else:
            sorted_arr.append(right[right_idx])
            right_idx += 1
            
    sorted_arr.extend(left[left_idx:])
    sorted_arr.extend(right[right_idx:])
    return sorted_arr


# --- PRESENTATION LAYER: USER INTERFACE ---

def main_menu():
    # SET YOUR FILE PATH HERE
    TARGET_FILE = "data/generated_data (2).csv"
    
    print("------------------------------------------------")
    print("  PRELIM EXAM: ALGORITHM COMPLEXITY ANALYSIS   ")
    print("------------------------------------------------")
    print("[Status] Initializing system and loading data...")
    
    master_data = load_database(TARGET_FILE)
    if master_data is None:
        return

    while True:
        print("\n================ MAIN CONTROL MENU ================")
        print("1. [Quick Search] Find & Select a Student")
        print("2. [Benchmark] Run Algorithm Stress Tests")
        print("3. [Exit] Shut Down System")
        print("===================================================")
        
        main_choice = input("\nEnter your choice (1-3): ")

        if main_choice == '1':
            search_input = input("\nEnter partial ID or First Name to search: ")
            results = find_matches(master_data, search_input)
            
            if not results:
                print(">>> No matching records found.")
            else:
                print(f"\nShowing top {len(results)} matches:")
                print(f"{'No.':<4} | {'ID Number':<12} | {'Full Name'}")
                print("-" * 40)
                for i, r in enumerate(results, 1):
                    print(f"[{i}]  | {r['ID']:<12} | {r['FirstName']} {r['LastName']}")
                
                print("\n[0] Cancel selection")
                pick = input("\nType the number to select the person: ")
                
                if pick.isdigit() and 0 < int(pick) <= len(results):
                    chosen = results[int(pick) - 1]
                    print("\n[!] RECORD FULLY ACCESSED:")
                    print(f"    - ID: {chosen['ID']}")
                    print(f"    - NAME: {chosen['FirstName']} {chosen['LastName']}")
                else:
                    print("Selection cancelled.")
            input("\nPress Enter to return to Menu...")

        elif main_choice == '2':
            try:
                print("\n--- BENCHMARK CONFIGURATION ---")
                n_size = int(input("How many rows to sort? (1000/10000/100000): "))
                sort_col = input("Sort by which column? (ID/FirstName/LastName): ")
                
                print("\nChoose Algorithm:")
                print("A. Bubble Sort (O(n^2))")
                print("B. Insertion Sort (O(n^2))")
                print("C. Merge Sort (O(n log n))")
                alg_choice = input("Choice (A/B/C): ").upper()

                # Slice the data according to N
                test_set = master_data[:n_size]

                # Performance warning
                if n_size >= 100000 and alg_choice in ['A', 'B']:
                    print("\n!!! WARNING: O(n^2) algorithm detected for 100k records.")
                    print("!!! This will take 15-30 minutes of CPU processing.")
                    confirm = input("Are you sure? (y/n): ")
                    if confirm.lower() != 'y': continue

                print(f"\n[Status] Sorting {n_size} records by {sort_col}...")
                start_time = time.time()

                if alg_choice == 'A':
                    sorted_list = bubble_sort_logic(test_set, sort_col)
                elif alg_choice == 'B':
                    sorted_list = insertion_sort_logic(test_set, sort_col)
                elif alg_choice == 'C':
                    sorted_list = merge_sort_logic(test_set, sort_col)
                else:
                    print("Invalid algorithm selection.")
                    continue

                end_time = time.time()
                total_time = end_time - start_time

                print("\n--- SORTING COMPLETE ---")
                print(f"Top 5 Results:")
                for r in sorted_list[:5]:
                    print(f" >> {r['ID']} | {r['FirstName']} {r['LastName']}")
                
                print(f"\n>>> FINAL TIME: {total_time:.4f} seconds")
                input("\nPress Enter to return to Menu...")

            except ValueError:
                print("Invalid input. N must be a number.")

        elif main_choice == '3':
            print("\nExiting system. Final reports saved in memory.")
            break
        else:
            print("Invalid Menu Choice.")

if __name__ == "__main__":
    main_menu()
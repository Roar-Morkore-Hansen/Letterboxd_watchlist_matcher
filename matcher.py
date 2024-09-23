import csv
import glob
from itertools import combinations

def get_list_keys(dict):
    keyList = []
    for (k, v) in dict.items():
        keyList.append(k)
    return(keyList)

def get_combos(list):
    combos = []
    
    # Generate sublists of lengths from 2 to len(input_list)-1
    for r in range(2, len(list) + 1):
        combos.extend(combinations(list, r))
    
    return combos

def extract_name_from_path(file_path):
    # Split the path by '/' and get the last part (filename)
    filename = file_path.split('/')[-1]
    # Remove the file extension to get the name
    name = filename.split('.')[0]
    return name

def get_files_from_dirc(path):
    return glob.glob(path + "/*.csv")

def extract_movie_names_from_csv(filename, collumName):
    values = []
    try:
        with open(filename, mode='r') as file:
            csv_reader = csv.DictReader(file)  # Use DictReader to access columns by header
            for row in csv_reader:
                if collumName in row:  # Check if the 'name' column exists
                    values.append(row[collumName])  # Extract the 'name' value
                else:
                    print("Error: 'name' column not found in the CSV file.")
                    return None
        return values
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return None

def files_to_dictonary(fileList):
    dict = {}
    for file in fileList:
        dict[extract_name_from_path(file)] = extract_movie_names_from_csv(file, "Name")
    return dict


def find_movie_overlap(keys, data_dict):
    # Extract movie lists for the specified keys
    movie_lists = [set(data_dict[key]) for key in keys if key in data_dict]
    
    # Find the intersection of all movie lists
    common_movies = set.intersection(*movie_lists) if movie_lists else set()
    
    return list(common_movies)

data_dict = files_to_dictonary(get_files_from_dirc('data'))


users = get_list_keys(data_dict)
userCombs = get_combos(users)


for keys in userCombs:
    overlap = find_movie_overlap(keys, data_dict)

    print("=" * 20)
    print(keys)
    print("-" * 20)
    for movie in overlap:
        print(movie)


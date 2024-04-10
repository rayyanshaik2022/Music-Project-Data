import json
import os


# with open(f"{output_dir}/data2.json", "w") as json_file:
#         json.dump(lyrics, json_file)

            

def read_and_merge(file1, file2):
    with open(file1, "r") as json_file:
        data1 = json.load(json_file)
    with open(file2, "r") as json_file:
        data2 = json.load(json_file)


    data1.update(data2)

    return data1
        

def save_dictionary(dict, output_file):
    with open(output_file, "w") as json_file:
        json.dump(dict, json_file)


if __name__ == "__main__":
        
    file1 = "lyrics/clean_data_full.json"
    file2 = "lyrics/clean_missing_data.json"

    combined = read_and_merge(file1, file2)
    print(len(combined.keys()))

    output_file = "lyrics/clean_data_full.json"
    save_dictionary(combined, output_file)
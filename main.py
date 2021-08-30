import json

global master_dict


def get_prof(name):
    for professor in master_dict["Professors"]:
        if name.lower() in professor.lower():
            for key in master_dict["Professors"][professor]:
                print(master_dict["Professors"][professor][key])


if __name__ == "__main__":
    input_file = open("updated.json")
    master_dict = json.load(input_file)

    get_prof("Santosh")

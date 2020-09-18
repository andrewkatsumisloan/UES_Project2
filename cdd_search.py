import re
import json
import pprint
import os
import sys

# Export CDD in .tsv format, vi the file, remove garbage lines.
# Dependency on CDD in .tsv form.

def read_input(input_json):
    """
    Read input file
    :param input_json: json file containing terms to be searched.
    :return: JSON file as dict
    """
    with open('Data/attribute_inputs.json') as f:
        attributes = json.load(f)
    return attributes


# Make a list of all keys from the JSON input file
def list_key(attributes):
    """
    Makes a list of all of the keys from the JSON input file (flattened list of all keys)
    :param attributes:
    :return: list of all keys in dict
    """
    all_attr = []
    for key in attributes.keys():
        val = attributes[key]
        all_attr.append(key)
        all_attr.extend(list(val.keys()))
    return all_attr


def load_cdd():
    """
    Function that returns a list of dictionaries, where each row in the CDD becomes a dictionary.
    :return: list of dictionaries
    """
    # Open CDD Dict, save as list
    handle = open('Data/CompleteAMCDD-Table.tsv', 'r')
    lines = handle.readlines()
    print(len(lines))
    handle.close()

    keys = re.split('\t', lines[0])[1:9]
    # print(keys)
    dict_list = []
    for line in lines[1:]:
        values = re.split('\t', line)[1:9]
        new_dict = {}
        for i, value in enumerate(values):
            new_dict[keys[i]] = value
        dict_list.append(new_dict)
    return dict_list
    # print(dict_list)


def search_cdd(dict_list, all_attr):
    """
    Searches the cdd for each of the attributes in the all_attr list.
    :param dict_list: list of dictionaries where each element in list is derived from row of CDD
    :param all_attr: list of all attributes taken from input JSON
    :return: dictionary containing all potential matches
    """
    # For each dictionary in the list of dictionaries called dict_list
    all_dict = {}
    for attr in range(0, len(all_attr)):
        # Each row is a dictionary for each line in the CDD
        all_dict[all_attr[attr]] = []
        for row in dict_list:
            if 'Data Element Name' in row.keys() and all_attr[attr] in row['Data Element Name']:
                # print(row['ID'], ':', row['Data Element Name'], ';', row['Definition'])

                # If attr match in 'Data Element Name', populate temporary dictionary with relevant keys+values.
                temp_dict = {}
                temp_dict['ID'] = row['ID']
                temp_dict['Data Element Name'] = row['Data Element Name']
                temp_dict['Definition'] = row['Definition']
                all_dict[all_attr[attr]].append(temp_dict)
    return all_dict


def user_input(prompt, options):
    """
    Prompts user to select best match, overwrites all_dict to only contain matches selected by user.
    :param prompt: string that prompts user to select the best match for each potential match
    :param options: potential matches found
    :return: user selected match
    """
    print(prompt)
    for i, option in enumerate(options):
        print("   {0} {1:30} {2}".format(i+1, option['Data Element Name'], option['Definition']))
    print("Choose one.")
    answer = input()
    return answer

if __name__ == "__main__":
    # Enter the attributes.json files (#1)
    # Enter the path to the output JSON file (#2)
    input_json = sys.argv[1]
    file_path = sys.argv[2]

    # Load the common data dictionary into a list, where each row is a dictionary.
    dict_list = load_cdd()

    # Read in the JSON file as dict
    list_attr = read_input(input_json)

    # Make list comprised of all attributes from JSON file.
    all_attr = list_key(list_attr)

    # Search the CDD for all of the attributes extracted from the input JSON file.  Store result in all_dict.
    all_dict = search_cdd(dict_list, all_attr)

    for key in all_dict:
        if all_dict[key]:
            answer = user_input('Choose the best match for {}'.format(key), all_dict[key])
            while int(answer)-1 >= len(all_dict[key]) or int(answer)-1 < 0:
                print('Please choose number between: {0} and {1}'.format(1, len(all_dict[key])))
                answer = input()
            all_dict[key] = all_dict[key][int(answer)-1]

    # Dump into file, close.
    handle = open(sys.argv[2], 'w')
    json.dump(all_dict, handle)
    handle.close()

    # Print output
    pp = pprint.PrettyPrinter()
    pp.pprint(all_dict)

# Output is a dictionary, where each key is an attribute.
# The value that corresponds to the key is a list of dictionaries where each dictionary is a matching term in the CDD.



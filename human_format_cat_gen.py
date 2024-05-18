import yaml

CATEGORIES_RAW_FILENAME = "categories.yaml"

# transform the categories inside given yaml file file into pairs of the original category and its human readable format
#   defined by rules in 'categories_syntax.txt

def include_category_name(category_name, cur_path, cur_human_path):
    # remove emoji
    if("|" in category_name):
        category_name = category_name.split("|")
        category_name = category_name[0].strip()

    if(category_name.startswith("^+")):
        if(len(cur_path) == 0):
            raise Exception(f"'^+' is specified for {category_name} but there is no parent category")
        category_name = category_name[2:]
        cur_human_path.append(cur_path[-1])
        cur_human_path.append(category_name)
    elif(category_name.startswith("^")):
        if(len(cur_path) == 0):
            raise Exception(f"'^' is specified for {category_name} but there is no parent category")
        category_name = category_name[1:]
        if(cur_path[-1] != cur_human_path[-1]):
            cur_human_path.append(cur_path[-1])
    elif(category_name.startswith("?")):
        category_name = category_name[1:]
    else:
        cur_human_path.append(category_name)

    cur_path.append(category_name)

def visit(categories_dict, categories_list, cur_path, cur_human_path):
    if(categories_list == None):
        return
    
    # if it is the final category
    if not isinstance(categories_list, dict) and type(categories_list) is not list:
        if(len(cur_human_path) == 0):
            return
        cur_path_str = "_".join(cur_path)
        cur_human_path_str = "_".join(cur_human_path)

        if(cur_human_path_str in categories_dict):
            print(f"WARNING: Categories {categories_dict[cur_human_path_str]} and {cur_path_str} have the same human readable form ({cur_human_path_str})")
        categories_dict[cur_human_path_str] = cur_path_str
        return

    for subcategory in categories_list:
        cur_path_copy = cur_path.copy()
        cur_human_path_copy = cur_human_path.copy()

        # if it is the final category
        if not isinstance(subcategory, dict):
            subcategory_name = subcategory
            include_category_name(subcategory_name, cur_path_copy, cur_human_path_copy)
            visit(categories_dict, subcategory, cur_path_copy, cur_human_path_copy)
        else:
            # take one and only key
            subcategory_key = next(iter(subcategory))
            subcategory_name = subcategory_key
            include_category_name(subcategory_name, cur_path_copy, cur_human_path_copy)
            visit(categories_dict, subcategory[subcategory_key], cur_path_copy, cur_human_path_copy)


def generate():
    with open(CATEGORIES_RAW_FILENAME, 'r', encoding='utf-8') as file:
        categories_raw = yaml.safe_load(file)

    categories_dict = {}
    visit(categories_dict, categories_raw, [], [])
    return categories_dict

        
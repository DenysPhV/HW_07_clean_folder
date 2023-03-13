from typing import Dict, List
import re
import os
import shutil
import os.path
import sys


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "y", "j",
               "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h",
               "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "je", "i", "ji", "g")


TRANSLITERATION_DICT = {}


for cyr, lat in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANSLITERATION_DICT[ord(cyr)] = lat
    TRANSLITERATION_DICT[ord(cyr.upper())] = lat.upper()


def normalize(name):
    translate_name = name.translate(TRANSLITERATION_DICT)
    idx = translate_name.rfind(".")
    translate_name = re.sub(r'\W', '_', translate_name[0:idx]) + translate_name[idx:]
    return translate_name


ARCHIVES = "archives"
UNKNOWN = "unknown"

CATEGORIES: Dict[str, List] = {
    "images": ['jpeg', 'png', 'jpg', 'svg'],
    "videos": ['avi', 'mp4', 'mov', 'mkv'],
    "documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    "music": ['mp3', 'ogg', 'wav', 'amr'],
    "archives": ['zip', 'gz', 'tar'],
    "unknowns": [],
    }

sorted_files_list = []
extensions_set = set()
unknown_ext_set = set()


def define_category(file_path: str):
    global CATEGORIES
    extension = file_path.split(".")[-1]

    for category, category_extensions in CATEGORIES.items():
        if extension in category_extensions:
            extensions_set.add(extension)
            return category

    CATEGORIES[UNKNOWN].append(extension)
    unknown_ext_set.add(extension)
    return UNKNOWN


def unpack_archive(archive_src: str, destination_folder: str):
    shutil.unpack_archive(archive_src, destination_folder)


def move_to_category_folder(src: str, destination: str):
    category = define_category(src)
    destination_folder: str = os.path.join(destination, category)  # - /target/images

    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)

    if category == ARCHIVES:
        unpack_archive(src, destination_folder)
        return

    filename: str = os.path.split(src)[-1]
    new_filename = normalize(filename)
    destination_filepath = os.path.join(destination_folder, new_filename)
    sorted_files_list.append(destination_filepath)
    shutil.move(src, destination_filepath)


def arrange_files_sorting_in_folder(target_path: str, destination_folder: str = None):
    if destination_folder is None:
        destination_folder = target_path

    inner_files = os.listdir(target_path)
    for filename in inner_files:
        file_path: str = os.path.join(target_path, filename)

        if os.path.isdir(file_path):
            arrange_files_sorting_in_folder(file_path)

        elif os.path.isfile(file_path):
            move_to_category_folder(file_path, destination_folder)

        else:
            raise OSError


def main_script():
    try:
        target_folder = sys.argv[1]
    except IndexError:
        print("Folder for sorting was not defined. Please enter path to folder.")
        return

    if not os.path.exists(target_folder):
        print("Indicated folder doesn't exist. Please check path and start process again")
        exit()

    print(f'\nWe start file sorting process in folder -> {target_folder}\n')
    arrange_files_sorting_in_folder(target_folder)
    print(f'Sorting process in progress...\n')
    print(f"Files were sorted successfully. Please check here -> {target_folder}\n")


if __name__ == "__main__":
    main_script()

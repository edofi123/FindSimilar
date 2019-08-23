import os
import random
from PIL import Image


'''Const variables'''
PTC_MUL = 2
PTC_START = 5
PR_START = 30
PR_MUL = 4
MIN = 1
MAX = 5


def rand(min_val, max_val):
    return random.randint(min_val, max_val)


def tuple_calc(my_tuple, num, state):
    val = 1 if state else -1
    return tuple((my_tuple[0] + (num*val), my_tuple[1] + (num*val), my_tuple[2] + (num*val)))


def tuple_between(first, second, third):
    return (first[0] < second[0] < third[0]) and (first[1] < second[1] < third[1]) and (first[2] < second[2] < third[2])


def check_image(file):
    return "jpg" in str(file) or "png" in str(file) or "jpeg" in str(file)


def print_images_name(image_list):
    for image in image_list:
        print(str(image_list.index(image) + 1) + ". " + image)
    print()
    return input()


def starting_program():
    """
    The hello message of the program, get the user's input
    Output: path, accuracy
    """

    print("Hello to findDuplicates created by Edo Fisher!\n"
          "Give a path to a directory to examine: ")
    path = input()
    print("How much accurate you would like it to be? (1 - 5) ")
    accuracy = int(input())
    return path, accuracy


def show_similar(path, similar_dict):
    """
    Shows the user the similar images and let him decide if delete those images or not
    Input: path, similar_dict
    Output: nothing
    """

    print("I found " + str(len(similar_dict)) + " images that match to other images")
    removed_images = []
    # removed_images_size = 0
    for file, similar in similar_dict.items():
        if file in removed_images:
            continue
        for image in [file] + similar:
            if image in removed_images:
                similar.remove(image)
                continue
            os.startfile(path + "\\" + image)
        print("Do you want to remove one of the images? (y/n)")
        ans = input()
        if ans.lower() == 'y':
            print("Choose one of the options:\n"
                  "1. Remove one or couple of images\n"
                  "2. Remove all images except one or couple of them\n"
                  "3. Remove all images")
            ans = input()
            list_of_images = [file] + similar
            list_of_indexes = []
            if ans == "1":
                print("Which images would you like to remove? (leave a space between two numbers)")
                images_to_remove = print_images_name(list_of_images)
                list_of_indexes = images_to_remove.split(' ')
            elif ans == "2":
                print("Which images would you like to keep? (leave a space between two numbers)")
                images_to_keep = print_images_name(list_of_images)
                list_of_indexes = list(range(len(list_of_images)))
                for index in images_to_keep.split(' '):
                    if (int(index) - 1) in list_of_indexes:
                        list_of_indexes.remove(int(index) - 1)
            elif ans == "3":
                list_of_indexes = list(range(len(list_of_images)))
            for index in list_of_indexes:
                if (int(index) - 1) in list(range(len(list_of_images))):
                    os.remove(path + "\\" + list_of_images[int(index) - 1])
                    if image in similar_dict:
                        removed_images.append(image)
    print("That's it!")


def search_similar(path, accuracy):
    """
    Searches similar images inside a directory and put the results in a dictionary
    Input: path, accuracy
    Output: similar_images
    """

    if not (MIN <= accuracy <= MAX):
        accuracy = MIN
    pixels_to_check = accuracy * PTC_MUL + PTC_START
    pixels_range = PR_START - (accuracy * PR_MUL)
    checked_files = []
    similar_images = {}
    open_files = {}
    rand_pixel = []
    dir_files = os.listdir(path)
    # Open all the picture and take details
    print("Loading part 1...")
    for num in range(pixels_to_check):
        rand_pixel.append(rand(10, 100) / 10)
    for file in dir_files:
        if check_image(file):
            info = Image.open(path + '\\' + file)
            pixels = info.load()
            pixels_list = []
            # Choose pixels to examine
            for num in rand_pixel:
                x = int((info.width / num) - 1)
                y = int((info.height / num) - 1)
                pixels_list.append(pixels[x, y])
            open_files[file] = (info.size, pixels_list)
            info.close()
    # Go over all the files in the directory and compare each file to the others
    print("Loading part 2...")
    for name1, info1 in open_files.items():
        for name2, info2 in open_files.items():
            # Check: Not the same file, name2 hasn't checked yet
            if (name1 == name2) or (name2 in checked_files):
                continue
            if info1[0][0] == info2[0][0] and info1[0][1] == info2[0][1]:
                similar = True
                # Compare the pixels
                for x in range(len(info1[1])):
                    if not tuple_between(tuple_calc(info1[1][x], pixels_range, 0), info2[1][x], tuple_calc(info1[1][x], pixels_range, 1)):
                        similar = False
                        break
                if similar:
                    if name1 in similar_images:
                        similar_images[name1].append(name2)
                    else:
                        similar_images[name1] = [name2]
        # Do not double check each file
        checked_files.append(name1)
    return similar_images


def main():
    path, accuracy = starting_program()
    show_similar(path, search_similar(path, accuracy))
    input()


main()

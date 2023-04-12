import random

def print_map(to_print):

    # a function to output a dictionary's key value pairs

    for key, value in to_print.items():

        print(f"{key}: {value}")

def char_to_string(arr):

    # function that returns a string representation of a character array

    str = ""

    for char in arr:

        if char == '\0':

            break

        str += char

    return str

def split_string(str, delim):

    # this is a custom function to split a string

    # returns a list of "words", according to the delimiter character

    

    tokens = str.split(delim)

    return tokens

def get_salt_hash(file, username):

    # this function reads the file (typically shadow.txt) and finds the value corresponding to the specified username

    # the value is then parsed to get the salt and hash (as one string) for this username

    # salt and hash are returned as one string

    salt_hash = ""

    with open(file, "r") as infile:

        for line in infile:

            if username in line:

                tokens = split_string(line, ":")

                salt_hash = tokens[1]

                break

    return salt_hash

def divide_alphabet(slave_procs):

    # this function divides the alphabet characters and assigns certain number of characters to each process

    # also takes into account the case when alphabet is not perfectly divisible by number of slave processes

    # so may also assign master some characters

    # the distribution is stored in a dictionary with (key, value) pair being (process rank, characters assigned)

    # rank 0 is master, rank 1 is slave 1, rank 2 is slave 2 and so on...

    distrib = {}

    alphabet = list("abcdefghijklmnopqrstuvwxyz")

    random.shuffle(alphabet)

    # case 1: alphabet perfectly divisible by number of slaves

    if len(alphabet) % slave_procs == 0:

        chunk = len(alphabet) // slave_procs

        distrib[0] = "" # no letters assigned to master (characters can be evenly distributed among the slaves), still we keep a record for master in case required

        index = 0

        for i in range(1, slave_procs+1):

            start = index

            letters = alphabet[start:start+chunk]

            distrib[i] = letters # assigning letters to that slave rank

            index += chunk

        

    # case 2: alphabet not perfectly divisible, some characters will have to be allotted to master too

    else:

        mod = len(alphabet) % slave_procs

        distrib[0] = alphabet[:mod]

        new_len = len(alphabet) - mod

        mod1 = new_len // slave_procs

        index = mod

        for i in range(1, slave_procs+1):

            start = index

            letters = alphabet[start:start+mod1]

            distrib[i] = letters

            index += mod1

    return distrib


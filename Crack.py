from mpi4py import MPI

import crypt

def are_all_z(str):

    # This function is used to check if a string has only zzzzzz (first character excepted)

    # done by checking string from 2nd character to the end

    # for the edge case of string having only one character

    if len(str) == 1:

        if str[0] == 'z':

            return True

        return False

    # check that all characters save the starting one are z

    for i in range(1, len(str)):

        if str[i] != 'z':

            return False

    return True

def password_cracker(initial, salt_hash):

    # initial: the character whose possibilities have to be traversed e.g. a -> a, ab, ac...abbbd, abbbe... till azzzzzzzz

    # this function traverses through the character's strings, crypts each using the salt and compares the resulting hash to the salt_hash parameter

    # if password is found, function prints result, sends password to master (rank 0 proc) then terminates

    # Split salt and hash from salt_hash parameter

    tokens = salt_hash.split('$')

    salt = '$' + tokens[1] + '$' + tokens[2] + '$'

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()

    found = False  # used to keep track of password being found or not

    current_length = 0  # keep track of which length possibilities are being explored -> 2 characters, 3 characters and so on

    MAX_LENGTH = 8  # maximum string-length to check possibilities upto

    initial_char = initial  # string representation of the initial char parameter

    current = initial_char  # initializing the current string with the initial character

    # run until password is found or max length is exceeded

    while not found and current_length < MAX_LENGTH:

        # incrementing characters till we reach end e.g. azz or azzzz

        while not are_all_z(current) and not found:

            # crypt the current string with constant salt

            crypted = crypt.crypt(current, salt)

            # compare the hash generated to the salt_hash

            if crypted == salt_hash:

                found = True

                print(f"password is {current}")

                # signal master that password has been found (and send the password along)

                if rank != 0:

                    comm.send(current.encode(), dest=0, tag=200)

                break

            else:

                changed = False

                # go backwards in the string till a non-z character is found

                for i in range(len(current) - 1, -1, -1):

                    # convert any z encountered to a (resetting it)

                    if current[i] == 'z':

                        current = current[:i] + 'a' + current[i + 1:]

                        continue

                    # incrementing the first non-z character found from the right

                    if current[i] != 'z':

                        current = current[:i] + chr(ord(current[i]) + 1) + current[i + 1:]

                        # as we only change one character at a time, so we mark that it has been changed

                        changed = True

                        break

                if not changed:

                    break

        # this is so we can check for an all-z string e.g. azz, bzzz

        # if this was not applied, z-strings would be skipped

                if crypted == salt_hash:
            found = True
            print("password is", current)

            # signal master that password has been found (and send the password along)
            comm.send(current.encode(), dest=0, tag=200)
            break

        else:
            changed = False

            # go backwards in the string till a non-z character is found
            for i in range(len(current) - 1, -1, -1):
                # convert any z encountered to a (resetting it)
                if current[i] == 'z':
                    current = current[:i] + 'a' + current[i + 1:]
                    continue

                # incrementing the first non-z character found from the right
                if current[i] != 'z':
                    current = current[:i] + chr(ord(current[i]) + 1) + current[i + 1:]

                    # as we only change one character at a time, so we mark that it has been changed
                    changed = True
                    break

            if not changed:
                break

    # this is so we can check for an all-z string e.g. azz, bzzz
    # if this was not applied, z-strings would be skipped
    crypted = crypt(current, salt)

    if crypted == salt_hash and not found:
        found = True
        print("password is", current)

        # signal master that password has been found (and send the password along)
        comm.send(current.encode(), dest=0, tag=200)

        break

    # string length has to added to now
    current_length += 1

    # resetting the string and incrementing length
    current = initial_char
    for i in range(current_length):
        current += 'a'
Close the communication channels

comm.Disconnect()

End the timer and print the elapsed time

end_time = time.time()

print("Elapsed time:", end_time - start_time, "seconds")


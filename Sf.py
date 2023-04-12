import string

import itertools

import os

import crypt

from mpi4py import MPI

# Function to divide the alphabet among the processes

def divide_alphabet(nprocs):

    alphabet = string.ascii_lowercase

    letter_counts = len(alphabet)

    div_counts = letter_counts // nprocs

    rem_counts = letter_counts % nprocs

    letters_per_process = [div_counts] * nprocs

    for i in range(rem_counts):

        letters_per_process[i] += 1

    distrib = {}

    start_idx = 0

    for i in range(nprocs):

        distrib[i] = alphabet[start_idx:start_idx + letters_per_process[i]]

        start_idx += letters_per_process[i]

    return distrib

# Function to retrieve the salt and hash for a specified username from a file

def get_salt_hash(file_path, username):

    with open(file_path, 'r') as f:

        for line in f:

            fields = line.strip().split(':')

            if fields[0] == username:

                salt_hash = fields[1]

                break

    return salt_hash

# Function to crack the password for a given character and salt+hash

def password_cracker(c, salt_hash):

    for length in range(1, 4):

        for attempt in itertools.product(string.ascii_lowercase, repeat=length):

            pw = ''.join(attempt)

            if crypt.crypt(pw, salt_hash) == salt_hash:

                print(f"Password found: {pw}")

                comm.Abort()

# Main function

if __name__ == '__main__':

    comm = MPI.COMM_WORLD

    rank = comm.Get_rank()

    nprocs = comm.Get_size()

    # Master code

    if rank == 0:

        print(f"Master: there are {nprocs - 1} slave processes")

        username = "project"

        salt_hash = get_salt_hash("/mirror/shadow.txt", username)

        if not salt_hash:

            print("File was not opened, terminating program.")

            comm.Abort()

        distrib = divide_alphabet(nprocs-1)

        for i in range(1, nprocs):

            comm.send(salt_hash, dest=i, tag=100)

            comm.send(distrib[i], dest=i, tag=101)

        if distrib[0]:

            letters = distrib[0]

            print(f"Master: {letters}")

            for i in range(2):

                if i == 0:

                    for letter in letters:

                        password_cracker(letter, salt_hash)

                else:

                    password = comm.recv(source=MPI.ANY_SOURCE, tag=200)

                    print(f"Process {status.Get_source()} has cracked the password: {password}")

                    print("Terminating all processes")

                    comm.Abort()

        else:

            password = comm.recv(source=MPI.ANY_SOURCE, tag=200)

            print(f"Process {status.Get_source()} has cracked the password: {password}")

            print("Terminating all processes")

            comm.Abort()

    # Slave code

    else:

        salt_hash = comm.recv(source=0, tag=100)

        letters = comm.recv(source=0, tag=101)

        print(f"Slave {rank}: {letters}")

        for letter in letters:

            password_cracker(letter, salt_hash)


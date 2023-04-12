# basic-password-cracker
This code is a basic implementation of a password cracker that uses a brute force approach to crack password hashes. The code takes a hash value and salt as input and tries to find the corresponding password for that hash by iterating through all possible combinations of characters.

The program uses MPI (Message Passing Interface) to distribute the workload across multiple processors, which allows for much faster password cracking. The algorithm is simple - it starts by creating a string with the length of 1 and then iterates through all possible combinations of characters for that length. If no match is found, the length is incremented and the process is repeated.

The actual password cracking is done using the crypt() function which is a one-way hash function that takes the password and salt as input and returns a hashed value. The output hash is then compared with the hash that we are trying to crack, and if there is a match, the password is considered cracked.

To speed up the cracking process, the code is optimized by starting with the most probable characters and gradually moving towards less probable characters. For example, it starts by trying all one-letter passwords starting with the most common letters like 'a', 'e', 't', etc., then moves on to two-letter passwords with the most common two-letter combinations like 'aa', 'ab', 'ac', etc.

The code also employs a number of other optimizations to reduce the number of possibilities that need to be tested. For example, it skips all passwords that contain characters that are not allowed in the password, and it also skips all passwords that have already been tested. Additionally, it uses a multi-step process to incrementally search for the password by iterating through all possible combinations of characters and then moving on to the next length if no match is found.

Overall, this code is a basic implementation of a password cracker that uses a brute-force approach to find the password for a given hash. While it is not the most efficient or sophisticated method, it is still effective in cracking simple passwords that are not well-protected

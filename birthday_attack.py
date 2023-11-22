#!/usr/bin/env python3

import sys

from hashlib import sha256

def main():
    if len(sys.argv) != 4:
        print(f"USAGE: python3 {sys.argv[0]} <path_to_real_file> <path_to_fake_file> <number_of_matches>")
        exit(1)

    real_file = sys.argv[1]
    fake_file = sys.argv[2]
    matches = int(sys.argv[3])

    try:
        with open(real_file) as file:
            real = file.read()
        with open(fake_file) as file:
            fake = file.read()
    except Exception as err:
        print(err)
        exit(1)

    real_hashes = {}
    fake_hashes = {}

    collision = None
    while collision is None:
        real_hash = sha256(real.encode()).hexdigest()[-1 * matches:]
        real_hashes[real_hash] = real
        real += ' '

        fake_hash = sha256(fake.encode()).hexdigest()[-1 * matches:]
        fake_hashes[fake_hash] = fake
        fake += ' '

        collision = find_collisions(real_hashes, fake_hashes)

    print("hash found:", collision)
    real_altered = real_hashes[collision]
    fake_altered = fake_hashes[collision]

    with open('confession_real.altered.txt', 'w') as file:
        file.write(real_altered)
    with open('confession_fake.altered.txt', 'w') as file:
        file.write(fake_altered)

def find_collisions(real_hashes: dict, fake_hashes: dict) -> str | None:
    real = set(real_hashes.keys())
    fake = set(fake_hashes.keys())
    collisions = list(real.intersection(fake))
    return None if len(collisions) == 0 else collisions[0]

if __name__ == "__main__":
    main()

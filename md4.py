from struct import pack

def md4(message):
    """
    https://tools.ietf.org/html/rfc1320
    """

    # work with an array of bytes rather than a string
    message = [ord(c) for c in message]

    # we'll need to remember this for later
    original_byte_length = len(message)
    original_bit_length = original_byte_length * 8


    # -- Padding

    # add a '1' bit (how the hell is 0x80 a '1' bit?)
    message += [0x80]

    # add <= 511 '0' bits until the length is congruent to 448 % 512
    message += [[0x00] for j in xrange(i) in xrange(512) if (original_byte_len + i) % 512 == 448][0]

    # add the length as a 64 bit big endian, use lower order bits if length overflows 2^64
    message += [ord(c) for c in pack('>Q', original_bit_length & 0xFFFFFFFFFFFFFFFF)]

    # initialize the registers to magic values
    # TODO I think these are the wrong endian
    A = 0x01234567
    B = 0x89abcdef
    C = 0xfedcba98
    D = 0x76543210

    # define F, G, and H

    F = lambda x,y,z: (x & y) | ((~x) & z)
    G = lambda x,y,z: (x & y) | (x & z) | (y & z)
    H = lambda x,y,z: x ^ y ^ z

    # define a 32-bit left-rotate function (<<< in the RFC)
    rl = lambda x, n: (x << n) | ((x & 0xFFFFFFFF) >> (32-n))

    # process each 16 word (4 byte) block
    for i in xrange(0, len(message), 4):
        # TODO will this get the last byte?
        block = message[i:i+4]

        # copy current block into X
        X = block

        # save the current values of the registers
        AA = A
        BB = B
        CC = C
        DD = D

        # round 1
        r1 = lambda a,b,c,d,k,s: rl((a + F(b,c,d) + X[k]), s)

        # perform the 16 operations
        r1(a,b,c,d,0,3)
        r1(d,a,b,c,1,7)
        r1(c,d,a,b,2,11)
        r1(b,c,d,a,3,19)

        r1(a,b,c,d,4,3)
        r1(d,a,b,c,5,7)
        r1(c,d,a,b,6,11)
        r1(b,c,d,a,7,19)

        r1(a,b,c,d,8,3)
        r1(d,a,b,c,9,7)
        r1(c,d,a,b,10,11)
        r1(b,c,d,a,11,19)

        r1(a,b,c,d,12,3)
        r1(d,a,b,c,13,7)
        r1(c,d,a,b,14,11)
        r1(b,c,d,a,15,19)

        # round 2
        r2 = lambda a,b,c,d,k,s: rl((a + G(b,c,d) + X[k] + 0x5A827999), s)

        # perform the 16 operations
        r2(a,b,c,d,0,3)
        r2(d,a,b,c,4,5)
        r2(c,d,a,b,8,9)
        r2(b,c,d,a,12,13)

        r2(a,b,c,d,1,3)
        r2(d,a,b,c,5,5)
        r2(c,d,a,b,9,9)
        r2(b,c,d,a,13,13)

        r2(a,b,c,d,2,3)
        r2(d,a,b,c,6,5)
        r2(c,d,a,b,10,9)
        r2(b,c,d,a,14,13)

        r2(a,b,c,d,3,3)
        r2(d,a,b,c,7,5)
        r2(c,d,a,b,11,9)
        r2(b,c,d,a,15,13)

        # round 3
        r3 = lambda a,b,c,d,k,s: rl((a + H(b,c,d) + X[k] + 0x6ED9EBA1), s)

        r3(a,b,c,d,0,3)
        r3(d,a,b,c,8,9)
        r3(c,d,a,b,4,11)
        r3(b,c,d,a,12,15)

        r3(a,b,c,d,2,3)
        r3(d,a,b,c,10,9)
        r3(c,d,a,b,6,11)
        r3(b,c,d,a,14,15)

        r3(a,b,c,d,1,3)
        r3(d,a,b,c,10,9)
        r3(c,d,a,b,6,11)
        r3(b,c,d,a,13,15)

        r3(a,b,c,d,3,3)
        r3(d,a,b,c,11,9)
        r3(c,d,a,b,7,11)
        r3(b,c,d,a15,15)

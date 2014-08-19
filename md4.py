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
    # TODO these could be the wrong endian
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

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
        FF = lambda a,b,c,d,k,s: rl((a + F(b,c,d) + X[k]), s)

        # perform the 16 operations
        A = FF(A,B,C,D,0,3)
        D = FF(D,A,B,C,1,7)
        C = FF(C,D,A,B,2,11)
        B = FF(B,C,D,A,3,19)

        A = FF(A,B,C,D,4,3)
        D = FF(D,A,B,C,5,7)
        C = FF(C,D,A,B,6,11)
        B = FF(B,C,D,A,7,19)

        A = FF(A,B,C,D,8,3)
        D = FF(D,A,B,C,9,7)
        C = FF(C,D,A,B,10,11)
        B = FF(B,C,D,A,11,19)

        A = FF(A,B,C,D,12,3)
        D = FF(D,A,B,C,13,7)
        C = FF(C,D,A,B,14,11)
        B = FF(B,C,D,A,15,19)

        # round 2
        GG = lambda a,b,c,d,k,s: rl((a + G(b,c,d) + X[k] + 0x5A827999), s)

        # perform the 16 operations
        A = GG(A,B,C,D,0,3)
        D = GG(D,A,B,C,4,5)
        C = GG(C,D,A,B,8,9)
        B = GG(B,C,D,A,12,13)

        A = GG(A,B,C,D,1,3)
        D = GG(D,A,B,C,5,5)
        C = GG(C,D,A,B,9,9)
        B = GG(B,C,D,A,13,13)

        A = GG(A,B,C,D,2,3)
        D = GG(D,A,B,C,6,5)
        C = GG(C,D,A,B,10,9)
        B = GG(B,C,D,A,14,13)

        A = GG(A,B,C,D,3,3)
        D = GG(D,A,B,C,7,5)
        C = GG(C,D,A,B,11,9)
        B = GG(B,C,D,A,15,13)

        # round 3
        HH = lambda a,b,c,d,k,s: rl((a + H(b,c,d) + X[k] + 0x6ED9EBA1), s)

        A = HH(A,B,C,D,0,3)
        D = HH(D,A,B,C,8,9)
        C = HH(C,D,A,B,4,11)
        B = HH(B,C,D,A,12,15)

        A = HH(A,B,C,D,2,3)
        D = HH(D,A,B,C,10,9)
        C = HH(C,D,A,B,6,11)
        B = HH(B,C,D,A,14,15)

        A = HH(A,B,C,D,1,3)
        D = HH(D,A,B,C,10,9)
        C = HH(C,D,A,B,6,11)
        B = HH(B,C,D,A,13,15)

        A = HH(A,B,C,D,3,3)
        D = HH(D,A,B,C,11,9)
        C = HH(C,D,A,B,7,11)
        B = HH(B,C,D,A,15,15)

       # increment by previous values
       A += AA 
       B += BB
       C += CC
       D += DD

    digest = (A << 32) | B
    digest = (digest << 32) | C
    digest = (digest << 32) | D

    return digest

# SHA-1 Algorithm 
# -----------------------------------------------------------------------------------------------------
def sha1(message):
    '''
    Hashes message using SHA1.

    Parameters:
        message (str): message to be hashed.

    Returns:
        str: SHA1 digest of message.
    '''


    entry_constants = [
        0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 
        0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 
        0x5a827999, 0x5a827999, 0x5a827999, 0x5a827999, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 
        0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 
        0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 0x6ed9eba1, 
        0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 
        0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 
        0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0x8f1bbcdc, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 
        0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 
        0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6, 0xca62c1d6 
    ]

    hash_constants = [
        0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0
    ]

    rotl = lambda num, bits : (num << bits) | (num >> (32 - bits)) % 2**32

    # 1. Pre-Process 'message'
    data_len = 8 * len(message)

    if (data_len % 512) < 448:
        data = ''.join([format(ord(x), '08b') for x in message]) + '1' + ''.join([format(data_len, f'0{511-((data_len)%512)}b')])
    else:
        data = ''.join([format(ord(x), '08b') for x in message]) + '1' + ''.join([format(data_len, f'0{1023-((data_len)%512)}b')])

    # 2. Chunk Loop
    blocks = []

    for x in range(0, len(data) // 512):
        blocks.append([data[x*512:(x*512)+512]])
        blocks[x] = [int(blocks[x][0][y:y+32], 2) for y in range(0, len(blocks[x][0]), 32)]
        blocks[x].extend([0]*64) 

    # 3. Compression Loop
    for block in range(0, len(blocks)):
        for entry in range(16, 80):
            blocks[block][entry] = (rotl(blocks[block][entry - 3] ^ blocks[block][entry - 8] ^ blocks[block][entry - 14] ^ blocks[block][entry - 16], 1)) % 2**32

    # 4. Mutation Loop
    for block in range(0, len(blocks)):
        a, b, c, d, e = hash_constants

        for entry in range(0, 80):
            if entry in range(0, 20): f = (b & c) ^ (~b & d)
            if entry in range(20, 40): f = b ^ c ^ d
            if entry in range(40, 60): f = (b & c) ^ (b & d) ^ (c & d)
            if entry in range(60, 80): f = b ^ c ^ d

            t = (rotl(a, 5) + f + e + entry_constants[entry] + blocks[block][entry]) % 2**32
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = t
        
        hash_constants[0] = (hash_constants[0] + a) % 2**32
        hash_constants[1] = (hash_constants[1] + b) % 2**32
        hash_constants[2] = (hash_constants[2] + c) % 2**32
        hash_constants[3] = (hash_constants[3] + d) % 2**32
        hash_constants[4] = (hash_constants[4] + e) % 2**32

    # 5. Digest Concatenation
    return ''.join([format(hash, '08x') for hash in hash_constants])



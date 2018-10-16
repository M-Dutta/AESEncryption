
Sbox =\
    "63, 7c, 77, 7b, f2, 6b, 6f, c5, 30, 01, 67, 2b, fe, d7, ab, 76, " \
    "ca, 82, c9, 7d, fa, 59, 47, f0, ad, d4, a2, af, 9c, a4, 72, c0, " \
    "b7, fd, 93, 26, 36, 3f, f7, cc, 34, a5, e5, f1, 71, d8, 31, 15, " \
    "04, c7, 23, c3, 18, 96, 05, 9a, 07, 12, 80, e2, eb, 27, b2, 75, " \
    "09, 83, 2c, 1a, 1b, 6e, 5a, a0, 52, 3b, d6, b3, 29, e3, 2f, 84, " \
    "53, d1, 00, ed, 20, fc, b1, 5b, 6a, cb, be, 39, 4a, 4c, 58, cf, " \
    "d0, ef, aa, fb, 43, 4d, 33, 85, 45, f9, 02, 7f, 50, 3c, 9f, a8, " \
    "51, a3, 40, 8f, 92, 9d, 38, f5, bc, b6, da, 21, 10, ff, f3, d2, " \
    "cd, 0c, 13, ec, 5f, 97, 44, 17, c4, a7, 7e, 3d, 64, 5d, 19, 73, " \
    "60, 81, 4f, dc, 22, 2a, 90, 88, 46, ee, b8, 14, de, 5e, 0b, db, " \
    "e0, 32, 3a, 0a, 49, 06, 24, 5c, c2, d3, ac, 62, 91, 95, e4, 79, " \
    "e7, c8, 37, 6d, 8d, d5, 4e, a9, 6c, 56, f4, ea, 65, 7a, ae, 08, " \
    "ba, 78, 25, 2e, 1c, a6, b4, c6, e8, dd, 74, 1f, 4b, bd, 8b, 8a, " \
    "70, 3e, b5, 66, 48, 03, f6, 0e, 61, 35, 57, b9, 86, c1, 1d, 9e, " \
    "e1, f8, 98, 11, 69, d9, 8e, 94, 9b, 1e, 87, e9, ce, 55, 28, df, " \
    "8c, a1, 89, 0d, bf, e6, 42, 68, 41, 99, 2d, 0f, b0, 54, bb, 16";
Sbox = Sbox.split(", ");

def Sbox_Format():
    k = 0;
    s_box = [[0 for x in range(16)] for y in range(16)];
    for i in range(16):
        for j in range(16):
            s_box[i][j] = Sbox[k];
            k+=1;
    return  s_box;

Sbox = Sbox_Format();

#########################
def convertToHex(val):
    hexs = list();
    for x in val:
        hexs.append(hex(ord(x))[2::])
    return hexs;

def plain_breaker(val):
    hexp = convertToHex(val);
    lst = list();
    j = 0;
    for i in range(4):
        lst.append(hexp[j:j + 4]);
        j += 4;
    return lst;

def w(key1):
    val = key1;
    hexk = convertToHex(val);
    lst = list();
    j=0;
    for i in range(4):
        lst.append(hexk[j:j+4]);
        j+=4;
    return lst;

def shift(val1):
    val= val1.copy();
    l = val[0];
    for i in range(len(val)-1):
        val[i] = val[i+1];
    val[len(val)-1] = l;
    return val;

def runSbox(val1):
    val = val1.copy();
    val.reverse();
    new_w =list();
    while len(val) != 0:
        ch = list(val.pop());
        row = int(ch[0], 16);
        col = int(ch[1], 16);
        hexCh = Sbox[row][col];
        new_w.append(hexCh);
    return new_w;

def addRoundConst(val1):
    val = val1.copy();
    val[0] = (hex(int("01", 16) ^ int(val[0], 16))[2::]);
    return val;

def gw(val1):
    val = val1.copy();
    s1= shift(val);
    s2=runSbox(s1);
    s3=addRoundConst(s2);
    return s3;

def XOR(x,y):
    z = list();
    for i in range(len(x)):
        z.append(hex(int(x[i], 16) ^ int(y[i], 16))[2::].zfill(2));
    return z;

def generateW(wval):
    g = gw(wval[3]);
    wval.append(XOR(wval[0],g));
    for i in range (3):
        wval.append(XOR(wval[i+4],wval[i+1]))
    return wval;

def generateRoundkey(val):
    w1 = generateW(w(val));
    return w1;

def generateMatrix(plainText,the_key):
    hex_plain = plain_breaker(plainText);
    roundKey = generateRoundkey(the_key);
    plain_Matrix = [[0 for x in range(4)] for y in range(4)];
    roundKey_Matrix = [[0 for x in range(4)] for y in range(4)];
    j = 0;
    for i in range(4):
        for j in range(4):
            plain_Matrix[i][j] = hex_plain[j][i];
            roundKey_Matrix[i][j] = roundKey[j][i];
    return plain_Matrix,roundKey_Matrix;


def matrixXOR(plainM,roundkeyM):
    l = list();
    for i in range(len(plainM)):
        l.append(XOR(plainM[i],roundkeyM[i]));
    return l;

def substitute(matrix):
    l = list();
    for i in range(len(matrix)):
        l.append(runSbox(matrix[i]));
    for i in range(4):
        for j in range(4):
            matrix[i][j] = l[j][i];
    return l;

def shifter(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

def shiftMatrix(matrix):
    i =0;
    for i in range(len(matrix)):
        matrix[i]=shifter(matrix[i],i);
        i+=1;
    return matrix;

def mult_matrix(X):
    mixMatrix =[['02', '03', '01', '01'],
                ['01', '02', '03', '01'],
                ['01', '01', '02', '03'],
                ['03', '01', '01', '02']]

    result = [['00' for x in range(len(X))] for y in range(len(mixMatrix[0]))];
    r = '';
    for i in range(len(mixMatrix)):
        # iterate through columns of Y
        for j in range(len(X[0])):
            # iterate through rows of Y
            for k in range(len(X)):
                if k == 1:
                    r =  hex( (int(mixMatrix[i][k-1], 16) * int(X[k][j], 16)) ^ int(X[k][j],16) )[2::].zfill(8);
                    print("k is 1",mixMatrix[i][k-1], '*', X[k][j],'^', X[k][j], bin(int(r, 16))[2::].zfill(8));
                else:
                    r = hex(int(mixMatrix[i][k], 16) * int(X[k][j], 16))[2::].zfill(8);
                    print(mixMatrix[i][k], '*', X[k][j], bin(int(r, 16))[2::].zfill(8));

                binr = bin(int(r,16))[2::];
                if len(binr)>8:
                    print("val here:",r, binr);
                    r = binFixser(binr);
                result[i][j] = hex(int(result[i][j],16) ^ int(r,16));

    print('out');
    return result;

def binFixser(binVal):
    b = binVal;
    gf = '100011011';
    print("big b ",b);
    xor = bin(int(b, 2) ^ int(gf, 2))[2::];
    while len(xor)>8:
        xor = bin(int(xor,2) ^int(gf,2))[2::];
        #print(xor);
    print("bin: ",xor);
    print('hex:', hex(int(xor,2)));
    return xor;


def matrix_print(a):
    for i in range(len(a)):
        print(*a[i]);
    return
####
##test Here:
key ="Thats my Kung Fu";
str ="Two One Nine Two";

data = generateMatrix(str, key);
plainText_matrix = data[0];
key_matrix = data[1];
print("PlainText Matrix in HEX:")
matrix_print(plainText_matrix);
print("RoundKey 0 in Hex:")
matrix_print(key_matrix);




###


















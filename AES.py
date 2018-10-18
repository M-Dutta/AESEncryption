
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
        print(ch)
        row = int(ch[0], 16);
        col = int(ch[1], 16);
        print(ch[0],row)
        print(ch[1],col)
        hexCh = Sbox[row][col];
        new_w.append(hexCh);
    return new_w;

#left off here
def runSboxMatrix(val1):
    new_w = [[0x00 for x in range(len(val1))] for y in range(len(val1[0]))];
    val = val1.copy();

    for i in range(len(new_w)):
        for j in range(len(new_w[0])):
            ch = list(val[i][j]);
            row = int(ch[0], 16);
            col = int(ch[1], 16);
            hexCh = Sbox[row][col];
            new_w[i][j]= hexCh

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

def XORmatrix(a,b):
    result = [[0x00 for a in range(len(a))] for y in range(len(a[0]))];
    stringToByteConverter(a);
    stringToByteConverter(b);
    for i in range(len(a)):
        for j in range(len(a[0])):
            result[i][j] = a[i][j]^b[i][j]
    bytetoStringConverter(result)
    return result

def mixCol(X):
    mixMatrix =[[0x02, 0x03, 0x01,0x01],
                [0x01, 0x02, 0x03, 0x01],
                [0x01, 0x01, 0x02, 0x03],
                [0x03, 0x01, 0x01, 0x02]]
    print("mixMatrix", type(X[0][0]))
    X = stringToByteConverter(X);
    result = [[0x00 for x in range(len(X))] for y in range(len(mixMatrix[0]))];
    for i in range(len(X)):
        for j in range(len(X[0])):
            for k in range(len(X)):
                result[i][j] ^= result[i][j] ^ hexMult(mixMatrix[i][k], X[k][j]);

    result =bytetoStringConverter(result);
    return result;


def matrix_print(a):
    for i in range(len(a)):
        print(a[i][0],a[i][1],a[i][2],a[i][3]);
    return

def stringToByteConverter(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = int(matrix[i][j],16);
    return matrix;

def bytetoStringConverter(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = (hex(matrix[i][j]).replace('0x','')).rjust(2,"0");

    return matrix;


def hexMult(a,b):
    mult = a* b
    binval = bin(mult);
    gf = '100011011';
    xor = int(binval, 2) ^ int(gf, 2);

    return int(hex(xor), 16);
####
##test Here:
key ="Thats my Kung Fu";
str ="Two One Nine Two";


data = generateMatrix(str, key);
state_matrix = (data[0]);
key_matrix = (data[1]);
print("PlainText Matrix in HEX:")
#atrix_print(plainText_matrix);
print("RoundKey 0 in Hex:")
matrix_print(state_matrix);
print()
matrix_print(key_matrix);
xorM = XORmatrix(state_matrix,key_matrix)
print()
matrix_print(xorM)
print(len(xorM),len(xorM[1]))
sboxedMatrix = runSboxMatrix(xorM);
print("Sboxed Matrix")
matrix_print(sboxedMatrix)
mixed_Matrix = mixCol(sboxedMatrix);
matrix_print(mixed_Matrix)


## Only Mix Matrix Remaining:
##
##


###


















from PIL import Image


def open_image(image_name):
    # print('here', image_name)
    x = True
    while x == True:
        try:
            fp = Image.open(image_name)
            x = False
        except:
            # print('here', image_name)
            print('File not found.', image_name, x)
            fp = None
            break
            # image_name = input("The name of the image file: ")
    return fp, image_name


def encode_string(string):
    bi_string = ''
    for ch in string:
        num = to_binary(ord(ch))
        bi_string += str(num).zfill(8)
    bi_string += '010000110111010001110010011011000010110101000100'

    return bi_string


def decode_string(bi_string):
    string = ''
    count = 0
    while count <= (len(bi_string)):
        string += chr(to_decimal(bi_string[count:count+8]))
        count += 8

    string = string[:-7]
    return string


def encode_image(image, bi_string):
    # TODO: might need to change this
    im, image = open_image(image)
    w, h = im.size
    pix = im.load()
    count = 0
    for i in range(w):
        if count >= len(bi_string):
                break
        for j in range(h):
            rgb = pix[i,j]
            r = to_binary(rgb[0])
            g = to_binary(rgb[1])
            b = to_binary(rgb[2])

            if count < len(bi_string):
                if bi_string[count] == '1':
                    r = r[:-1] + '1'
                else:
                    r = r[:-1] + '0'

            count += 1

            if count < len(bi_string):
                if bi_string[count] == '1':
                    g = g[:-1] + '1'
                else:
                    g = g[:-1] + '0'

            count += 1

            if count < len(bi_string):
                if bi_string[count] == '1':
                    b = b[:-1] + '1'
                else:
                    b = b[:-1] + '0'
            count += 1

            pix[i,j] = (int(to_decimal(r)), int(to_decimal(g)), int(to_decimal(b)))

            if count >= len(bi_string):
                break
    # TODO: change this
    # new_image = str(image[:-4] + "encoded.png")
    im.save(image)
    im.close()
    return im


def decode_image(image):
    # TODO: will probably need to edit this function
    im, image = open_image(image)
    w, h = im.size
    pix = im.load()
    bi_string = ''
    for i in range(w):
        for j in range(h):
            rgb = pix[i, j]

            r = to_binary(rgb[0])
            g = to_binary(rgb[1])
            b = to_binary(rgb[2])

            bi_string += r[-1:]
            bi_string += g[-1:]
            bi_string += b[-1:]

            if '010000110111010001110010011011000010110101000100' in bi_string:
                return bi_string

    return 'No message was found'


def to_decimal(num):
    num = list(str(num))

    num.reverse()
    lst = []

    for i in range(len(num)):
        part = int(num[i]) * (2 ** i)
        lst.append(part)

    dec = sum(lst)
    return dec


def to_binary(dec):
    lst = []
    dec = int(dec)
    while dec >= 1:
        rmdr = dec % 2
        dec = int(dec / 2)
        lst.append(str(rmdr))

    lst.reverse()
    binary = ''.join(lst)
    return binary.zfill(8)
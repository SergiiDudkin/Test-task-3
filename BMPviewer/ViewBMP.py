#!/usr/bin/env python
import sys


class BMPImage(object):
    """BMP image parser"""
    def __init__(self, filepath):
        with open(filepath, 'rb') as ifile: self.bytestr = ifile.read()

        compressions = {0: 'BI_RGB',
                        1: 'BI_RLE8',
                        2: 'BI_RLE4',
                        3: 'BI_BITFIELDS',
                        4: 'BI_JPEG',
                        5: 'BI_PNG',
                        6: 'BI_ALPHABITFIELDS',
                       11: 'BI_CMYK',
                       12: 'BI_CMYKRLE8',
                       13: 'BI_CMYKRLE4 '
        }

        self.filetype = self.bytestr[:2]
        self.filesize = self.intfrombytes(2, 6)
        self.offset = self.intfrombytes(10, 14)
        self.header_size = self.intfrombytes(14, 18)
        self.img_w = self.intfrombytes(18, 22)
        self.img_h = self.intfrombytes(22, 26)
        self.num_of_planes = self.intfrombytes(26, 28)
        self.bits_per_pix = self.intfrombytes(28, 30)
        self.compression = compressions[self.intfrombytes(30, 34)]
        self.img_size = self.intfrombytes(34, 38)
        self.h_res = self.intfrombytes(38, 42)
        self.v_res = self.intfrombytes(42, 46)
        self.num_of_clrs = self.intfrombytes(46, 50)
        self.num_of_imp_clrs = self.intfrombytes(50, 54)

    def __str__(self):
        """Returns parsed image data"""
        output = '''
            Bitmap file header
        Type:                        {}
        Size:                        {}
        Offset:                      {}

            DIB header
        Size of this header:         {}
        Image width:                 {}
        Image height:                {}
        Number of color planes:      {}
        Number of bits per pixel:    {}
        Compression method:          {}
        Image size:                  {}
        Horizontal resolution:       {}
        Vertical resolution:         {}
        Number of colors in palette: {}
        Number of important colors:  {}
        '''.format(self.filetype.decode('ascii'), self.filesize, self.offset,
                   self.header_size, self.img_w, self.img_h,
                   self.num_of_planes, self.bits_per_pix, self.compression,
                   self.img_size, self.h_res, self.v_res,
                   self.num_of_clrs, self.num_of_imp_clrs)
        return output

    def intfrombytes(self, st, en):
        """Converts sequence of bytes from self.bytestr into positive integer"""
        return int.from_bytes(self.bytestr[st:en], byteorder='little')

    def show(self):
        """Display image in console by means of pseudo graphics"""
        row_size = ((self.bits_per_pix * self.img_w + 31) // 32) * 4
        img_end = self.offset + self.img_size
        bytes_per_pix = int(self.bits_per_pix / 8)
        alpha = ' ░▒▓█'
        strlist = []

        if self.compression == 'BI_RGB':
            for row_start in range(img_end - row_size, self.offset - row_size, -row_size):
                for i in range(row_start, row_start + bytes_per_pix * self.img_w, bytes_per_pix):
                    strlist.append('\033[38;2;{};{};{}m██'.format(self.bytestr[i+2], self.bytestr[i+1], self.bytestr[i]))
                strlist.append('\n')
        elif self.compression == 'BI_BITFIELDS' and self.bits_per_pix == 32:
            ri = list(self.bytestr[54:58]).index(255) # Red
            gi = list(self.bytestr[58:62]).index(255) # Green
            bi = list(self.bytestr[62:66]).index(255) # Blue
            ai = list(self.bytestr[66:70]).index(255) # Alpha
            for row_start in range(img_end - row_size, self.offset - row_size, -row_size):
                for i in range(row_start, row_start + bytes_per_pix * self.img_w, bytes_per_pix):
                    strlist.append('\033[38;2;{};{};{}m{}'.format(self.bytestr[i+ri], # Red
                                                                  self.bytestr[i+gi], # Green
                                                                  self.bytestr[i+bi], # Blue
                                                                  alpha[(self.bytestr[i+ai]+32)//64] * 2 # Alpha
                    ))
                strlist.append('\n')
        else:
            print('Sorry, I do not know how to parse {}bit {}.'.format(self.bits_per_pix, self.compression))
            return

        strlist.append('\033[0m')
        print(''.join(strlist))


if __name__ == '__main__':
    args = sys.argv
    path = args[1] if len(args) == 2 else input('Enter path to your image: ')

    img = BMPImage(path)
    print(img)
    img.show()

#!/usr/bin/env python
import sys, os.path


def read_from_image(filename):
    from PIL import Image
    import pytesseract
    image = Image.open(filename)
    return pytesseract.image_to_string(image, lang='eng', config='--psm 5 --oem 3 -c tessedit_char_whitelist=0123456789 textord_tabfind_vertical_horizontal_mix=1')
    raise NotImplementedError


def read_from_text(filename):
    with open(filename) as f:
        lines = f.readlines()
        collines = lines[1:lines.index("\n")]
        rowlines = lines[lines.index("\n") + 2:]
        colspecs = [map(int, line.strip().rstrip().split(' ')) for line in collines]
        rowspecs = [map(int, line.strip().rstrip().split(' ')) for line in rowlines]
        assert len(colspecs) == len(rowspecs)
        size = len(colspecs)
        return colspecs, rowspecs, size
    raise Exception("Some sort of error reading specs from %s" % filename)


def read_specs(filename):
    _, extension = os.path.splitext(filename)
    if extension == ".png":
        return read_from_image(filename)
    elif extension == ".txt":
        return read_from_text(filename)
    else:
        raise ValueError("Unknown extension.")


def main(args):
    if len(args) != 2:
        print "Usage: %s [filename]" % args[0]
        return 1
    if not os.path.isfile(args[1]):
        print "Could not find file '%s'." % args[1]
        return 1

    try:
        print read_specs(args[1])
    except ValueError:
        print "'%s' has an unknown extension. Use a file with .txt or .png extension." % args[1]
        return 1

    return 0



if __name__ == "__main__":
    sys.exit(main(sys.argv))

import json


def get_tags(f, nextIFD, tagsize, endian):
    f.seek(nextIFD)
    nrtags = int.from_bytes(f.read(tagsize[0]), endian)
    tags = []
    for i in range(nrtags):
        ID = int.from_bytes(f.read(tagsize[1]), endian)
        dtype = int.from_bytes(f.read(tagsize[2]), endian)
        nrv = int.from_bytes(f.read(tagsize[3]), endian)
        tagd = int.from_bytes(f.read(tagsize[4]), endian)
        tag = [ID, dtype, nrv, tagd]
        tags.append(tag)
    nextIFD = int.from_bytes(f.read(tagsize[5]), endian)
    return tags, nextIFD


def ifd2json(in_pth: str, out_pth: str = None):
    with open(in_pth, 'rb') as f:
        byteorder = f.read(2)
        endian = 'big'  # big endian
        if byteorder == b'II':
            endian = 'little'  # little endian
        bigtiff = int.from_bytes(f.read(2), endian) == 43
        nextIFD = int.from_bytes(f.read(4), endian)
        if bigtiff:
            nextIFD = int.from_bytes(f.read(8), endian)
        tagsize = (2, 2, 2, 4, 4, 4)  # (nr_tags, ID, type, nr of values, tag data, nextIFD)
        if bigtiff:
            tagsize = (8, 2, 2, 8, 8, 8)  # (nr_tags, ID, type, nr of values, tag data, nextIFD)
        tagslist = []
        tags, nextIFD = get_tags(f, nextIFD, tagsize, endian)
        tagslist.append(tags)
        while nextIFD > 0:
            tags, nextIFD = get_tags(f, nextIFD, tagsize, endian)
            tagslist.append(tags)
    with open(out_pth, "w") as outfile:
        json.dump(tagslist, outfile)

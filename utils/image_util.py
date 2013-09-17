import urllib
import ImageFile

def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None

print getsizes("http://i0.uyl.me/files/02192514363784633354.jpg")
#print getsizes("http://106.imagebam.com/download/lbU0CYYQzMbBIeIUszzAvA/27573/275723253/3.jpg")

import urllib2
import httplib
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

def exists(site, path):
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

try:
    #urllib2.urlopen("http://xpics.us/images/472923085915_2013825109023.jpg", timeout=5)
    urllib2.urlopen("http://www.tu265.com/di-c3676a09d876b3c94749a248699f610f.jpg", timeout=5)
    print 'true!'
except urllib2.URLError:
    print 'false'


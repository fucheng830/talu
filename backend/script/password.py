import hashlib 

def md5(raw_password):
    return hashlib.md5(raw_password.encode('utf-8')).hexdigest()

if __name__=='__main__':
    import sys
    print(md5(sys.argv[1]))
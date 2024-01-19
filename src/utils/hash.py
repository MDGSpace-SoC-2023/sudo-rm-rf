import hashlib

def hashing(object):
    hash_value=hashlib.sha256(bytes(str(object),'utf-8')).hexdigest()
    


    return hash_value


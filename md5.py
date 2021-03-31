from hashlib import md5

while True:
    a = md5()
    a.update(input('输入原始值:').encode())
    print(a.hexdigest().upper())

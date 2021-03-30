from hashlib import md5
a = md5()
while True:
    a.update(input('输入原始值:').encode())
    print(a.hexdigest().upper())

'''Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных'''



str1 = ["разработка","сокет","декоратор"]
for i in range(0,len(str1)-1):
    a = str1[i].encode(encoding='utf-8', errors='ignore')
    print(f"{str1[i]}\nв unicod:{str1[i].encode(encoding='utf-8', errors='ignore')}\nтип: {type(str1[i])}\nтип: {str1[i].encode(encoding='utf-8', errors='ignore')}\n")
   
'''Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных'''  



class Struct:
        def __init__(self,slice):
            self.slice = slice
            self.atribute = []

        def magic(self):
            for i,v in enumerate(self.slice):
                if i ==0:
                    self.a = f"b'{v}'"# ВОПРОС как возможно присвоить атрибуту класса значение b'str',
                    # возвращает строку, и префикс b  тоже как строка.
                if i ==1:
                    self.b = f"b'{v}'"
                else:
                    self.c = f"b'{v}'"
            print(type(b'self.a'),type(b'self.b'),type(b'self.c'))
            print(len(b'self.a'),len(b'self.b'),len(b'self.c'))
            self.atribute = [self.a,self.b,self.c]
            print(self.atribute)
           
interface = Struct(["class", "function", "method"])
interface.magic()
  
"""Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе."""



slice2 = ['attribute', 'класс', 'функция','type']


for el in slice2:

    try:
        print(bytes(el, 'ascii'))
    except UnicodeEncodeError:
        print(f'{el} невозможно записать в  байтовом типе')


"""Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode)."""

slice_str = ['разработка', 'администрирование', 'protocol', 'standard']
slice_to_utf8 = []
slice_to_str =[]

for el in slice_str:
    try:
        elm = el.encode("UTF-8",'ignore')
        slice_to_utf8.append(elm)
    except UnicodeEncodeError:
        print(f'{el} невозможно записать в  байтовом типе')

print(slice_to_utf8)

for el in slice_to_utf8:
    try:
        elm = el.decode('UTF-8','ignore')
        slice_to_str.append(elm)
    except UnicodeEncodeError:
        print(f'{el} неправильная кодировка')

print(slice_to_str)

"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""
import subprocess
# import chardet- # !!!не смог поставить библиотеку !!!  from .compat import JSONDecodeError as CompatJSONDecodeError
#ImportError:
 #cannot import name 'JSONDecodeError' from 'pip._vendor.requests.compat' 
# (/home/yamamotod/Рабочий стол/Asyncchat/venvAC/lib/python3.8/site-packages/pip/_vendor/requests/compat.py)

hosts = ['ping', 'yandex.ru']
ping = subprocess.Popen(hosts, stdout=subprocess.PIPE)
for line in ping.stdout:
    result = chardet.detect(line)
    print(result)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))


"""Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое"""

with open('less1.txt', 'w', encoding='utf-8') as lw1:
    lw1.write('сетевое программирование\n')
    lw1.write('сокет\n')
    lw1.write('декоратор\n')

with open('less1.txt','r', encoding='utf-8') as lr1:
    for line in lr1:
        print(line, end="")

"""
кодировка файла проблема с импортом chardet!!!
"""
from chardet.universaldetector import UniversalDetector

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')
file.close()# Вопрос- обязательно при конструкции with open закрывать файловый дескриптор?

# узнаем кодировку файла

"""
Если файл имеет большой размер, то вместо считывания его целиком в строку
и использования функции detect() можно воспользоваться классом UniversalDetector.
В этом случае можно читать файл построчно и передавать текущую строку методу feed().
Если определение кодировки прошло успешно, атрибут done будет иметь значение True.
Это условие можно использовать для выхода из цикла.
После окончания проверки следует вызвать метод close().
Получить результат определения кодировки позволяет атрибут result
"""

DETECTOR = UniversalDetector()
with open('test.txt', 'rb') as test_file:
    for i in test_file:
        DETECTOR.feed(i)
        if DETECTOR.done:
            break
    DETECTOR.close()
print(DETECTOR.result['encoding'])

# открываем файл в правильной кодировке
with open('test.txt', 'r', encoding=DETECTOR.result['encoding']) as file:
    CONTENT = file.read()
print(CONTENT)

"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)
например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

from chardet import detect

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')
file.close()


def encoding_convert():
    """Конвертация"""
    with open('test.txt', 'rb') as f_obj:
        content_bytes = f_obj.read()
    detected = detect(content_bytes)
    encoding = detected['encoding']
    content_text = content_bytes.decode(encoding)
    with open('test.txt', 'w', encoding='utf-8') as f_obj:
        f_obj.write(content_text)


encoding_convert()

# открываем файл в правильной кодировке
with open('test.txt', 'r', encoding='utf-8') as file:
    CONTENT = file.read()
print(CONTENT)



"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но отерыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""

import sys
from _locale import _getdefaultlocale

# изменение кодировки локали

_getdefaultlocale = (lambda *args: ['en_US', 'utf-8'])

LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
with open('test.txt', 'w') as file:
    for line in LINES_LST:
        file.write(f'{line}\n')
file.close()

# открываем файл в правильной кодировке
with open('test.txt', 'r') as file:
    CONTENT = file.read()
print(CONTENT)
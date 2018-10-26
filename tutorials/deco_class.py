import sys
import time
import heapq
from matplotlib import pyplot as plt


def timed(f, args, *, n_iter=100):
    acc = float("inf")
    for i in range(n_iter):
        t0 = time.perf_counter()
        f(*args)
        acc = min(acc, time.perf_counter() - t0)

    return acc


def compare(fs, args):
    xs = list(range(len(args)))
    for f in fs:
        plt.plot(xs, [timed(f, chunk) for chunk in args],
                 label=f.__name__)
    plt.legend()
    plt.grid(True)
#-------------------------------------------------------------------------------------------
def packsack(values_and_weights, capacity):
    order = [(v/w, w) for v, w in values_and_weights]
    order.sort(reverse=True)
    acc = 0
    for v, w in order:
        if w < capacity:
            acc += v * w
            capacity -=w
        else:
            acc += v * capacity
            break

    return acc

def main_packsack():
    reader = (tuple(map(int, line.split())) for line in sys.stdin)
    n, capacity  = next(reader)
    values_and_weights = list(reader)
    assert len(values_and_weights) == n
    result = packsack(values_and_weights, capacity)
    print('{:.3f}'.format(result))
#---------------------------------------------------------------------------------------------
from  collections import  Counter, namedtuple
#Node = namedtuple('Node', ['left','right'])  -  простейший способо объявить класс
class Node(namedtuple('Node', ['left','right'])):
    def walk(self, code, acc):
        #print('***',self.left)
        self.left.walk(code,acc + '0')
        self.right.walk(code, acc + '1')

class Leaf(namedtuple('Leaf',['char'])):
    def walk(self, code, acc):
        code[self.char] = acc or '0'
        #print('+++',code)

def haffman_encode(s):
    #print(Counter(s))
    # будет проблема,если abracadabra: "TypeError: '<' not supported between instances of 'Leaf' and 'str'", при таком случае: Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
    # т.е. Node(c:1,d:1) будет сравниваится с Leaf(b:2) на втором шаге while, т.е (2, Leaf('b')) сравнить  c (2,Node(left=Leaf('d'),right=Leaf('c')) => Leaf('char'='b');
    #Node(left=Leaf('d'), right=Leaf('c'), т.е. будет сравниваться 'b' с  Leaf('d'). Поэтому надо добавить элемент уникальности len(h) в кортеж:
    #h = [(freq, Leaf(ch)) for ch, freq in Counter(s).items()] #[(2, Leaf(char='a')), (2, Leaf(char='b')), (2, Leaf(char='c')), (1, Leaf(char='d'))] # это не годится
    h = []
    for ch, freq in Counter(s).items():
        h.append((freq, len(h), Leaf(ch)))
    #print(h)
    heapq.heapify(h) # очередь с приоритетами
    #print(s)
    count = len(h) #для уникальности
    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h) #вытянуть минимальную частоту
        freq2, _count2, right  = heapq.heappop(h)
        heapq.heappush(h,(freq1 + freq2, count, Node(left, right)))
        #print('{}   freq1*** |{}| : left*** |{}| + freq2*** |{}| : right*** |{}| | {}'.format(count,freq1,left, freq2, right,Node(left, right)))
        count +=1
    code = {}
    if  h:
        [(_freq, _count, root)] = h
        print(h)
        root.walk(code,'')
        #print(type(root))
    return code

def main_haffman(s):
    #s= input()
    code = haffman_encode(s)
    encoded = ''.join(code[ch] for ch in s)
    print(len(code), len(encoded))
    for ch in sorted(code):
        print('{}: {}'.format(ch, code[ch]))
    print (encoded)

#main_haffman('abracadabra')

#для тестирования
import string
import random

length = random.randint(0,15)
s = "".join(random.choice(string.ascii_letters) for i in  range(length))
#s='abcadbc'
s = 'abracadabra'
#code  = haffman_encode(s)
#print(s,code)
#encoded = ''.join(code[ch] for ch in s)
#print(encoded)
#---------------------------------------------------------------------------------------------
#Двоичный поиск
#альтернатива from bisect import bisect_left
'''def contains(l, elem):
...     index = bisect_left(l, elem)
...     if index < len(l):
...         return l[index] == elem
...     return False
>>> testlist = (1, 2, 3, 6, 8, 10, 15)
>>> contains(testlist, 10)
'''
def find_pos(xs,query):
    lo, hi = 0, len(xs)
    print('init', lo,hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if query < xs[mid]:
            hi = mid #[lo,mid)
            print(mid,lo,hi,'query < xs[mid]','xs[mid]=',xs[mid])
        elif query > xs[mid]:
            lo = mid + 1  #(mid+1, hi]
            print(mid, lo, hi,'query > xs[mid]','xs[mid]=',xs[mid])
        else:
            print(mid, lo, hi,'query = xs[mid]','xs[mid]=',xs[mid])
            return mid + 1

    return -1
def test_pos():
    q=[1,5,8,12,13,17]
    find_pos(q, 17)
    assert find_pos([],42) == -1
    assert find_pos([42], 42) == 1
    assert find_pos([42], 24) == -1


def main_find_pos():
    reader =(map(int, line.split()) for line in sys.stdin) #sys.stdin  в этом случае в cmd вывод: python als.py < input_pos.txt
    n, *xs = next(reader)
    k, *queries = next(reader)
    for query in queries:
        print(find_pos(query, xs), end=' ')
#test_pos()
#---------------------------------------------------------------------------------------------
#Расстояние редактирования
from  functools import lru_cache

def edit_distance(s1, s2):
    #Рекурсивный метод
    cnt=0
    @lru_cache(maxsize=None)
    def d(i, j):
        nonlocal cnt
        cnt += 1
        print('cnt',cnt,'i=',i,'j=',j)
        if i == 0 or j == 0:
            print('result', 'cnt=',cnt,'i=',i,'j=',j, 'max=',max(i,j),)
            return max(i,j)
        else:
            a= d(i, j - 1) + 1
            b = d(i - 1, j) + 1
            c= d(i - 1, j - 1) + (s1[i - 1] != s2[j - 1])

            print('deeper', 'cnt=',cnt,'i=',i,'j=',j,'min=',min(a,b,c))

            return min(d(i,j-1) + 1,
                        d(i-1,j) + 1,
                        d(i-1, j-1) + (s1[i-1] != s2[j-1])
                    )
    #return d(len(s1), len(s2))

    #Итерационный метод
    m, n  = len(s1), len(s2)
    if m < n:
        edit_distance(s2, s1)

    prev = list(range(n+1))
    for i,ch1 in enumerate(s1,1):
        curr = [i] #0 хотим min(m,n)
        for j, ch2 in enumerate(s2,1):
            curr.append(min(curr[-1] + 1,
                            prev[j] + 1,
                            prev[j-1] + (ch1 != ch2)
                        )
            )
        prev = curr
    return prev[n]


def test(n_iter=100):
    '''for i in range(n_iter):
        length = random.randint(0, 64)
        s = ''.join(random.choice('01') for i in range(length))
        assert edit_distance(s,'') == edit_distance('', s) == len(s)
        assert edit_distance(s,s) == 0
    '''
    #assert edit_distance('ab','ab') == 0
    edit_distance('so','po')
    #short-
    #p-orts
test()
#---------------------------------------------------------------------------------------------
#фабрика
def make_min(*,lo=float('-inf'),hi=float('inf')):
    def min(first,*args):
        res = hi
        #print((first, ) + args)
        #print(*args)
        for arg in (first, ) + args:
            if arg < res and lo < arg < hi :
                res = arg
        return max(res,lo)

    return min
x = [300,-999,100,-500]
fabric = make_min(lo=-1000,hi=1000)
res = fabric(*x)
#print(res)
#---------------------------------------------------------------------------------------------
#getter-setter-function
def cell(value=None):
    def get():
        return value
    def sett(update):
        nonlocal value #чтобы изменить enclosing value, а не создать новую
        value = update
    return get,sett
get,sett= cell()
sett(700)
#print(get())
#---------------------------------------------------------------------------------------------
map, lambda. Здесь интересно, что итерация сразу по [2,3] range[1,8] одновременно. Берется минимальный список
#т.е 2**1 = 2
#3**2 = 9
mapper = map(lambda x,n: x ** n, [2,3],range(1,8))
#print(list(mapper))
#f1 = list(filter(lambda x: x%2 !=0,range(10)))
#print(f1)
#x = [0, None, "",[], {}, set(), 42,700]
#f2 = list(filter(None,x))
#print(f2)
#f3 = list(zip('abc', range(10), [42j,42j,42j],))
#print(type(42j))
#print(f3)
#x = [1,2,3]
#y = [-1,-2,-3,-4]
#f4 = list(map(lambda *args: args, x, y))
#print(f4)
#---------------------------------------------------------------------------------------------
#генератор списка
nested = [[1,2], range(8)]
f5 = [x**2 for xs in nested for x in xs]
#print(f5)
#---------------------------------------------------------------------------------------------
#декораторы
import functools

#думать о декораторе  надо так: identity = trace(identity)
trace_enabled = True
def trace(func):
    @functools.wraps(func) #3 variant
    def inner(*args):
        print('*****',func.__name__, args)
        return func(args)
    #inner.__doc__ = func.__doc__          #1 variant
    #inner.__module__ = func.__module__
    #inner.__name__ = func.__name__
    #functools.update_wrapper(inner,func)   #2 variant
    return inner if trace_enabled else func

@trace
def identity(x):
    '''I do nothing useful'''
    return x
#a = identity(42)
#print(identity.__doc__)
#print(identity.__name__)
#print(identity.__module__)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#но существуют декораторы с аргументом (например, запись ошибок в файл), шаблон использования:
#тогда думать надо так:
#deco = trace(sys.stderr)  #wrapper
#identity = identity(deco)  #inner
def trace_first(handle):
    def deco(func):
        @functools.wraps(func)
        def inner(*args):
            print('+++++'.func.__name__, args, file=handle)
            return func(args)
        return inner
    return deco

#Но такая запись  выглядит плохо, поэтому преобразована:
def trace_second(func=None, *, handle=sys.stdout):
    #со скобками
    if func is None:
        print('outter step')
        return lambda func: trace_second(func,handle=handle)
    #без скобок
    @functools.wraps(func)
    def inner(*args):
        print('inner step')
        print(func.__name__,args)
        return func(*args)
    return inner

@trace_second
def ident(x):
    print('x=',x)
    return x
#ident(100)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#пример полезного декоратора

def timethis(func=None,*,n_iter=100):
    if func is None:
        return lambda func: timethis(func,n_iter=n_iter)

    @functools.wraps(func)
    def inner(*args,**kwargs):
        print(func.__name__, end='...')
        acc = float('inf')
        for i in range(n_iter):
            tick = time.perf_counter()
            result = func(*args,**kwargs)
            acc = min(acc, time.perf_counter()-tick)
        print('acc',acc)
        return result
    return inner
#можно вызать так:
#помни, думать о декораторе  надо так: identity = trace(identity)
#result = timethis(sum)(range(10**6))
#print(result)

# или вызвать так:
@timethis
def summer(rang):
    res = sum(rang)
    return res

#result2 = summer(range(10**6))
#print(result2)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#пример 2
#Сколько раз грузилась функция
def profiled(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        inner.ncalls += 1
        return func(*args,**kwargs)
    inner.ncalls = 0
    return inner

@profiled
def identity(x):
    return x
#identity(42)
#identity(43)
#print(identity.ncalls)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#пример 3
#Загрузить единожды настройки
def once(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        if not inner.loaded:
            inner.loaded = True
            func(*args,**kwargs)
    inner.loaded = False
    return inner
@once
def initialize_settings():
    print('Settings initialized')
#initialize_settings()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#пример 4
# PRE + POST - decorators: time 47:43
# https://www.youtube.com/watch?v=umy_e8cHKgU
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#пример 5
def square(func):
   return lambda x,y: func(x*y, y)

def addsome(func):
    return lambda x,y: func(x,y+5)

@square
@addsome
def iden(x,y):
    return x,y

#res = iden(3,4)
#print(res)
#---------------------------------------------------------------------------------------------
#Функциональное программирование, модуль FUNCTOOLS
f = functools.partial(sorted, key=lambda p: p[1])
a=f([('z',100),('a',1)])
#print(a)
f1= functools.partial(sorted,{'z':300,'q':1000,'a':80000})
b=f1()
#print(b)
#---------------------------------------------------------------------------------------------
#Коллекции
from  collections import namedtuple
Person = namedtuple('Person',['name','age'])
p = Person('George',44)
#print(p.name,p.age,p._fields)
#print(p._asdict())

#---------------------------------------------------------------------------------------------
#Классы
from collections import deque
#1~~~~~
class MemorizingDict(dict):
    history = deque(maxlen=10)
    def set(self,key,val):
        self.history.append(key)
        self[key] = val
    def get_hist(self):
        return self.history

d = MemorizingDict({'first': 100})
d.set('second', 200)
#print(d.get_hist())
a = MemorizingDict()
#print(a.get_hist())
a.set('third',300)
#print(a.get_hist())
#print(d.get_hist())
#print(vars(MemorizingDict))

class SomeClass:
    def do_something(self):
        print('Doing something...')
SomeClass().do_something #связанный с экземпляром
#SomeClass().do_something()
SomeClass.do_something #не связанный c эземпляром
instance = SomeClass()
#SomeClass.do_something(instance)

#2~~~~
#Избыточный подход
class BigData:
    def __init__(self):
        self._params = []

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self,new_params):
        assert all(map(lambda p: p > 0, new_params))
        self._params = new_params

    @params.deleter
    def params(self):
        del self._params

model = BigData()
model.params = [1,2,3,45]
#print(model.params)
del model.params
#print(model.params)

#3~~~~~~~
#Минималисткий

from os import path
class Path:
    def __init__(self,current):
        self.current = current

    def __repr__(self):
        return 'Path here({})'.format(self.current)

    @property
    def parent(self):
        return Path(path.dirname(self.current))

p = Path('./proba/algs.py')
#print(p.parent)
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------
if __name__== '__main__':
    #main_knapsack()
    #main_find_pos()
    pass

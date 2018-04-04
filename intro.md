
Introduction of Rem Language
--------------------------------

Rem language is currently implemented by CPython, and it's for people who're working on the fields of Python, Julia, R or MATLAB .etc...  

Rem looks like Python, Ruby and many other dynamic languages, and it adopts some convenient features from many functional programming languages.  

The **inverted syntax** in Rem is the core in some degree. As the result of unifying the manipulations on first-class functions, you can write these object-oriented-like codes in the following way:  

```
>> ["foo", "bar"] . map {|x| x ++ "tail"} 
``` 
However it's not really object-oriented, it's functional!  

To explain, the codes above could be represented in Python codes:  

```python
map (lambda x: x + "tail", ["foo", "bar"])
```
(Just **take care** that not all the codes in Rem can be directly translated to Python.  

Also, we can try to imitate `keyword` with functions in Rem:  

```
let x = 0
while { x < 10} {
    x = x + 1
}
``` 
And `while` here is just a function!  

**Pattern Matching** and **Where Syntax** are both tasty, too. You can learn how to use them in the following manual.

All in all, Rem has a lot of features to support comfortable programming with modern paradigms.  

I'm planning to write a C# backend for Rem sooner in order to get rid of too much Python(however we shouldn't ignore the requirements of works in real world),
and efficient compilers will come up, too.  

## Hello World

Install `remlang` easily by using **PyPI** with Python 3.6+.

```shell
pip install remlang
```

If you want to use the `repl`, just type `irem`:
```
irem

Rem Language alpha, March 15 2018 02:14.
Backend CPython, Author thautwarm, MIT License.
Report at https://github.com/thautwarm/Rem/issues.

>> "Hello World"
'Hello World'

>> "Hello World" . print
Hello World
```
## Function(Lambda)

Something you need to take care is that **Functions are curried** in Rem.

```
>> let fn = {|x| x + 1}
>> fn 1
=> 2
>> let fn = {|x, y, z|
    y = y + z + x
    y
}
>> f1 = fn 5
>> f2 = fn 10
>> fn 20
=> 35
=> from x, y, z let x + y + z end # another way to define a lambda
```

A very sweet syntax sugar from `Scala` is now supported.
```
>> 1 . {_ + 1} 
=> 2
>> [1, 2, 3] . map {_ + 1} . list
=> [2, 3, 4]
>> {_1 + _2} 1 2
=> 3
```
Take care that when you're using multiple implicit parameters, you cannot curry it.  

So the following codes would cause runtime error.
```
>> let f = {_1 + _2} 1 
```

## $ operator

```
>> let fn = {|x| x**2}
>> fn 2 + 3
=> 7  # 2**2 + 3
>> fn $ 2 + 3
=> 25 # (2+3) ** 2
>> let fn = {|x, y| x*y}
>> fn $ 1+2 $ 3+4
=>  21 # 3*7 
```

## Scope

Partly **Dynamic Scoping**

```
>> let x = 0
>> call { x }
=> 0
>> call { x = 1; x}
=> 1
>> x
=> 1
>> call {let x = x; x = 10; x}
=> 10
>> x
=> 1
```

## Where Syntax
```
>> dictionary = %{
    c where
        c = 1
    end : 2
  }
>> dictionary
=> {1: 2}

>> from math import pi
>> S = S1 + 2*S2 where
        let S1 = pi*r**2
        let S2 = 2*pi*r
    end
```

## Inverted Syntax
```
>> let add = {|x, y| x + y}
>> 1 . add 2
=> 3
>> 1 then add 2
=> 3
```
However, the **priority** of `.` is different from `then`.

Here is the table of priorities in Rem:

| syntax           | priority  | sample              |
| -------          | ---       | ---                 | 
| then             | 1         | `a then func`       |
| `$`              | 1         | `f $ 1 2`           | 
| case             | 2         | `case ... end`      |
| binary expr      | 2         | `1 * 2`             |
| unary expr       | 3         | `a?`, `a??`, `not a`|
| `.`(inverted)    | 4         | `a . add`           |
| function call    | 4         | `f 1 2`, `call f`   |
|expr with trailers| 5         | `a'name`, `a![0]`  |
| atom             | 6         | lambda and so on    |



```
>> let concat = {|x| print x ; {|y| print y ;x ++ y}}
>> "left" . concat "right"
left
=> "leftright"
>> "right" then add "left"
right
=> "rightleft"
```
Both of them are left associative.


## For Comprehension

Make a generator
```
>> from [1, 2, 3] yield {|x| x+1} . list
=> [2, 3, 4]
>> from [1, 2, 3], ["a", "b", "c"] yield {|a, b| (a, b)} . list
=> [(1, 'a'), (1, 'b'), (1, 'c'), (2, 'a'), (2, 'b'), (2, 'c'), (3, 'a'), (3, 'b'), (3, 'c')]
```

- for-loop: `not yield`

```
>>> from [1, 2, 3] not yield {|x|
        print x
        x
    }
 1
 2
 3
=> 3
```

## Pattern Matching

Very powerfull and can even be the alternative of `if-else`.

```
case (1, 2, 3)
    as 1, ...a when 
        a![0] == 2
    
        => a

    as _ => raise
end
```
You can use it for only destruction:
```
>> case (1, 2, 3) as (a, b, c) end
>> print a*b*c
=> 6
>> let t = case (1, 2, (3, 5, (6, 5))) as [1, 2, [3, 5, [6,...a]]] => a end
>> t
=> <tuple_iterator object at 0x0000017689F95FD0>
>> t. tuple
=> (5, )
>> case 
        %{1: [1, 2, 3], 2: [2, 3, 4]} 
   as 
        {1: a, 2: b} 
   end
>> (a, b)
=> ([1, 2, 3], [2, 3, 4])
```


The return of `pack` destruction(`...a`) is of type tuple when length is 1, or it's of type 
tuple_iterator.

## Into Statement

It is similar to `goto`, but I add some constraints on it: you cannot go to the previous steps,
but you can jump out of current closure until you're in specific closure.

If you want to use `into` in `for comprehension`
```
>> @here
>> from [1, 2, 3] not yield {|x|
    into here
    print x
   }
>> from [1, 2, 3] not yield {|x|
    print x
} 
 1
 2
 3
=> 3
```

Take care that the literal construction of `list`, `tuple`, `set` and `dict` will ignore the `into` keyword, as well as `from ... not yield ...` for-loop.



## Collections

List: Just Python `list`
```
>> let l1 = [
    1,
    2,
    c where
        let c = 3
    end,
    4
]

>> l1 ++ [1, 2, 3] 
=> [1, 2, 3, 4, 1, 2, 3]
>> l1 -- [1, 2, 3]
=> [4]
```

Dict: Just Python `dict`
```
>> let d1 = %{
            1: 2,
            expr where
                let expr = 3
            end : 4
}
```

Set is also Python `set` as well as `tuple`.

## OOP Support

- Access Member and Index
```
# access member
>> import math
>> math 'pi
=>  3.141592653589793
>> math 'pi  '__class__
=>  <class 'float'>

# index
>> import numpy as np
>> let arr_cons = np 'ndarray
>> arr_cons [1, 2, 3]
=>  array([[1, 2, 3]])
>> (arr_cons [[1, 2, 3]]) . slice [0, (1, 2)]
=> array([2])
>> (arr_cons [[1, 2, 3]]) ![indexer [0, (1, 2)]]
=> array([2])
>> (arr_cons [[1, 2, 3]]) ![0]
=> array([1, 2, 3])
```

[class.rem](https://github.com/thautwarm/Rem/blob/master/example_source_codes/class.rem)
```
/* define class here */
let class = {
    |fn_dict|
    # constructor
    {
        let self = call Object
        from 
            fn_dict 'items then call
        not yield {
            |tp|
            case tp as k, v 
                => 
                    self. set k (v self)
            end
        }
        self
    }        
}


# spec
let cls1 = class %{
                "go":  {|x, y| y},
            }

let inst = call cls1

inst'go 1
```












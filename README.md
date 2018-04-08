[![PyPI version](https://img.shields.io/pypi/v/remlang.svg)](https://pypi.python.org/pypi/remlang)
[![Intro](https://img.shields.io/badge/intro-remlang-red.svg)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/LICENSE)


# Rem Langauge

Just use **PyPI**. Recommend to install `cytoolz` before installing Rem to speed up function invocations.  
```shell
pip install remlang
```  

[![Overview](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview++.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview++.png)


## Some Supported Features

See all features at [Inrtoduction](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md).  


- [Pattern Matching](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#pattern-matching)  
    Currently support `case` syntax.  
    ```
    case expr 
        as destruction 
        [when condition]
        => statements
    end
    ```
    
    - Dictionary Pattern Matching
    
    ```
    case %{a: b}
        as {a : &b+1} => 1
        as {a : &b }  => 2
    end 
    ```

    - Function Parameter Destruction
    ```
    >> {|(1, 2, c)| c*2} (1, 2, 3)
    => 6
    ```
- [**Inverted Syntax**](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#inverted-syntax) (see the priority table in the linked page)  
    ```
    file . open . write some_text
    ```
    
    `.` has a high priority while `then` has a lower one.  

    [![Inverted](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/inverted.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/inverted.png)  

    [![$](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/$.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/$.png)



- [Into Statement](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#into-statement)(just like `goto`)  

    [![Into](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/into.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/into.png)


- [Currying Function](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#functionlambda)   

    [![Lambda](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/lambda.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/lambda.png) 


- [Scope](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#scope)  

- [Where Syntax and Block Expression](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#where-syntax)  
    [![Where](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/where.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png)


- [For Comprehension and For Loop](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#for-comprehension)  
    [![For](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png)](https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png)



## 关于中文编程

Rem 支持中文编程, 因为它的tokenizer可以被动态操控，在任意一个Rem模块里，均有一个`__compiler__`对象， 负责处理输入语句到`ast`的转换。当下内置了一个无参函数`中文编程`， 便可以使用中文关键字。  

```
>> call 中文编程
>> 对于 [3, 2] 作为 [甲, 乙] => 甲 * 乙 结束
# 等价于 =>
# case [3, 2] as [甲, 乙] => 甲 * 乙 end
=> 6
```

中英文token对照  
| English           | 中文   |
| -------           | ---    |
| then              | 然后   |
| when              | 当     |
| and               | 并且   |
| or                | 或者   |
| in                | 含于   |
| not               | 非     |
| case              | 对于   |
| as                | 作为   |
| end               | 结束   |
| where             | 其中   |
| from              | 从     |
| yield             | 生成   |
| into              | 跳跃到 |
| let               | 使/让  |
| True              | 真     |
| False             | 假     |
| None              | 空     |
| is                | 是     |
| `.`               | 之     |

    


[![PyPI version](https://img.shields.io/pypi/v/remlang.svg)](https://pypi.python.org/pypi/remlang)
[![Intro](https://img.shields.io/badge/intro-remlang-red.svg)](https://github.com/thautwarm/Rem/blob/master/intro.md)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/thautwarm/Rem/blob/master/LICENSE)


# Available Rem Langauge


## Some Support Features

See all features at [Inrtoduction](./intro.md).

- Pattern Matching
    Currenly support `case` syntax.
    ```
    case expr 
        as destruction 
        [when condition]
        => statements
    end
    ```
    In the future this feature would be applied on arguments for multiple dispatch.

- **Inverted Syntax**

    ```
    file . open then write some_text
    ```
    
    `.` has a high priority while `then` has a lower one.


## 关于中文编程

Rem 支持中文编程来源于它的tokenizer可以被动态操控，在任意一个Rem模块里，均有一个`__token__`对象。当下内置了一个无参函数`中文编程`， 便可以使用中文关键字。

```
>> call 中文编程
>> 当 [3, 2] as [甲, 乙] => 甲 * 乙 end
=> 6
```

    


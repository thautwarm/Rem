|PyPI version| |Intro| |MIT|

Available Rem Langauge
======================

Just use **PyPI**. Recommend to install ``cytoolz`` before installing to
speed up function calls in Rem.

|Overview|

Some Supported Features
-----------------------

See all features at
`Inrtoduction <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md>`__.

-  | `Pattern
     Matching <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#pattern-matching>`__
   | Currenly support ``case`` syntax.

   ::

       case expr 
           as destruction 
           [when condition]
           => statements
       end

   -  Dictionary Pattern Matching

   ::

       case %{a: b}
           as {a : &b+1} => 1
           as {a : &b }  => 2
       end 

   -  Function Parameter Destruction

      ::

          >> {|(1, 2, c)| c*2} (1, 2, 3)
          => 6

   |Intro Picture|

-  `**Inverted
   Syntax** <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#inverted-syntax>`__
   (see the priority table in the linked page)

   ::

       file . open . write some_text

   ``.`` has a high priority while ``then`` has a lower one.

|Inverted|

|$|

-  `Into
   Statement <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#into-statement>`__\ (just
   like ``goto``)

|Into|

-  `Currying
   Function <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#functionlambda>`__

|Lambda|

-  `Scope <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#scope>`__

-  | `Where Syntax and Block
     Expression <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#where-syntax>`__
   | |Where|

-  | `For Comprehension and For
     Loop <https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md#for-comprehension>`__
   | |For|

   ::

       from range

关于中文编程
------------

Rem
支持中文编程来源于它的tokenizer可以被动态操控，在任意一个Rem模块里，均有一个\ ``__compiler__``\ 对象。当下内置了一个无参函数\ ``中文编程``\ ，
便可以使用中文关键字。

::

    >> call 中文编程
    >> 对于 [3, 2] 作为 [甲, 乙] => 甲 * 乙 结束
    # 等价于 case [3, 2] as [甲, 乙] => 甲 * 乙 end
    => 6

中英文token对照

::

    {
        '然后': '`then`',
        '当': '`when`',
        '并且': '`and`',
        '或者': '`or`',
        '含于': '`in`',
        '非': '`not`',
        '对于': '`case`',
        '作为': '`as`',
        '结束': '`end`',
        '其中': '`where`',
        '从': '`from`',
        '生成': '`yield`',
        '跳跃到': '`into`',
        '使': '`let`',
        '让': '`let`',
        '真': '`True`',
        '假': '`False`',
        '空': '`None`',
        '导入': '`import`',
        '是': '`is`',
        '之': '.',
    }

用事实证明中文编程的反人类。

.. |PyPI version| image:: https://img.shields.io/pypi/v/remlang.svg
   :target: https://pypi.python.org/pypi/remlang
.. |Intro| image:: https://img.shields.io/badge/intro-remlang-red.svg
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro.md
.. |MIT| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/LICENSE
.. |Overview| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview++.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview++.png
.. |Intro Picture| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro_pic.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/intro_pic.png
.. |Inverted| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/inverted.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/inverted.png
.. |$| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/$.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/$.png
.. |Into| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/into.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/into.png
.. |Lambda| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/lambda.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/lambda.png
.. |Where| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/where.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png
.. |For| image:: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png
   :target: https://github.com/thautwarm/Rem/blob/ebnfparser2.0/overview-figs/for.png

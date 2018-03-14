[![PyPI version](https://img.shields.io/pypi/v/remlang.svg)](https://pypi.python.org/pypi/remlang)
[![Intro](https://img.shields.io/badge/intro-remlang-red.svg)](https://github.com/thautwarm/Rem/blob/master/intro.md)
[![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/thautwarm/Rem/blob/master/LICENSE)


# Available Rem Langauge

## Support Features

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

- Currying and Ruby-like Lambda

    ```
    let fn = {|x y z| x + y + z}
    let f1 = fn 1
    let f2 = f1 2
    f2 3 then print
    ```

- Unpack and Pack

    ```
    case (1, 2, 3)
        as (1, ...a)
        when a . len == 2
        => a

    let x = (2, 3)

    case (1, 2, 3)
        as (1, &x) 
        /* use value reference to do pattern matching, 
            like `^` in Elixir.
        */
        => True
    end
    ```

- **Where Syntax**

    ```
    r = a + b where
        a = 1
        b = 2
    end
    ```
    `where syntax` makes it possible to unify `expression` and `statement`. However, everything in `Rem` is expression.
     

- `for`-comprehension

    ```
    from (1, 2, 3) yield {|g| g+1} . list . print
    ```


## Example Snippet

```

let str = "I'm in where syntax"
1 . print then {|x|

    case x
        as None
        when
        True where
            print str
        end

        => print 233
    end}

1 + 2 then print



let x = (2, 3)

    case (1, 2, 3)
        as (1, &x)
        => True
    end

let x = (1, ) ++ x

(case x
    as (1, ...a)
    => a
end) . print


x . print

x then print

1 . {|x| x+1} then {|x| x*2} then print

{ |x, y|
    x + y
} 1 2

from (1, 2, 3) yield {|g| g+1} . list . print


%{1, 2, 3} . print

% { c where let c = 1 end : 2, 2: 3}
/* very cool dictionary constructor!!!*/

```



## Ruiko EBNF

```
Token tk
comments ::= '#[\w\W]*';
T        ::= R'\n+' + ;
symbol  ::=  R'[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*';

refName Throw ['&']
        ::=  ['&'] symbol;

number  ::=  R'0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E\-{0,1}\d+|)';

string  ::=  R'"[\w\W]*"';

const   ::=  R'`True`|`False`|`None`';

arg     ::=    ['...']
                ('_'         |
                  refName    |
                  tupleArg   |
                  string
                  ('++'
                  string)+   |
                  const      |
                  number     );

iterMark
        ::= ',';
argMany Throw [',' T]
        ::=  arg [([T] ',' [T] arg)+  [T] [iterMark]];
tupleArg Throw ['(' ')']
        ::= '(' argMany ')';


unaryOp ::= '`not`' | '+' | '-';
suffix  ::= '?'   | '??';

lambdef Throw ['{', '}', '|', ',', T]
        ::= '{'
            ['|' [symbol (',' symbol)*] '|']
            [T]
            [statements [T]]
            '}';

atom  Throw ['++']
        ::=  refName | const | string ('++' string)* | number |
            '(' expr ')'|
             listCons | tupleCons | setCons | dictCons | compreh |
             lambdef;

trailer Throw ['[', ']']
        ::= '[' exprMany ']';

atomExpr Throw['!']
        ::= atom ['!' trailer*];

invExp  ::= atomExpr invTrailer*;
invTrailer Throw ['.']
        ::= '.' atomExpr;

factor ::= [unaryOp] invExp [suffix];

binExp ::= factor (
        ('+'    | '-'   | '*'   | '/' | '%'  |
         '++'   | '--'  | '**'  | '//'|
         '^'    | '&'   | '|'   | '>>'| '<<' |
         '^^'   | '&&'  | '||'  |
         '`and`'| '`or`'| '`in`'|
         '|>'   |
         '>'    | '<'   | '>='  | '<='|
         '=='   | '!='  |
         '<-')
        factor)*;

caseExp Throw ['`case`', '`end`', T]
        ::= '`case`' expr [T] asExp* [otherwiseExp] [T] '`end`';

asExp  Throw ['=>', T, '`as`']
        ::= '`as`' argMany
            [
              [T] '`when`' [T] expr
            ]
            [T]
            ['=>' [T] [statements]];

otherwiseExp Throw ['`otherwise`', T]
        ::= '`otherwise`' [T] [statements [T]];

testExpr ::= caseExp | binExp;

callExp ::= testExpr testExpr*;

where Throw ['`where`', T, '`end`']   ::= '`where`' [T] [statements [T]] '`end`';

expr    ::=  callExp thenTrailer* [where];

thenTrailer Throw ['`then`'] ::= '`then`' callExp;

statements Throw [T]
        ::= [label] statement ([T] statement)*;
statement
        ::= (expr | let | breakUntil) [';'];
let    Throw ['`let`' '=']
        ::= '`let`' symbol '=' expr;

exprMany Throw [',', T] ::= expr [([T] ',' [T] expr)+  [T] [',']];
unpack   Throw ['...']  ::= '...' expr;
exprCons Throw [',']    ::= exprMany (unpack [',' exprMany])* [','];

kv       Throw [':', T] ::= expr ':' expr;
kvMany   Throw [',', T] ::= kv [([T] ',' [T] kv)+  [T] [',']];
kvCons   Throw [',']    ::= kvMany (unpack [',' kvMany])* [','];


listCons  Throw ['[' ']']
        ::= '[' [exprCons] ']';
tupleCons  Throw ['(' ')']
        ::= '(' [exprCons] ')';
setCons  Throw ['%' '{' '}']
        ::=  '%' '{' [exprCons] '}';
dictCons  Throw ['%' '{' '}']
        ::=  '%' '{' [kvCons] '}';

compreh  Throw['`from`' '`yield`']  ::=  '`from`' exprMany '`yield`' lambdef;

label Throw ['@']
           ::= '@' symbol;

breakUntil Throw ['`break-until`']
           ::= '`break-until`' symbol;

file Throw [T] ::= [T] [statements [T]];
```



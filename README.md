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



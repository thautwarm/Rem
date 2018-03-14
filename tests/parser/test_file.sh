python $REM/testIntepreter.py file """

let str = \"I'm in where syntax\"
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
""" -testTk True
python $REM/testLang.py lambdef """{
    print x
}""" -testTk True

python $REM/testLang.py file """{|x, y|
    print x
}"""  -testTk True



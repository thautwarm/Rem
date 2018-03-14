import sys, os

path = os.path.abspath('remlang/compiler')
os.environ['REM'] = path
sys.path.append(os.path.abspath('.'))
sys.path.append(path)

#
# os.system('bash tests/parser/test_arg_many.sh')
# os.system('bash tests/parser/test_lambda.sh')
os.system('bash tests/parser/test_file.sh')
# os.system('bash tests/parser/test_bin_op.sh')

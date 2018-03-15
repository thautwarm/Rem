
from Ruikowa.ObjectRegex.Node import Ref, AstParser, SeqParser, LiteralParser, CharParser, MetaInfo, DependentAstParser
try:
    from .etoken import token
except:
    from etoken import token
import re
namespace     = globals()
recurSearcher = set()
singleImportExpr = AstParser([LiteralParser('`import`', name='\'`import`\''),Ref('singleArgs'),SeqParser([LiteralParser('`as`', name='\'`as`\''),Ref('symbol')], atmost = 1)], name = 'singleImportExpr')
importAs = AstParser([Ref('symbol'),SeqParser([LiteralParser('as', name='\'as\''),Ref('symbol')], atmost = 1)], name = 'importAs')
fromImportExpr = AstParser([LiteralParser('`from`', name='\'`from`\''),Ref('singleArgs'),LiteralParser('`import`', name='\'`import`\''),LiteralParser('(', name='\'(\''),Ref('importAs'),SeqParser([LiteralParser(',', name='\',\''),Ref('importAs')]),LiteralParser(')', name='\')\'')], name = 'fromImportExpr')
importExpr = AstParser([Ref('singleImportExpr')],[Ref('fromImportExpr')],[Ref('remImport')], name = 'importExpr')
remImport = AstParser([LiteralParser('`import`', name='\'`import`\''),Ref('string'),SeqParser([LiteralParser('`as`', name='\'`as`\''),Ref('symbol')], atmost = 1)], name = 'remImport', toIgnore = [{},{'`as`','`import`'}])
comments = AstParser([LiteralParser('#[\w\W]*', name='\'#[\w\W]*\'')], name = 'comments')
T = AstParser([SeqParser([LiteralParser('\n+', name='\'\n+\'', isRegex = True)], atleast = 1)], name = 'T')
symbol = AstParser([LiteralParser('[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff_]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*', name='\'[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff_]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*\'', isRegex = True)], name = 'symbol')
refName = AstParser([SeqParser([LiteralParser('&', name='\'&\'')], atmost = 1),Ref('symbol')], name = 'refName', toIgnore = [{},{'&'}])
number = AstParser([LiteralParser('0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E\-{0,1}\d+|)', name='\'0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E\-{0,1}\d+|)\'', isRegex = True)], name = 'number')
string = AstParser([LiteralParser('"[\w\W]*"', name='\'\"[\w\W]*\"\'', isRegex = True)], name = 'string')
const = AstParser([LiteralParser('`True`|`False`|`None`', name='\'`True`|`False`|`None`\'', isRegex = True)], name = 'const')
arg = AstParser([SeqParser([LiteralParser('...', name='\'...\'')], atmost = 1),DependentAstParser([LiteralParser('_', name='\'_\'')],[Ref('refName')],[Ref('tupleArg')],[Ref('string'),SeqParser([LiteralParser('++', name='\'++\''),Ref('string')], atleast = 1)],[Ref('const')],[Ref('number')])], name = 'arg')
iterMark = AstParser([LiteralParser(',', name='\',\'')], name = 'iterMark')
argMany = AstParser([Ref('arg'),SeqParser([SeqParser([SeqParser([Ref('T')], atmost = 1),LiteralParser(',', name='\',\''),SeqParser([Ref('T')], atmost = 1),Ref('arg')], atleast = 1),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('iterMark')], atmost = 1)], atmost = 1)], name = 'argMany', toIgnore = [{"T"},{','}])
tupleArg = AstParser([LiteralParser('(', name='\'(\''),Ref('argMany'),LiteralParser(')', name='\')\'')], name = 'tupleArg', toIgnore = [{},{'(',')'}])
singleArgs = AstParser([Ref('symbol'),SeqParser([LiteralParser(',', name='\',\''),Ref('symbol')])], name = 'singleArgs', toIgnore = [{},{','}])
unaryOp = AstParser([LiteralParser('`not`', name='\'`not`\'')],[LiteralParser('+', name='\'+\'')],[LiteralParser('-', name='\'-\'')], name = 'unaryOp')
suffix = AstParser([LiteralParser('?', name='\'?\'')],[LiteralParser('??', name='\'??\'')], name = 'suffix')
lambdef = AstParser([LiteralParser('{', name='\'{\''),SeqParser([LiteralParser('|', name='\'|\''),SeqParser([Ref('singleArgs')], atmost = 1),LiteralParser('|', name='\'|\'')], atmost = 1),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('statements'),SeqParser([Ref('T')], atmost = 1)], atmost = 1),LiteralParser('}', name='\'}\'')], name = 'lambdef', toIgnore = [{"T"},{'|','}','{',','}])
atom = AstParser([Ref('refName')],[Ref('const')],[Ref('string'),SeqParser([LiteralParser('++', name='\'++\''),Ref('string')])],[Ref('number')],[LiteralParser('(', name='\'(\''),Ref('expr'),LiteralParser(')', name='\')\'')],[Ref('listCons')],[Ref('tupleCons')],[Ref('setCons')],[Ref('dictCons')],[Ref('compreh')],[Ref('lambdef')], name = 'atom', toIgnore = [{},{'++'}])
trailer = AstParser([LiteralParser('[', name='\'[\''),Ref('exprCons'),LiteralParser(']', name='\']\'')],[LiteralParser('.', name='\'.\''),Ref('symbol')], name = 'trailer', toIgnore = [{},{'.','[',']'}])
atomExpr = AstParser([Ref('atom'),SeqParser([LiteralParser('!', name='\'!\''),SeqParser([SeqParser([Ref('T')], atmost = 1),Ref('trailer')], atleast = 1)], atmost = 1)], name = 'atomExpr', toIgnore = [{"T"},{'!'}])
invExp = AstParser([Ref('atomExpr'),SeqParser([Ref('invTrailer')])], name = 'invExp')
invTrailer = AstParser([LiteralParser('.', name='\'.\''),Ref('atomExpr')], name = 'invTrailer', toIgnore = [{},{'.'}])
factor = AstParser([SeqParser([Ref('unaryOp')], atmost = 1),Ref('invExp'),SeqParser([Ref('suffix')], atmost = 1)], name = 'factor')
binExp = AstParser([Ref('factor'),SeqParser([DependentAstParser([LiteralParser('+', name='\'+\'')],[LiteralParser('-', name='\'-\'')],[LiteralParser('*', name='\'*\'')],[LiteralParser('/', name='\'/\'')],[LiteralParser('%', name='\'%\'')],[LiteralParser('++', name='\'++\'')],[LiteralParser('--', name='\'--\'')],[LiteralParser('**', name='\'**\'')],[LiteralParser('//', name='\'//\'')],[LiteralParser('^', name='\'^\'')],[LiteralParser('&', name='\'&\'')],[LiteralParser('|', name='\'|\'')],[LiteralParser('>>', name='\'>>\'')],[LiteralParser('<<', name='\'<<\'')],[LiteralParser('^^', name='\'^^\'')],[LiteralParser('&&', name='\'&&\'')],[LiteralParser('||', name='\'||\'')],[LiteralParser('`and`', name='\'`and`\'')],[LiteralParser('`or`', name='\'`or`\'')],[LiteralParser('`in`', name='\'`in`\'')],[LiteralParser('`is`', name='\'`is`\'')],[LiteralParser('|>', name='\'|>\'')],[LiteralParser('>', name='\'>\'')],[LiteralParser('<', name='\'<\'')],[LiteralParser('>=', name='\'>=\'')],[LiteralParser('<=', name='\'<=\'')],[LiteralParser('==', name='\'==\'')],[LiteralParser('!=', name='\'!=\'')],[LiteralParser('<-', name='\'<-\'')]),Ref('factor')])], name = 'binExp')
caseExp = AstParser([LiteralParser('`case`', name='\'`case`\''),Ref('expr'),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('asExp')]),SeqParser([Ref('otherwiseExp')], atmost = 1),SeqParser([Ref('T')], atmost = 1),LiteralParser('`end`', name='\'`end`\'')], name = 'caseExp', toIgnore = [{"T"},{'`case`','`end`'}])
asExp = AstParser([LiteralParser('`as`', name='\'`as`\''),Ref('argMany'),SeqParser([SeqParser([Ref('T')], atmost = 1),LiteralParser('`when`', name='\'`when`\''),SeqParser([Ref('T')], atmost = 1),Ref('expr')], atmost = 1),SeqParser([Ref('T')], atmost = 1),SeqParser([LiteralParser('=>', name='\'=>\''),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('statements')], atmost = 1)], atmost = 1)], name = 'asExp', toIgnore = [{"T"},{'`as`','=>'}])
otherwiseExp = AstParser([LiteralParser('`otherwise`', name='\'`otherwise`\''),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('statements'),SeqParser([Ref('T')], atmost = 1)], atmost = 1)], name = 'otherwiseExp', toIgnore = [{"T"},{'`otherwise`'}])
testExpr = AstParser([Ref('caseExp')],[Ref('binExp')], name = 'testExpr')
callExp = AstParser([Ref('testExpr'),SeqParser([Ref('testExpr')])], name = 'callExp')
where = AstParser([LiteralParser('`where`', name='\'`where`\''),SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('statements'),SeqParser([Ref('T')], atmost = 1)], atmost = 1),LiteralParser('`end`', name='\'`end`\'')], name = 'where', toIgnore = [{"T"},{'`where`','`end`'}])
expr = AstParser([Ref('callExp'),SeqParser([Ref('thenTrailer')]),SeqParser([Ref('where')], atmost = 1)], name = 'expr')
thenTrailer = AstParser([LiteralParser('`then`', name='\'`then`\''),Ref('callExp')], name = 'thenTrailer', toIgnore = [{},{'`then`'}])
statements = AstParser([SeqParser([Ref('label')], atmost = 1),Ref('statement'),SeqParser([SeqParser([Ref('T')], atmost = 1),Ref('statement')])], name = 'statements', toIgnore = [{"T"},{}])
statement = AstParser([DependentAstParser([Ref('expr')],[Ref('let')],[Ref('into')],[Ref('importExpr')]),SeqParser([LiteralParser(';', name='\';\'')], atmost = 1)], name = 'statement')
let = AstParser([LiteralParser('`let`', name='\'`let`\''),Ref('symbol'),SeqParser([LiteralParser('!', name='\'!\''),SeqParser([Ref('trailer')], atleast = 1)], atmost = 1),LiteralParser('=', name='\'=\''),Ref('expr')], name = 'let', toIgnore = [{},{'=','!','`let`'}])
exprMany = AstParser([Ref('expr'),SeqParser([SeqParser([SeqParser([Ref('T')], atmost = 1),LiteralParser(',', name='\',\''),SeqParser([Ref('T')], atmost = 1),Ref('expr')], atleast = 1)], atmost = 1)], name = 'exprMany', toIgnore = [{"T"},{','}])
unpack = AstParser([LiteralParser('...', name='\'...\''),Ref('expr')], name = 'unpack', toIgnore = [{},{'...'}])
exprCons = AstParser([Ref('exprMany'),SeqParser([LiteralParser(',', name='\',\''),Ref('unpack'),SeqParser([LiteralParser(',', name='\',\''),Ref('exprMany')], atmost = 1)]),SeqParser([LiteralParser(',', name='\',\'')], atmost = 1)], name = 'exprCons', toIgnore = [{},{','}])
kv = AstParser([Ref('expr'),LiteralParser(':', name='\':\''),Ref('expr')], name = 'kv', toIgnore = [{"T"},{':'}])
kvMany = AstParser([Ref('kv'),SeqParser([SeqParser([SeqParser([Ref('T')], atmost = 1),LiteralParser(',', name='\',\''),SeqParser([Ref('T')], atmost = 1),Ref('kv')], atleast = 1),SeqParser([Ref('T')], atmost = 1)], atmost = 1)], name = 'kvMany', toIgnore = [{"T"},{','}])
kvCons = AstParser([Ref('kvMany'),SeqParser([LiteralParser(',', name='\',\''),Ref('unpack'),SeqParser([LiteralParser(',', name='\',\''),Ref('kvMany')], atmost = 1)]),SeqParser([LiteralParser(',', name='\',\'')], atmost = 1)], name = 'kvCons', toIgnore = [{},{','}])
listCons = AstParser([LiteralParser('[', name='\'[\''),SeqParser([Ref('exprCons')], atmost = 1),LiteralParser(']', name='\']\'')], name = 'listCons', toIgnore = [{},{'[',']'}])
tupleCons = AstParser([LiteralParser('(', name='\'(\''),SeqParser([Ref('exprCons')], atmost = 1),LiteralParser(')', name='\')\'')], name = 'tupleCons', toIgnore = [{},{'(',')'}])
setCons = AstParser([LiteralParser('%', name='\'%\''),LiteralParser('{', name='\'{\''),SeqParser([Ref('exprCons')], atmost = 1),LiteralParser('}', name='\'}\'')], name = 'setCons', toIgnore = [{},{'}','{','%'}])
dictCons = AstParser([LiteralParser('%', name='\'%\''),LiteralParser('{', name='\'{\''),SeqParser([Ref('kvCons')], atmost = 1),LiteralParser('}', name='\'}\'')], name = 'dictCons', toIgnore = [{},{'}','{','%'}])
compreh = AstParser([LiteralParser('`from`', name='\'`from`\''),Ref('exprMany'),LiteralParser('`yield`', name='\'`yield`\''),Ref('lambdef')], name = 'compreh', toIgnore = [{},{'`yield`','`from`'}])
label = AstParser([LiteralParser('@', name='\'@\''),Ref('symbol')], name = 'label', toIgnore = [{},{'@'}])
into = AstParser([LiteralParser('`into`', name='\'`into`\''),Ref('symbol')], name = 'into', toIgnore = [{},{'`into`'}])
file = AstParser([SeqParser([Ref('T')], atmost = 1),SeqParser([Ref('statements'),SeqParser([Ref('T')], atmost = 1)], atmost = 1)], name = 'file', toIgnore = [{"T"},{}])
singleImportExpr.compile(namespace, recurSearcher)
importAs.compile(namespace, recurSearcher)
fromImportExpr.compile(namespace, recurSearcher)
importExpr.compile(namespace, recurSearcher)
remImport.compile(namespace, recurSearcher)
comments.compile(namespace, recurSearcher)
T.compile(namespace, recurSearcher)
symbol.compile(namespace, recurSearcher)
refName.compile(namespace, recurSearcher)
number.compile(namespace, recurSearcher)
string.compile(namespace, recurSearcher)
const.compile(namespace, recurSearcher)
arg.compile(namespace, recurSearcher)
iterMark.compile(namespace, recurSearcher)
argMany.compile(namespace, recurSearcher)
tupleArg.compile(namespace, recurSearcher)
singleArgs.compile(namespace, recurSearcher)
unaryOp.compile(namespace, recurSearcher)
suffix.compile(namespace, recurSearcher)
lambdef.compile(namespace, recurSearcher)
atom.compile(namespace, recurSearcher)
trailer.compile(namespace, recurSearcher)
atomExpr.compile(namespace, recurSearcher)
invExp.compile(namespace, recurSearcher)
invTrailer.compile(namespace, recurSearcher)
factor.compile(namespace, recurSearcher)
binExp.compile(namespace, recurSearcher)
caseExp.compile(namespace, recurSearcher)
asExp.compile(namespace, recurSearcher)
otherwiseExp.compile(namespace, recurSearcher)
testExpr.compile(namespace, recurSearcher)
callExp.compile(namespace, recurSearcher)
where.compile(namespace, recurSearcher)
expr.compile(namespace, recurSearcher)
thenTrailer.compile(namespace, recurSearcher)
statements.compile(namespace, recurSearcher)
statement.compile(namespace, recurSearcher)
let.compile(namespace, recurSearcher)
exprMany.compile(namespace, recurSearcher)
unpack.compile(namespace, recurSearcher)
exprCons.compile(namespace, recurSearcher)
kv.compile(namespace, recurSearcher)
kvMany.compile(namespace, recurSearcher)
kvCons.compile(namespace, recurSearcher)
listCons.compile(namespace, recurSearcher)
tupleCons.compile(namespace, recurSearcher)
setCons.compile(namespace, recurSearcher)
dictCons.compile(namespace, recurSearcher)
compreh.compile(namespace, recurSearcher)
label.compile(namespace, recurSearcher)
into.compile(namespace, recurSearcher)
file.compile(namespace, recurSearcher)

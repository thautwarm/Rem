# This file is automatically generated by EBNFParser.
from Ruikowa.ObjectRegex.Tokenizer import unique_literal_cache_pool, regex_matcher, char_matcher, str_matcher, Tokenizer
from Ruikowa.ObjectRegex.Node import AstParser, Ref, SeqParser, LiteralValueParser as L, LiteralNameParser, Undef
namespace = globals()
recur_searcher = set()
token_table = ((unique_literal_cache_pool["auto_const"], char_matcher(('&'))),
               (unique_literal_cache_pool["newline"], regex_matcher('\n+')),
               (unique_literal_cache_pool["space"], regex_matcher('\s+')),
               (unique_literal_cache_pool["symbol"], regex_matcher('[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff_]{1}[a-zA-Z\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\d_]*')),
               (unique_literal_cache_pool["string"], regex_matcher('"([^\"]+|\\.)*?"')),
               (unique_literal_cache_pool["comments"], regex_matcher('(#.*)|(((/\*)+?[\w\W]+?(\*/)+))')),
               (unique_literal_cache_pool["number"], regex_matcher('0[Xx][\da-fA-F]+|\d+(?:\.\d+|)(?:E\-{0,1}\d+|)')),
               (unique_literal_cache_pool["operator"], str_matcher(('||', '|>', '^^', '>>', '>=', '==', '<=', '<<', '<-', '::', '//', '--', '++', '**', '&&', '!='))),
               (unique_literal_cache_pool["operator"], char_matcher(('^', '>', '<', '/', '-', '+', '*', '&', '%'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('from', 'as', '...'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('.'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('import'))),
               (unique_literal_cache_pool["auto_const"], char_matcher((',', '*', ')', '('))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('True', 'None', 'False'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('_'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('}', '|', '{', ']', '[', ':'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('let', 'end', '++'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('!'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('\''))),
               (unique_literal_cache_pool["suffix"], str_matcher(('??'))),
               (unique_literal_cache_pool["suffix"], char_matcher(('?'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('not'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('-', '+'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('where', 'when', 'or', 'is', 'in', 'case', 'and', '=>'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('`'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('then'))),
               (unique_literal_cache_pool["auto_const"], char_matcher((';', '$'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('='))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('%'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('yield'))),
               (unique_literal_cache_pool["auto_const"], char_matcher(('@'))),
               (unique_literal_cache_pool["auto_const"], str_matcher(('into'))))

class UNameEnum:
# names

    keyword_then = unique_literal_cache_pool['then']
    keyword_when = unique_literal_cache_pool['when']
    keyword_and = unique_literal_cache_pool['and']
    keyword_or = unique_literal_cache_pool['or']
    keyword_not = unique_literal_cache_pool['not']
    keyword_in = unique_literal_cache_pool['in']
    keyword_case = unique_literal_cache_pool['case']
    keyword_as = unique_literal_cache_pool['as']
    keyword_end = unique_literal_cache_pool['end']
    keyword_where = unique_literal_cache_pool['where']
    keyword_from = unique_literal_cache_pool['from']
    keyword_yield = unique_literal_cache_pool['yield']
    keyword_into = unique_literal_cache_pool['into']
    keyword_let = unique_literal_cache_pool['let']
    keyword_True = unique_literal_cache_pool['True']
    keyword_False = unique_literal_cache_pool['False']
    keyword_None = unique_literal_cache_pool['None']
    keyword_import = unique_literal_cache_pool['import']
    keyword_is = unique_literal_cache_pool['is']
    keyword = unique_literal_cache_pool['keyword']
    refName = unique_literal_cache_pool['refName']
    newline = unique_literal_cache_pool['newline']
    space = unique_literal_cache_pool['space']
    symbol = unique_literal_cache_pool['symbol']
    string = unique_literal_cache_pool['string']
    comments = unique_literal_cache_pool['comments']
    number = unique_literal_cache_pool['number']
    operator = unique_literal_cache_pool['operator']
    T = unique_literal_cache_pool['T']
    importAs = unique_literal_cache_pool['importAs']
    fromImportStmt = unique_literal_cache_pool['fromImportStmt']
    importStmt = unique_literal_cache_pool['importStmt']
    singleImportStmt = unique_literal_cache_pool['singleImportStmt']
    remImport = unique_literal_cache_pool['remImport']
    const = unique_literal_cache_pool['const']
    simpleArgs = unique_literal_cache_pool['simpleArgs']
    patMany = unique_literal_cache_pool['patMany']
    iterMark = unique_literal_cache_pool['iterMark']
    pat = unique_literal_cache_pool['pat']
    noZipPat = unique_literal_cache_pool['noZipPat']
    noZipPatMany = unique_literal_cache_pool['noZipPatMany']
    tuplePat = unique_literal_cache_pool['tuplePat']
    kvPat = unique_literal_cache_pool['kvPat']
    kvPatMany = unique_literal_cache_pool['kvPatMany']
    dictPat = unique_literal_cache_pool['dictPat']
    lambdef = unique_literal_cache_pool['lambdef']
    atom = unique_literal_cache_pool['atom']
    trailer = unique_literal_cache_pool['trailer']
    atomExpr = unique_literal_cache_pool['atomExpr']
    invExp = unique_literal_cache_pool['invExp']
    invTrailer = unique_literal_cache_pool['invTrailer']
    suffix = unique_literal_cache_pool['suffix']
    factor = unique_literal_cache_pool['factor']
    binExp = unique_literal_cache_pool['binExp']
    caseExp = unique_literal_cache_pool['caseExp']
    asExp = unique_literal_cache_pool['asExp']
    testExpr = unique_literal_cache_pool['testExpr']
    where = unique_literal_cache_pool['where']
    expr = unique_literal_cache_pool['expr']
    thenTrailer = unique_literal_cache_pool['thenTrailer']
    applicationTrailer = unique_literal_cache_pool['applicationTrailer']
    statements = unique_literal_cache_pool['statements']
    statement = unique_literal_cache_pool['statement']
    let = unique_literal_cache_pool['let']
    exprMany = unique_literal_cache_pool['exprMany']
    unpack = unique_literal_cache_pool['unpack']
    exprCons = unique_literal_cache_pool['exprCons']
    kv = unique_literal_cache_pool['kv']
    kvMany = unique_literal_cache_pool['kvMany']
    kvCons = unique_literal_cache_pool['kvCons']
    listCons = unique_literal_cache_pool['listCons']
    tupleCons = unique_literal_cache_pool['tupleCons']
    setCons = unique_literal_cache_pool['setCons']
    dictCons = unique_literal_cache_pool['dictCons']
    compreh = unique_literal_cache_pool['compreh']
    label = unique_literal_cache_pool['label']
    into = unique_literal_cache_pool['into']
    file = unique_literal_cache_pool['file']
        
cast_map = {'then': unique_literal_cache_pool['keyword'], 'when': unique_literal_cache_pool['keyword'], 'and': unique_literal_cache_pool['keyword'], 'or': unique_literal_cache_pool['keyword'], 'not': unique_literal_cache_pool['keyword'], 'in': unique_literal_cache_pool['keyword'], 'case': unique_literal_cache_pool['keyword'], 'as': unique_literal_cache_pool['keyword'], 'end': unique_literal_cache_pool['keyword'], 'where': unique_literal_cache_pool['keyword'], 'from': unique_literal_cache_pool['keyword'], 'yield': unique_literal_cache_pool['keyword'], 'into': unique_literal_cache_pool['keyword'], 'let': unique_literal_cache_pool['keyword'], 'True': unique_literal_cache_pool['keyword'], 'False': unique_literal_cache_pool['keyword'], 'None': unique_literal_cache_pool['keyword'], 'import': unique_literal_cache_pool['keyword'], 'is': unique_literal_cache_pool['keyword']}
token_func = lambda _: Tokenizer.from_raw_strings(_, token_table, ({"space", "comments"}, {}),cast_map=cast_map)
keyword = LiteralNameParser('keyword')
newline = LiteralNameParser('newline')
space = LiteralNameParser('space')
symbol = LiteralNameParser('symbol')
string = LiteralNameParser('string')
comments = LiteralNameParser('comments')
number = LiteralNameParser('number')
operator = LiteralNameParser('operator')
suffix = LiteralNameParser('suffix')
refName = AstParser([SeqParser(['&'], at_least=0,at_most=1), Ref('symbol')],
                    name="refName",
                    to_ignore=({}, {}))
T = AstParser([SeqParser([Ref('newline')], at_least=1,at_most=Undef)],
              name="T",
              to_ignore=({}, {}))
importAs = AstParser([Ref('symbol'), SeqParser(['as', Ref('symbol')], at_least=0,at_most=1)],
                     name="importAs",
                     to_ignore=({}, {}))
fromImportStmt = AstParser(['from', SeqParser(['...'], [SeqParser(['.'], at_least=1,at_most=1)], at_least=0,at_most=1), Ref('symbol'), SeqParser(['.', Ref('symbol')], at_least=0,at_most=Undef), 'import', SeqParser(['*'], [SeqParser([Ref('importAs')], at_least=1,at_most=Undef)], ['(', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('importAs'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('importAs')], at_least=0,at_most=Undef), ')'], at_least=1,at_most=1)],
                           name="fromImportStmt",
                           to_ignore=({}, {}))
importStmt = AstParser([Ref('singleImportStmt')],
                       [Ref('fromImportStmt')],
                       [Ref('remImport')],
                       name="importStmt",
                       to_ignore=({}, {}))
singleImportStmt = AstParser(['import', Ref('simpleArgs'), SeqParser(['as', Ref('symbol')], at_least=0,at_most=1)],
                             name="singleImportStmt",
                             to_ignore=({}, {}))
remImport = AstParser(['import', Ref('string'), SeqParser(['as', Ref('symbol')], at_least=0,at_most=1)],
                      name="remImport",
                      to_ignore=({}, {'import', 'as'}))
const = AstParser(['True'],
                  ['False'],
                  ['None'],
                  name="const",
                  to_ignore=({}, {}))
simpleArgs = AstParser([Ref('symbol'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('symbol')], at_least=0,at_most=Undef)],
                       name="simpleArgs",
                       to_ignore=({"T"}, {','}))
patMany = AstParser([Ref('pat'), SeqParser([SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('pat')], at_least=1,at_most=Undef), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), SeqParser([Ref('iterMark')], at_least=0,at_most=1)],
                    name="patMany",
                    to_ignore=({"T"}, {','}))
iterMark = AstParser([','],
                     name="iterMark",
                     to_ignore=({}, {}))
pat = AstParser([SeqParser(['...'], at_least=0,at_most=1), '_'],
                [SeqParser(['...'], at_least=0,at_most=1), Ref('refName')],
                [Ref('tuplePat')],
                [Ref('dictPat')],
                [Ref('string')],
                [Ref('const')],
                [Ref('number')],
                name="pat",
                to_ignore=({}, {}))
noZipPat = AstParser([Ref('refName')],
                     [Ref('tuplePat')],
                     [Ref('dictPat')],
                     [Ref('string')],
                     [Ref('const')],
                     [Ref('number')],
                     name="noZipPat",
                     to_ignore=({}, {}))
noZipPatMany = AstParser([Ref('noZipPat'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('noZipPat')], at_least=0,at_most=Undef)],
                         name="noZipPatMany",
                         to_ignore=({"T"}, {','}))
tuplePat = AstParser(['(', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('patMany'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), ')'],
                     ['[', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('patMany'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), ']'],
                     name="tuplePat",
                     to_ignore=({"T"}, {'(', ')', '[', ']'}))
kvPat = AstParser([Ref('expr'), ':', Ref('noZipPat')],
                  name="kvPat",
                  to_ignore=({}, {':'}))
kvPatMany = AstParser([Ref('kvPat'), SeqParser([SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('kvPat')], at_least=1,at_most=Undef), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), SeqParser([','], at_least=0,at_most=1)],
                      name="kvPatMany",
                      to_ignore=({"T"}, {','}))
dictPat = AstParser(['{', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('kvPatMany'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), '}'],
                    name="dictPat",
                    to_ignore=({"T"}, {'{', '}'}))
lambdef = AstParser(['{', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser(['|', SeqParser([SeqParser([Ref('simpleArgs')], [Ref('noZipPatMany')], at_least=1,at_most=1), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), '|'], at_least=0,at_most=1), SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('statements'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), '}'],
                    ['from', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([SeqParser([Ref('simpleArgs')], [Ref('noZipPatMany')], at_least=1,at_most=1), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), 'let', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('statements'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), 'end'],
                    name="lambdef",
                    to_ignore=({"T"}, {'{', '}', '|', ',', 'from', 'let', 'end'}))
atom = AstParser([Ref('refName')],
                 [Ref('const')],
                 [Ref('string'), SeqParser(['++', Ref('string')], at_least=0,at_most=Undef)],
                 [Ref('number')],
                 ['(', Ref('expr'), ')'],
                 [Ref('listCons')],
                 [Ref('tupleCons')],
                 [Ref('setCons')],
                 [Ref('dictCons')],
                 [Ref('compreh')],
                 [Ref('lambdef')],
                 name="atom",
                 to_ignore=({}, {'++'}))
trailer = AstParser(['!', '[', Ref('exprCons'), ']'],
                    ['\'', Ref('symbol')],
                    name="trailer",
                    to_ignore=({}, {'!', '[', ']', '\''}))
atomExpr = AstParser([Ref('atom'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), Ref('trailer')], at_least=0,at_most=Undef)],
                     name="atomExpr",
                     to_ignore=({"T"}, {}))
invExp = AstParser([Ref('atomExpr'), SeqParser([Ref('atomExpr')], [SeqParser([Ref('T')], at_least=0,at_most=1), Ref('invTrailer')], at_least=0,at_most=Undef)],
                   name="invExp",
                   to_ignore=({"T"}, {}))
invTrailer = AstParser(['.', Ref('atomExpr')],
                       name="invTrailer",
                       to_ignore=({}, {'.'}))
factor = AstParser([SeqParser(['not'], ['+'], ['-'], at_least=0,at_most=1), Ref('invExp'), SeqParser([Ref('suffix')], at_least=0,at_most=1)],
                   name="factor",
                   to_ignore=({}, {}))
binExp = AstParser([Ref('factor'), SeqParser([SeqParser([Ref('operator')], ['or'], ['and'], ['in'], ['is'], at_least=1,at_most=1), Ref('factor')], at_least=0,at_most=Undef)],
                   name="binExp",
                   to_ignore=({}, {}))
caseExp = AstParser(['case', Ref('expr'), SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('asExp')], at_least=0,at_most=Undef), 'end'],
                    name="caseExp",
                    to_ignore=({"T"}, {'case', 'end'}))
asExp = AstParser([SeqParser(['as', Ref('patMany')], at_least=0,at_most=1), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), 'when', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('expr')], at_least=0,at_most=1), SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser(['=>', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('statements')], at_least=0,at_most=1)], at_least=0,at_most=1)],
                  name="asExp",
                  to_ignore=({"T"}, {'=>', 'as', 'when'}))
testExpr = AstParser([Ref('caseExp')],
                     [Ref('binExp')],
                     name="testExpr",
                     to_ignore=({}, {}))
where = AstParser(['where', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('statements'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), 'end'],
                  name="where",
                  to_ignore=({"T"}, {'where', 'end'}))
expr = AstParser(['`', Ref('expr')],
                 [Ref('testExpr'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), Ref('thenTrailer')], [SeqParser([Ref('T')], at_least=0,at_most=1), Ref('applicationTrailer')], at_least=0,at_most=Undef), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), Ref('where')], at_least=0,at_most=1)],
                 name="expr",
                 to_ignore=({"T"}, {}))
thenTrailer = AstParser(['then', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('testExpr')],
                        name="thenTrailer",
                        to_ignore=({"T"}, {'then'}))
applicationTrailer = AstParser(['$', Ref('testExpr')],
                               name="applicationTrailer",
                               to_ignore=({}, {'$'}))
statements = AstParser([Ref('statement'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), Ref('statement')], at_least=0,at_most=Undef)],
                       name="statements",
                       to_ignore=({"T"}, {}))
statement = AstParser([SeqParser([Ref('label')], [Ref('let')], [Ref('expr')], [Ref('into')], [Ref('importStmt')], at_least=1,at_most=1), SeqParser([';'], at_least=0,at_most=1)],
                      name="statement",
                      to_ignore=({}, {}))
let = AstParser([SeqParser(['let'], at_least=0,at_most=1), Ref('symbol'), SeqParser([Ref('trailer')], at_least=0,at_most=Undef), '=', Ref('expr')],
                name="let",
                to_ignore=({}, {'=', '!'}))
exprMany = AstParser([Ref('expr'), SeqParser([SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('expr')], at_least=1,at_most=Undef)], at_least=0,at_most=1)],
                     name="exprMany",
                     to_ignore=({"T"}, {','}))
unpack = AstParser(['...', Ref('expr')],
                   name="unpack",
                   to_ignore=({}, {'...'}))
exprCons = AstParser([Ref('exprMany'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('unpack'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('exprMany')], at_least=0,at_most=1)], at_least=0,at_most=Undef), SeqParser([','], at_least=0,at_most=1)],
                     name="exprCons",
                     to_ignore=({"T"}, {','}))
kv = AstParser([Ref('expr'), ':', Ref('expr')],
               name="kv",
               to_ignore=({"T"}, {':'}))
kvMany = AstParser([Ref('kv'), SeqParser([SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('kv')], at_least=1,at_most=Undef), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1)],
                   name="kvMany",
                   to_ignore=({"T"}, {','}))
kvCons = AstParser([Ref('kvMany'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('unpack'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), ',', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('kvMany')], at_least=0,at_most=1)], at_least=0,at_most=Undef), SeqParser([','], at_least=0,at_most=1)],
                   name="kvCons",
                   to_ignore=({"T"}, {','}))
listCons = AstParser(['[', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('exprCons'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), ']'],
                     name="listCons",
                     to_ignore=({"T"}, {'[', ']'}))
tupleCons = AstParser(['(', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('exprCons'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), ')'],
                      name="tupleCons",
                      to_ignore=({"T"}, {'(', ')'}))
setCons = AstParser(['%', '{', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('exprCons'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), '}'],
                    name="setCons",
                    to_ignore=({"T"}, {'%', '{', '}'}))
dictCons = AstParser(['%', '{', SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('kvCons'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1), '}'],
                     name="dictCons",
                     to_ignore=({"T"}, {'%', '{', '}'}))
compreh = AstParser(['from', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('exprMany'), SeqParser([SeqParser([Ref('T')], at_least=0,at_most=1), 'not'], at_least=0,at_most=1), SeqParser([Ref('T')], at_least=0,at_most=1), 'yield', SeqParser([Ref('T')], at_least=0,at_most=1), Ref('lambdef')],
                    name="compreh",
                    to_ignore=({"T"}, {'from', 'yield'}))
label = AstParser(['@', Ref('symbol')],
                  name="label",
                  to_ignore=({}, {'@'}))
into = AstParser(['into', Ref('symbol')],
                 name="into",
                 to_ignore=({}, {'into'}))
file = AstParser([SeqParser([Ref('T')], at_least=0,at_most=1), SeqParser([Ref('statements'), SeqParser([Ref('T')], at_least=0,at_most=1)], at_least=0,at_most=1)],
                 name="file",
                 to_ignore=({"T"}, {}))
file.compile(namespace, recur_searcher)
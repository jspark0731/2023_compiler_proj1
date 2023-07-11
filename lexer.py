import ply.lex as lex
import re

class Lexer(object):
    # Java의 모든 키워드를 포함
    keywords = {
        'this', 'class', 'void', 'super', 'extends', 'implements', 'enum', 'interface',
        'byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean', 'null',
        'true', 'false',
        'final', 'public', 'protected', 'private', 'abstract', 'static', 'strictfp', 'transient', 'volatile',
        'synchronized', 'native',
        'throws', 'default',
        'instanceof',
        'if', 'else', 'while', 'for', 'switch', 'case', 'assert', 'do',
        'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally', 'new',
        'package', 'import'
    }

    tokens = [
        'vtype',
        'num',
        'character',
        'boolstr',
        'literal',
        'id',
        'cfg_if',
        'cfg_else',
        'cfg_while',
        'cfg_return',
        'cfg_class',
        'addsub',
        'multdiv',
        'assign',
        'comp',
        'semi',
        'comma',
        'lparen',
        'rparen',
        'lbrace',
        'rbrace',
    ] + list(keywords)

    # 각 토큰에 대한 정규 표현식
    t_vtype = r'\b(void|int|double|bool|char|String)\b'
    t_num = r'\b\d+\b'
    t_character = r'\'.'  # 단일 문자
    t_boolstr = r'\b(true|false)\b'
    t_literal = r'\".*?\"'  # 문자열
    t_addsub = r'\+|-'
    t_multdiv = r'\*|/'
    t_assign = r'='
    t_comp = r'==|!=|<=|>=|<|>'
    t_semi = r';'
    t_comma = r','
    t_lparen = r'\('
    t_rparen = r'\)'
    t_lbrace = r'\{'
    t_rbrace = r'\}'
    t_cfg_if = r'if'
    t_cfg_else = r'else'
    t_cfg_while = r'while'
    t_cfg_return = r'return'
    t_cfg_class = r'class'

    # 식별자와 키워드에 대한 정의
    def t_id(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in self.keywords:  # keywords를 확인하고 그렇지 않은 경우에만 id로 확인
            if t.value in ['void', 'int', 'double', 'bool', 'char', 'String']:  # 이 부분이 추가됩니다.
                t.type = 'vtype'
            else:
                t.type = t.value
        return t

    # 라인 번호 추적
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # 공백 무시
    t_ignore = ' \t'

    def find_column(input, token):
        i = token.lexpos
        while i > 0 and input[i] != '\n':
            i -= 1
        column = (token.lexpos - i) + 1
        return column

    # 오류 처리 규칙
    def t_error(self, t):
        column = find_column(code, t)  # 토큰 위치 찾기
        print(f"Illegal character {t.value[0]} at line {t.lineno}, column {column}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def input(self, data):
        return self.lexer.input(data)

    def __iter__(self):
        return iter(self.lexer)

# 렉서 구축
lexer = Lexer()

# 렉싱 할 코드 파일 입력. "myfile.txt"
with open('input_code.txt', 'r') as file:
    code = file.read()

# 렉서를 사용하여 소스 코드를 토큰화
with open('tokens.txt', 'w') as f:
    lexer.input(code)
    for token in lexer:  # `lexer` 객체를 직접 반복
        f.write(token.type + ' ')  # 모든 토큰을 한 줄에 공백으로 구분하여 출력
    f.write('\n')


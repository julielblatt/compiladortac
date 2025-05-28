from analisador_lexico import analisador_lexico
from ast import (
    ProgramNode, AssignNode, ReturnNode,
    BinOpNode, NumberNode, VariableNode,
    FuncDeclNode, FuncCallNode
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def consumir(self, tipo_esperado):
        tipo, valor = self.token_atual()
        if tipo == tipo_esperado:
            self.pos += 1
            return valor
        raise SyntaxError(f"Esperado {tipo_esperado}, encontrado {tipo} ({valor})")

    def parse(self):
        comandos = self.cmd_list()
        return ProgramNode(comandos)

    def cmd_list(self):
        comandos = []
        while self.token_atual()[0] in ['KEYWORD', 'ID']:
            comandos.append(self.cmd())
        return comandos

    def cmd(self):
        tipo, val = self.token_atual()

        if val == 'return':
            self.consumir('KEYWORD')
            expr = self.exp()
            self.consumir('SYMBOL')  # ;
            return ReturnNode(expr)

        elif val == 'func':
            self.consumir('KEYWORD')
            nome = self.consumir('ID')
            self.consumir('SYMBOL')  # (
            params = self.param_list()
            self.consumir('SYMBOL')  # )
            body = self.bloco()
            return FuncDeclNode(nome, params, body)

        elif tipo == 'ID':
            lookahead = self.tokens[self.pos + 1][1] if self.pos + 1 < len(self.tokens) else ''
            if lookahead == '(':
                func_call = self.factor()
                self.consumir('SYMBOL')  # ;
                return func_call  # Chamadas são expressões e comandos aqui
            else:
                atrib = self.atribuicao()
                self.consumir('SYMBOL')  # ;
                return atrib

        else:
            raise SyntaxError(f"Comando inválido: {val}")

    def atribuicao(self):
        var = self.consumir('ID')
        op = self.consumir('OP')
        expr = self.exp()
        if op != '=':
            raise SyntaxError("Atribuição precisa usar '='")
        return AssignNode(var, expr)

    def exp(self):
        node = self.term()
        while self.token_atual()[1] in ['+', '-']:
            op = self.consumir('OP')
            right = self.term()
            node = BinOpNode(op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.token_atual()[1] in ['*', '/']:
            op = self.consumir('OP')
            right = self.factor()
            node = BinOpNode(op, node, right)
        return node

    def factor(self):
        tipo, val = self.token_atual()
        if tipo == 'NUMBER':
            self.consumir('NUMBER')
            return NumberNode(int(val))
        elif tipo == 'ID':
            nome = self.consumir('ID')
            if self.token_atual()[1] == '(':
                self.consumir('SYMBOL')
                args = self.arg_list()
                self.consumir('SYMBOL')
                return FuncCallNode(nome, args)
            else:
                return VariableNode(nome)
        elif val == '(':
            self.consumir('SYMBOL')
            expr = self.exp()
            self.consumir('SYMBOL')
            return expr
        else:
            raise SyntaxError(f"Fator inválido: {val}")

    def bloco(self):
        self.consumir('SYMBOL')  # {
        comandos = self.cmd_list()
        self.consumir('SYMBOL')  # }
        return ProgramNode(comandos)

    def param_list(self):
        params = []
        if self.token_atual()[0] == 'ID':
            params.append(self.consumir('ID'))
            while self.token_atual()[1] == ',':
                self.consumir('SYMBOL')
                params.append(self.consumir('ID'))
        return params

    def arg_list(self):
        args = []
        if self.token_atual()[0] != 'SYMBOL' or self.token_atual()[1] != ')':
            args.append(self.exp())
            while self.token_atual()[1] == ',':
                self.consumir('SYMBOL')
                args.append(self.exp())
        return args

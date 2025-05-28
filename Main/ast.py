class ASTNode:
    def gerar_tac(self, contexto):
        raise NotImplementedError()

    def verificar_semantica(self, contexto):
        raise NotImplementedError()


class ProgramNode(ASTNode):
    def __init__(self, comandos):
        self.comandos = comandos

    def gerar_tac(self, contexto):
        for cmd in self.comandos:
            cmd.gerar_tac(contexto)

    def verificar_semantica(self, contexto):
        for cmd in self.comandos:
            cmd.verificar_semantica(contexto)


class AssignNode(ASTNode):
    def __init__(self, var, value):
        self.var = var
        self.value = value

    def gerar_tac(self, contexto):
        temp = self.value.gerar_tac(contexto)
        contexto.emit(f"{self.var} = {temp}")

    def verificar_semantica(self, contexto):
        if not contexto.foi_declarado(self.var):
            contexto.declarar(self.var, "variável")
        self.value.verificar_semantica(contexto)


class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def gerar_tac(self, contexto):
        temp = self.value.gerar_tac(contexto)
        contexto.emit(f"return {temp}")

    def verificar_semantica(self, contexto):
        self.value.verificar_semantica(contexto)


class BinOpNode(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def gerar_tac(self, contexto):
        t1 = self.left.gerar_tac(contexto)
        t2 = self.right.gerar_tac(contexto)
        temp = contexto.novo_temp()
        contexto.emit(f"{temp} = {t1} {self.op} {t2}")
        return temp

    def verificar_semantica(self, contexto):
        self.left.verificar_semantica(contexto)
        self.right.verificar_semantica(contexto)


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def gerar_tac(self, contexto):
        return str(self.value)

    def verificar_semantica(self, contexto):
        pass  # Número é sempre válido


class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def gerar_tac(self, contexto):
        return self.name

    def verificar_semantica(self, contexto):
        if not contexto.foi_declarado(self.name):
            contexto.erros.append(f"Erro: variável '{self.name}' usada mas não declarada")


class FuncDeclNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def gerar_tac(self, contexto):
        contexto.emit(f"func {self.name}({', '.join(self.params)})")
        self.body.gerar_tac(contexto)
        contexto.emit("endfunc")

    def verificar_semantica(self, contexto):
        contexto.declarar(self.name, "função")
        contexto.entrar_escopo(self.name)
        for param in self.params:
            contexto.declarar(param, "parâmetro")
        self.body.verificar_semantica(contexto)
        contexto.sair_escopo()


class FuncCallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def gerar_tac(self, contexto):
        temps = [arg.gerar_tac(contexto) for arg in self.args]
        temp = contexto.novo_temp()
        contexto.emit(f"{temp} = call {self.name}({', '.join(temps)})")
        return temp

    def verificar_semantica(self, contexto):
        if not contexto.foi_declarado(self.name):
            contexto.erros.append(f"Erro: função '{self.name}' chamada mas não declarada")
        for arg in self.args:
            arg.verificar_semantica(contexto)

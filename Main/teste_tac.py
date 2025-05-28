from analisador_lexico import analisador_lexico
from parser import Parser
from contexto_tac import ContextoTAC
from contexto_semantico import ContextoSemantico
from imprimir_ast import print_ast
codigo = '''
z = 4;
x = soma(2, 3);
y = soma(n, 2)*2; 
'''

tokens = analisador_lexico(codigo)
parser = Parser(tokens)
ast = parser.parse()
print("\nÁrvore Sintática (AST):")
print_ast(ast)

# Semântica
ctx_sem = ContextoSemantico()
ast.verificar_semantica(ctx_sem)
ctx_sem.imprimir_erros()
ctx_sem.imprimir_tabela()


# TAC
ctx_tac = ContextoTAC()
ast.gerar_tac(ctx_tac)
ctx_tac.imprimir()



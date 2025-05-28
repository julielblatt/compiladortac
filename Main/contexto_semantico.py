class ContextoSemantico:
    def __init__(self):
        self.escopo = ["global"]
        self.simbolos = []
        self.erros = []

    def escopo_atual(self):
        if len(self.escopo) == 1:
            return self.escopo[0]  # Ex: "global"
        return self.escopo[-1]
    def entrar_escopo(self, nome):
        self.escopo.append(nome)

    def sair_escopo(self):
        self.escopo.pop()

    def declarar(self, nome, tipo):
        if self.declarado_no_escopo(nome):
            self.erros.append(f"Erro: '{nome}' já declarado no escopo {self.escopo_atual()}")
        else:
            self.simbolos.append({
                "nome": nome,
                "tipo": tipo,
                "escopo": self.escopo_atual()
            })

    def declarado_no_escopo(self, nome):
        return any(s["nome"] == nome and s["escopo"] == self.escopo_atual() for s in self.simbolos)

    def foi_declarado(self, nome):
        return any(s["nome"] == nome for s in self.simbolos)

    def imprimir_tabela(self):
        print("\nTabela de símbolos:")
        for s in self.simbolos:
            print(s)

    def imprimir_erros(self):
        if not self.erros:
            print("\nNenhum erro semântico encontrado.")
        else:
            print("\nErros semânticos:")
            for e in self.erros:
                print(e)

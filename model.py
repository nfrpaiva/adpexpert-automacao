class Inconsistencia:
    def __init__(self, nome, entrada, saida, eh_final_de_semana, periodo_trabalhado, possui_horas_extras, horas_extras):
        self.nome = nome
        self.entrada = entrada
        self.saida = saida
        self.eh_final_de_semana = eh_final_de_semana
        self.periodo_trabalhado = periodo_trabalhado
        self.possui_horas_extras = possui_horas_extras
        self.horas_extras = horas_extras

    def __str__(self):
        return f"Entrada: {self.entrada} - Saída: {self.saida} Final de semana {self.eh_final_de_semana} - Período Trabalhado: {self.periodo_trabalhado} - Horas Extras: {self.horas_extras} - Colaborador: {self.nome}"

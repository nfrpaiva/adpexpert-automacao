class Inconsistencia:
    def __init__(self, nome, horarios, eh_final_de_semana, periodo_trabalhado, possui_horas_extras, horas_extras, element_suggestion):
        self.nome = nome
        self.horarios = horarios
        self.eh_final_de_semana = eh_final_de_semana
        self.periodo_trabalhado = periodo_trabalhado
        self.possui_horas_extras = possui_horas_extras
        self.horas_extras = horas_extras
        self.element_suggestion = element_suggestion

    def str_horarios(self):
        str_horarios = []
        for horario in self.horarios:
            str_horarios.append(f"{str(horario[0])} - {str(horario[1])}")
        return "//".join(str_horarios)

    def __str__(self):
        return f"Horarios: {self.str_horarios()} Final de semana {self.eh_final_de_semana} - Período Trabalhado: {self.periodo_trabalhado} - Horas Extras: {self.horas_extras} - Colaborador: {self.nome}"

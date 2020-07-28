import aprovacao_automatica
import unittest
import datetime

class TestCalculoHora(unittest.TestCase):
    def test_um_dia_de_semana_sem_horas_extras(self):
        str_entrada = "2020-07-27T08:15:00.000"
        str_saida = "2020-07-27T17:30:00.000"
        datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = aprovacao_automatica.calcular_horas(str_entrada, str_saida)
        self.assertEqual(datetime_entrada, datetime.datetime(2020,7,27,8,15,0,0))
        self.assertEqual(datetime_saida, datetime.datetime(2020,7,27,17,30,0,0))
        self.assertEqual(periodo_trabalhado, datetime.timedelta(hours=9, minutes=15))
        self.assertFalse(eh_final_de_semana)
        self.assertEqual(horas_extras,datetime.timedelta(hours=0))
        self.assertFalse(possui_horas_extras)
    
    def test_um_dia_de_semana_com_horas_extras(self):
        str_entrada = "2020-07-27T08:15:00.000"
        str_saida = "2020-07-27T18:00:00.000"
        datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = aprovacao_automatica.calcular_horas(str_entrada, str_saida)
        self.assertEqual(datetime_entrada, datetime.datetime(2020,7,27,8,15,0,0))
        self.assertEqual(datetime_saida, datetime.datetime(2020,7,27,18,00,0,0))
        self.assertEqual(periodo_trabalhado, datetime.timedelta(hours=9, minutes=45))
        self.assertFalse(eh_final_de_semana)
        self.assertEqual(horas_extras,datetime.timedelta(hours=0, minutes=30))
        self.assertTrue(possui_horas_extras)

    def test_um_final_de_semana_com_horas_extras(self):
        str_entrada = "2020-07-26T15:00:00.000"
        str_saida = "2020-07-26T16:00:00.000"
        datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = aprovacao_automatica.calcular_horas(str_entrada, str_saida)
        self.assertEqual(datetime_entrada, datetime.datetime(2020,7,26,15,00,0,0))
        self.assertEqual(datetime_saida, datetime.datetime(2020,7,26,16,00,0,0))
        self.assertEqual(periodo_trabalhado, datetime.timedelta(hours=1, minutes=0))
        self.assertTrue(eh_final_de_semana)
        self.assertEqual(horas_extras,datetime.timedelta(hours=1, minutes=0))
        self.assertTrue(possui_horas_extras)

    def test_um_dia_de_semana_com_horas_negativas(self):
        str_entrada = "2020-07-27T08:15:00.000"
        str_saida = "2020-07-27T17:15:00.000"
        datetime_entrada, datetime_saida, periodo_trabalhado, eh_final_de_semana, horas_extras, possui_horas_extras = aprovacao_automatica.calcular_horas(str_entrada, str_saida)
        self.assertEqual(datetime_entrada, datetime.datetime(2020,7,27,8,15,0,0))
        self.assertEqual(datetime_saida, datetime.datetime(2020,7,27,17,15,0,0))
        self.assertEqual(str(periodo_trabalhado), str(datetime.timedelta(hours=9, minutes=00)))
        self.assertFalse(eh_final_de_semana)
        self.assertEqual(str(horas_extras),str(datetime.timedelta(hours=0, minutes=-15)))
        self.assertFalse(possui_horas_extras)
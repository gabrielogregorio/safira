"""Encontra lixo no código"""

#def localizar_temas_nao_usados():
#   "localiza chaves em temas que não foram usados"


import os
import re

lista = []
for base, _, files in os.walk('.\\'):
    for file in files:
        dir = os.path.join(base, file)
        if '.git\\' not in dir and dir.endswith('.py') and not '.github' in dir and not '__pycache__' in dir:
            with open(dir, 'r', encoding='utf-8') as f:
                texto = f.read()
                res = re.findall('''self.design.dic\\[\\s*['"]\\s*(.*?)\\s*['"]\\s*''', texto)
                if res is not None:
                    for item in res:
                        if item not in lista:
                            lista.append(item)

                res = re.findall('''self.design.get\\(\\s*"\\s*(.*?)\\s*"\\s*\\)''', texto)
                if res is not None:
                    for item in res:
                        if item not in lista:
                            lista.append(item)


lista2 = ["msg_erro_fr1","msg_erro_fr2","msg_erro_tx1","msg_erro_tx1_disable","msg_erro_bt1","msg_erro_bt2","idioma_tp","idioma_fr","idioma_fr2","idioma_fr3","idioma_fr4","idioma_lb","idioma_lb2","idioma_lb3","idioma_bt","idioma_bt2","splash_cor_intro","cor_menu","lb_sobDeTitulo","lb_sobDAutores","lb_sobDesenAno","tx_codificacao","scrollbar_text","dicBtnMenus","fr_dict_aviso","dicBtnAviso","dicBtnCopiarColar","dic_cor_abas_frame","dic_cor_abas","dic_cor_abas_focada","dic_cor_abas_nao_focada","dic_cor_marcador_focado","dic_cor_marcador_nao_focado","abas_botao_fechar_focado","abas_botao_fechar_desfocado","dic_cor_abas_botao_fechar_focado_focada","fr_opcoes_rapidas","lb_linhas","tx_terminal","tx_terminal_debug_fr1","tx_terminal_debug_fr2","tx_terminal_debug_bt1","tx_pesqu","titulo_terminal","linha_terminal","cor_grid_variaveis","cor_grid_variaveis_texto_busca","cor_grid_variaveis_campo_busca","cor_grid_variaveis_scrollbar","cor_grid_treeview_red_tag","fr_ajuda","fr_princ","tela","fr_ajuda_comando","lb_ajuda_texto_c","lb_ajuda_descr_c","fonte_ct_linha","aviso_versao_top_level","aviso_versao_tp_atualizada","aviso_versao_fr_atualizacao","aviso_versao_lb_dev","aviso_versao_ms","aviso_versao_btn","aviso_versao_btn_cancela","aviso_versao_btn_atualiza","aviso_versao_fr_atualizada","aviso_versao_lb_dev_atualizada","aviso_versao_ms_atualizada","aviso_bt_cancelar","aviso_versao_bt_facebook_atualizada","aviso_versao_fr_inf_atualizada","aviso_versao_bt_blog_atualizada","bug_lb1_encontrou_bug","bug_lb2_encontrou_bug","bug_lb3_encontrou_bug","bug_fr_bt_encontrou_bug","bug_bt_canc_encontrou_bug","bug_bt_report_encontrou_bug","tutorial_barra_superior","tutorial_tx_tutorial","tutorial_fr_botoes","tutorial_botao_anterior","tutorial_botao_proximo","tutorial_tag_titulo","tutorial_tag_subtitulo","tutorial_tag_subtitulo1","tutorial_tag_subtitulo2","tutorial_tag_texto","tutorial_tag_negrito","tutorial_tag_codigo","inicio_barra_superior","inicio_fr_principal","inicio_fr_botoes_superiores","inicio_frame_botoes","inicio_bt_abrir_programa","inicio_lb_espaco","inicio_lb_espaco2","inicio_frame_cor_tema","inicio_bt_tema","inicio_lb_tema_cores","inicio_fr_opcoes","inicio_fr_recentes","inicio_lb_especial","inicio_fr_especial","inicio_bt_especial"]
for item in lista2:
    if item not in lista:
        print(item)



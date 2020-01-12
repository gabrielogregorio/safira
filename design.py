class design():
    def cor_menu(): 
        return {
            'font':('',12),
            'background':'#494954',
            'foreground':'white',
            'activebackground':'#5a5a65',
            'activeborderwidth':0,
            'tearoff':False, # Separador
            'activeforeground':'white'}

    def lb_sobDeTitulo():
        return {
            'font':("Loma",70,"bold"),
            'height':5,
            'background':'#393944',
            'foreground':'#ffffff'}

    def lb_sobDAutores():
        return {
            'font':("Loma",15),
            'background':'#393944',
            'foreground':'#ffffff'}

    def lb_sobDesenAno():
        return {
            'font':("Loma",10),
            'background':'#393944',
            'foreground':'#ffffff'}

    def tx_codificacao():
        return {
            'bg':'#393944',
            'fg':'#ffffff',
            'highlightthickness':0,
            'insertbackground': '#ffffff',
            'selectbackground':'#494954',
            'selectforeground':'#dddddd',
            'font':('helvetica',12)}

    def lb_linhas():
        return {
            'width':5,
            'bg':'#393944',
            'fg':'#9999bb',
            'font':('helvetica',12)}

    def tx_informacoes():
        return {
            'width':50,
            'bg':'#393944',
            'fg':'#ffffff',
            'highlightthickness':0,
            'font':('helvetica',12)}

class Sintaxe():
    def numerico():
        return {
            'foreground':'#99ffcc'}

    def atribuicao():
        return {
            'foreground':'#aaff80'}

    def loops():
        return {
            'foreground':'#ffcc88'}

    def lista():
        return {
            'foreground':'#aaff80'}

    def logico():
        return {
            'foreground':'#eb99ff'}

    def entrada():
        return {
            'foreground':'#eb99ff'}

    def exibicao():
        return {
            'foreground':'#00e68a'}

    def tempo():
        return {
            'foreground':'#80d4ff'}

    def condicionais():
        return {
            'foreground':'#ffcc88'}


            
    def contas():
        return {
            'foreground':'#eb99ff'}

    def string():
        return {
            'foreground':'#ffff68'}

    def comentario():
        return {
            'foreground':'#616A6B'}         
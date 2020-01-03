class design():
    def cor_menu(): 
        return {
            'font':('',11),
            'background':'#343434',
            'foreground':'white',
            'activebackground':'#464646',
            'activeforeground':'white'}

    def lb_sobDeTitulo():
        return {
            'font':("Loma",70,"bold"),
            'height':5,
            'background':'#343434',
            'foreground':'#ffffff'}

    def lb_sobDAutores():
        return {
            'font':("Loma",15),
            'background':'#343434',
            'foreground':'#ffffff'}

    def lb_sobDesenAno():
        return {
            'font':("Loma",10),
            'background':'#343434',
            'foreground':'#ffffff'}

    def tx_codificacao():
        return {
            'bg':'#343434',
            'fg':'#ffffff',
            'highlightthickness':0,
            'insertbackground': '#ddddff',
            'selectbackground':'#565656',
            'selectforeground':'#343434',
            'font':('helvetica',12)}

    def lb_linhas():
        return {
            'width':5,
            'bg':'#333333',
            'fg':'#888888',
            'font':('helvetica',12)}

    def tx_informacoes():
        return {
            'width':40,
            'bg':'#343434',
            'fg':'#ffffff',
            'font':('',15)}

class Sintaxe():
    def numerico():
        return {
            'foreground':'#ff5de2'}

    def atribuicao():
        return {
            'foreground':'#f57600'}

    def loops():
        return {
            'foreground':'#fe468a'}

    def lista():
        return {
            'foreground':'#fe468a'}

    def logico():
        return {
            'foreground':'#f9264a'}

    def entrada():
        return {
            'foreground':'#f9264a'}

    def exibicao():
        return {
            'foreground':'#43ff69'}

    def tempo():
        return {
            'foreground':'#63f1d8'}

    def condicionais():
        return {
            'foreground':'#e2d872'}
            
    def contas():
        return {
            'foreground':'#f4264a'}

    def string():
        return {
            'foreground':'#F1C40F'}

    def comentario():
        return {
            'foreground':'#616A6B'}         


    def carregar_estilos_terminal(self):

        relief_titulo = self.design.dic["titulo_terminal"]["relief"]

        background_titulo = self.design.dic["titulo_terminal"]["background"]
        foreground_titulo = self.design.dic["titulo_terminal"]["foreground"]

        active_foreground_titulo = self.design.dic["titulo_terminal"]["active_foreground"]
        active_background_titulo = self.design.dic["titulo_terminal"]["active_background"]

        pressed_foreground_titulo = self.design.dic["titulo_terminal"]["pressed_foreground"]
        pressed_background_titulo = self.design.dic["titulo_terminal"]["pressed_background"]

        background_linha = self.design.dic["linha_terminal"]["background"]
        foreground_linha = self.design.dic["linha_terminal"]["foreground"]
        fieldbackground_linha = self.design.dic["linha_terminal"]["fieldbackground"]

        self.style_terminal = Style()
        self.style_terminal.element_create("Custom.Treeheading.border", "from", "default")

        self.style_terminal.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
                    ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
                    ("Custom.Treeheading.text", {'sticky':'we'})
                ]})
            ]}),
        ])


        # Titulo das colunas
        self.style_terminal.configure("Custom.Treeview.Heading",
            background=self.design.dic["titulo_terminal"]["background"],
            foreground=self.design.dic["titulo_terminal"]["foreground"],
            relief=relief_titulo)

        # Linhas 
        self.style_terminal.configure(style="Custom.Treeview",
            background=background_linha,
            foreground=foreground_linha,
            fieldbackground=fieldbackground_linha)
        
        # Mapeamento especial dos titulos
        self.style_terminal.map("Custom.Treeview.Heading",
            relief=[('active', relief_titulo), ('pressed', relief_titulo)],

            foreground=[
                ('pressed', '!disabled', pressed_foreground_titulo),
                ('active', '!disabled', active_foreground_titulo)],
            
            background=[
                ('pressed', '!disabled', pressed_background_titulo),
                ('active', '!disabled', active_background_titulo)]
        )

        return self.style_terminal
import flet as ft

class InicioView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/inicio"

        # AppBar superior
        self.appbar = ft.AppBar(
            leading=ft.Container(
                content=ft.Row([
                    ft.Text("Bienvenido", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START)
            ),
            actions=[
                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    tooltip="Perfil",
                    on_click=self.go_to_perfil,
                    visible=False
                ),
            ],
            toolbar_height=50,
            bgcolor="#FF00FF", # ¡De vuelta al color fucsia hexadecimal!
            elevation=2,
        )

        # Contenido principal de la vista
        self.main_content = ft.Column(
            [
                ft.Text("Contenido de la página de inicio...", size=20, text_align=ft.TextAlign.CENTER),
                ft.Text("Aquí podrías mostrar publicaciones, noticias, etc.", size=16, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

        # NavigationBar para la parte inferior
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    label="Inicio",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON,
                    label="Usuario",
                ),
            ],
            on_change=self.on_nav_bar_change,
            bgcolor="#FF00FF", # ¡De vuelta al color fucsia hexadecimal!
            selected_index=0
        )
        
        self.controls = [
            self.appbar,
            self.main_content,
        ]
        
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.START

    def on_nav_bar_change(self, e):
        if e.control.selected_index == 1:
            if self.page.session.get("user_id"):
                self.page.go("/perfil")
            else:
                self.page.go("/login")
        elif e.control.selected_index == 0:
            self.page.go("/inicio")

    def go_to_login(self, e):
        self.page.go("/login")

    def go_to_perfil(self, e):
        self.page.go("/perfil")

    def did_mount(self):
        self.update_appbar_buttons()
        self.page.navigation_bar = self.navigation_bar
        self.page.update()

    def will_unmount(self):
        self.page.navigation_bar = None
        self.page.update()

    def update_appbar_buttons(self):
        if self.page.session.get("user_id"):
            self.appbar.actions[0].visible = True
        else:
            self.appbar.actions[0].visible = False
        self.page.update()
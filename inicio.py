# inicio.py

import flet as ft

class InicioView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/inicio"

        # Controles para la AppBar superior
        self.login_button_appbar = ft.IconButton(
            icon=ft.Icons.LOGIN,
            tooltip="Iniciar Sesión",
            on_click=self.go_to_login,
            visible=False
        )
        self.register_button_appbar = ft.IconButton(
            icon=ft.Icons.PERSON_ADD,
            tooltip="Registrarse",
            on_click=self.go_to_registro,
            visible=False
        )
        self.profile_button_appbar = ft.IconButton(
            icon=ft.Icons.ACCOUNT_CIRCLE,
            tooltip="Ver Perfil",
            on_click=self.go_to_perfil,
            visible=False
        )
        self.logout_button_appbar = ft.IconButton(
            icon=ft.Icons.LOGOUT,
            tooltip="Cerrar Sesión",
            on_click=self.logout_user,
            visible=False
        )

        self.appbar = ft.AppBar(
            leading=ft.Container(
                content=ft.Row([
                    ft.Text("Bienvenido a CitasZ", size=20, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.START)
            ),
            leading_width=200,
            toolbar_height=70,
            bgcolor=ft.Colors.SURFACE,
            actions=[
                self.profile_button_appbar,
                self.login_button_appbar,
                self.register_button_appbar,
                self.logout_button_appbar,
            ]
        )

        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
            ],
            on_change=self.on_nav_bar_change,
            selected_index=0
        )
        
        self.controls_list = [ # Renombré 'controls' a 'controls_list' para evitar conflicto con la propiedad de View
            ft.Column(
                [
                    ft.Text("Esta es la página de Inicio.", size=20),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]
        
        # Las propiedades route, appbar y navigation_bar se asignan directamente al View
        # No es necesario asignarlas aquí si se pasan directamente en el build()
        # self.route = "/inicio"
        # self.appbar = self.appbar
        # self.navigation_bar = self.navigation_bar


    def update_appbar_buttons(self):
        user_id = self.page.session.get("user_id")
        current_route = self.page.route

        if user_id:
            self.logout_button_appbar.visible = True
            self.login_button_appbar.visible = False
            self.register_button_appbar.visible = False
            
            if current_route == "/perfil":
                self.profile_button_appbar.visible = False
                print("DEBUG: Botón Perfil oculto (ya en /perfil).")
            else:
                self.profile_button_appbar.visible = True
                print("DEBUG: Botón Perfil visible.")
            
            print("DEBUG: Botones de AppBar: Usuario logueado.")
        else:
            self.profile_button_appbar.visible = False
            self.logout_button_appbar.visible = False
            self.login_button_appbar.visible = True
            self.register_button_appbar.visible = True
            print("DEBUG: Botones de AppBar: Usuario NO logueado (Login, Registro visibles).")
        
        # Asegúrate de que el appbar de la página actual se actualice
        # Esto solo tiene sentido si esta instancia de AppBar es la que está en la página.
        # Si tienes AppBars diferentes para cada View, cada View se encargaría de la suya.
        # Para la AppBar global de la página, esto es correcto si se asigna globalmente.
        if self.page.appbar is not None and self.page.appbar == self.appbar:
            self.page.appbar.update()

        self.update_navigation_bar_items()

    def update_navigation_bar_items(self):
        user_id = self.page.session.get("user_id")
        
        self.navigation_bar.destinations.clear()

        self.navigation_bar.destinations.append(
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio")
        )

        if user_id:
            print("DEBUG: Usuario logueado. El icono 'Usuario' en NavigationBar se ocultará.")
        else:
            self.navigation_bar.destinations.append(
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Usuario")
            )
            print("DEBUG: Usuario NO logueado. El icono 'Usuario' en NavigationBar es visible.")

        if self.navigation_bar.selected_index >= len(self.navigation_bar.destinations):
            self.navigation_bar.selected_index = 0

        if self.page.navigation_bar is not None and self.page.navigation_bar == self.navigation_bar:
            self.page.navigation_bar.update()
        else:
            print("DEBUG: NavigationBar no está asignada a la página o no es la misma instancia, no se puede actualizar directamente.")
        
        print(f"DEBUG: NavigationBar actualizada. Destinos actuales: {[d.label for d in self.navigation_bar.destinations]}")


    def on_nav_bar_change(self, e):
        print(f"DEBUG: Navegación inferior cambiada a índice: {e.control.selected_index}")

        current_destinations_labels = [d.label for d in self.navigation_bar.destinations]

        if e.control.selected_index == 0:
            self.page.go("/inicio")
        elif len(current_destinations_labels) > 1 and e.control.selected_index == 1:
            if current_destinations_labels[1] == "Usuario":
                self.page.go("/login")

        self.page.update()


    def logout_user(self, e):
        self.page.session.remove("user_id")
        self.page.client_storage.remove("user_id")
        self.page.snack_bar = ft.SnackBar(ft.Text("Has cerrado sesión."), open=True)
        print("DEBUG: Sesión cerrada, user_id removido.")
        
        self.page.go("/login")
        # No es necesario llamar update_appbar_buttons aquí, route_change en app.py lo hará.
        # self.update_appbar_buttons() # Esta llamada es redundante si page.go lo gatilla
        # self.page.update() # Se llama en route_change


    def go_to_login(self, e):
        self.page.go("/login")

    def go_to_registro(self, e):
        self.page.go("/registro")

    def go_to_perfil(self, e):
        self.page.go("/perfil")

    def build(self):
        # CORREGIDO: Pasar appbar como argumento nombrado y controls_list como argumento posicional
        return ft.View(
            self.route,
            self.controls_list, # Controles del cuerpo de la vista (lista)
            appbar=self.appbar, # AppBar como argumento nombrado
            navigation_bar=self.navigation_bar
        )
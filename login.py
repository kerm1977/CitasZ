import flet as ft
# NUNCA MODIFICAR ft.Colors | ft.Icons

from db import get_user_by_username_or_phone

class LoginView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/login"
        self.appbar = ft.AppBar(title=ft.Text("Iniciar Sesión"), bgcolor="#FF00FF")

        self.username_field = ft.TextField(label="Usuario o Teléfono", hint_text="Ingresa tu usuario o teléfono", width=300)
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )
        self.remember_me_checkbox = ft.Checkbox(label="Recordarme")
        self.message_text = ft.Text("", color=ft.Colors.RED_500)

        self.controls = [
            ft.Column(
                [
                    ft.Text("Bienvenido de nuevo!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Inicia sesión para continuar.", size=16),
                    ft.Container(height=20),
                    self.username_field,
                    self.password_field,
                    self.remember_me_checkbox,
                    ft.ElevatedButton("Iniciar Sesión", on_click=self.login_user),
                    ft.TextButton("¿No tienes cuenta? Regístrate", on_click=self.go_to_registro),
                    ft.TextButton("¿Olvidaste tu contraseña?", on_click=self.recover_password),
                    self.message_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15
            )
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

    def login_user(self, e):
        username_or_phone = self.username_field.value
        password = self.password_field.value

        if not username_or_phone or not password:
            self.message_text.value = "Por favor, ingresa usuario/teléfono y contraseña."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            return

        user = get_user_by_username_or_phone(username_or_phone)

        if user and user["password"] == password:
            self.message_text.value = "¡Inicio de sesión exitoso!"
            self.message_text.color = ft.Colors.GREEN_500
            
            user_id_int = int(user["id"])
            self.page.session.set("user_id", user_id_int)
            print(f"DEBUG: user_id {user_id_int} guardado en session.")

            # --- NUEVO: Lógica para "Recordarme" con client_storage ---
            if self.remember_me_checkbox.value:
                self.page.client_storage.set("user_id", user_id_int)
                print(f"DEBUG: user_id {user_id_int} guardado en client_storage (Recordarme).")
            else:
                # Si no marca "Recordarme", asegúrate de que no haya un user_id persistente anterior
                if self.page.client_storage.contains_key("user_id"):
                    self.page.client_storage.remove("user_id")
                    print("DEBUG: user_id removido de client_storage (No recordar).")
            # ----------------------------------------------------------
            
            self.page.go("/inicio")
        else:
            self.message_text.value = "Usuario o contraseña incorrectos."
            self.message_text.color = ft.Colors.RED_500
        self.page.update()

    def go_to_registro(self, e):
        self.page.go("/registro")

    def recover_password(self, e):
        self.message_text.value = "Funcionalidad de recuperación de contraseña no implementada."
        self.message_text.color = ft.Colors.BLUE_500
        self.page.update()
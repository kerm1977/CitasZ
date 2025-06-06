# recuperar.py
import flet as ft
from db import get_user_by_username_or_email, update_user_password

class RecuperarView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/recuperar"
        self.appbar = ft.AppBar(
            title=ft.Text("Recuperar Contraseña"),
            bgcolor="#FF00FF", # Color consistente con Login/Registro
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.page.go("/login"))
        )

        self.identifier_field = ft.TextField(
            label="Usuario o Correo Electrónico",
            hint_text="Ingresa tu usuario o correo electrónico registrado",
            width=300
        )
        self.message_text = ft.Text("", color=ft.Colors.RED_500)

        self.controls = [
            ft.Column(
                [
                    ft.Text("¿Olvidaste tu contraseña?", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Ingresa tu usuario o correo electrónico para restablecerla.", size=16),
                    ft.Container(height=20),
                    self.identifier_field,
                    ft.ElevatedButton("Restablecer Contraseña", on_click=self.reset_password),
                    self.message_text,
                    ft.TextButton("Volver a Iniciar Sesión", on_click=lambda e: self.page.go("/login")),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        ]

    def reset_password(self, e):
        identifier = self.identifier_field.value
        if not identifier:
            self.message_text.value = "Por favor, ingresa tu usuario o correo electrónico."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            return

        user = get_user_by_username_or_email(identifier)

        if user:
            # En una aplicación real, aquí se generaría un token y se enviaría un email.
            # Para esta simulación, estableceremos una contraseña por defecto (NUNCA HACER ESTO EN PRODUCCIÓN).
            # O simplemente diremos que se "ha enviado" un correo.
            
            # Opción 1: Simular que se ha enviado un correo (más realista para Flet sin backend de correo)
            self.message_text.value = "Si el usuario existe, se ha enviado un enlace de restablecimiento a tu correo electrónico."
            self.message_text.color = ft.Colors.GREEN_500
            print(f"DEBUG: Simulación: Enlace de restablecimiento enviado para {identifier}.")

            # Opción 2 (solo para pruebas extremas y NO segura): Restablecer a una contraseña por defecto
            # new_default_password = "password123" # NUNCA USAR ESTO EN PRODUCCIÓN REAL
            # if update_user_password(user["id"], new_default_password):
            #     self.message_text.value = f"¡Contraseña restablecida! Tu nueva contraseña es '{new_default_password}'. Por favor, cámbiala después de iniciar sesión."
            #     self.message_text.color = ft.Colors.GREEN_500
            #     print(f"DEBUG: Contraseña de {identifier} restablecida a '{new_default_password}'.")
            # else:
            #     self.message_text.value = "Error al restablecer contraseña. Inténtalo de nuevo."
            #     self.message_text.color = ft.Colors.RED_500

            self.page.update()
            # Puedes redirigir a login después de un breve retraso
            # self.page.go("/login")

        else:
            self.message_text.value = "Usuario o correo electrónico no encontrado."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            print(f"DEBUG: Intento de recuperación fallido para {identifier}.")
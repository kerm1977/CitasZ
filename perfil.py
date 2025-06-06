import flet as ft
from db import get_user_by_id, update_user_profile

class PerfilView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/perfil"
        self.appbar = ft.AppBar(
            title=ft.Text("Mi Perfil"),
            bgcolor="#FF00FF", # ¡De vuelta al color fucsia hexadecimal!
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.page.go("/inicio"))
        )

        self.user_data = {}
        self.display_controls = []
        self.edit_controls = []
        self.edit_mode = False

        self.avatar_image = ft.CircleAvatar(radius=50)
        self.username_display = ft.Text(size=20, weight=ft.FontWeight.BOLD)
        self.nombre_display = ft.Text()
        self.apellido1_display = ft.Text()
        self.apellido2_display = ft.Text()
        self.whatsapp_display = ft.Text()
        self.otro_telefono_display = ft.Text()
        self.email_display = ft.Text()
        self.pais_display = ft.Text()
        self.provincia_display = ft.Text()
        self.busco_display = ft.Text()

        # Editable fields
        self.nombre_edit = ft.TextField(label="Nombre Registrado")
        self.apellido1_edit = ft.TextField(label="Apellido 1")
        self.apellido2_edit = ft.TextField(label="Apellido 2")
        self.whatsapp_edit = ft.TextField(label="Teléfono WhatsApp", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9+ ]+$"))
        self.otro_telefono_edit = ft.TextField(label="Otro Teléfono (Opcional)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9+ ]+$"))
        self.email_edit = ft.TextField(label="Correo Electrónico", keyboard_type=ft.KeyboardType.EMAIL)
        self.avatar_url_edit = ft.TextField(label="URL de Avatar")

        self.country_edit = ft.Dropdown(
            label="País",
            options=[
                ft.dropdown.Option("Costa Rica"),
                ft.dropdown.Option("Nicaragua"),
                ft.dropdown.Option("Panamá"),
            ],
            on_change=self.update_provincia_options_edit
        )

        self.provincia_edit = ft.Dropdown(label="Provincia")
        
        self.busco_options_edit = [
            "Amiga con Derecho", "Amiga Bisexual", "Amiga Lesbiana", "Curiosa", "Novia",
            "Chat Erótico", "Video llamada", "Masajista", "Acompañante", "Aventurera",
            "Solo una Amiga", "Otra"
        ]
        self.busco_checkboxes_edit = []
        for option in self.busco_options_edit:
            self.busco_checkboxes_edit.append(ft.Checkbox(label=option, value=False))

        self.edit_button = ft.ElevatedButton("Editar Perfil", on_click=self.toggle_edit_mode)
        self.save_button = ft.ElevatedButton("Guardar Cambios", on_click=self.save_profile, visible=False)
        self.cancel_button = ft.ElevatedButton("Cancelar", on_click=self.toggle_edit_mode, visible=False)
        self.message_text = ft.Text("", color=ft.Colors.RED_500)

        self.controls = [
            ft.Column(
                [
                    self.avatar_image,
                    self.username_display,
                    ft.Divider(),
                    ft.Column(self.display_controls),
                    ft.Column(self.edit_controls),
                    ft.Row([self.edit_button, self.save_button, self.cancel_button], alignment=ft.MainAxisAlignment.CENTER),
                    self.message_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                scroll=ft.ScrollMode.ADAPTIVE
            )
        ]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.START

    def did_mount(self):
        self.load_user_data()

    def load_user_data(self):
        user_id = self.page.session.get("user_id")
        if user_id:
            user = get_user_by_id(user_id)
            if user:
                self.user_data = dict(user)
                self.populate_display_fields()
                self.populate_edit_fields()
                self.update_content_visibility()
                self.page.update()
            else:
                self.message_text.value = "Error: Usuario no encontrado."
                self.page.update()
        else:
            self.message_text.value = "Debes iniciar sesión para ver tu perfil."
            self.page.go("/login")

    def populate_display_fields(self):
        user_data = self.user_data
        self.avatar_image.content = ft.Image(src=user_data.get("avatar_url")) if user_data.get("avatar_url") else ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=100)
        self.username_display.value = user_data.get("username", "N/A")
        self.nombre_display.value = f"Nombre: {user_data.get('nombre_registrado', 'N/A')}"
        self.apellido1_display.value = f"Apellido 1: {user_data.get('apellido1', 'N/A')}"
        self.apellido2_display.value = f"Apellido 2: {user_data.get('apellido2', 'N/A')}"
        self.whatsapp_display.value = f"WhatsApp: {user_data.get('telefono_whatsapp', 'N/A')}"
        self.otro_telefono_display.value = f"Otro Teléfono: {user_data.get('otro_telefono', 'N/A')}"
        self.email_display.value = f"Correo: {user_data.get('correo_electronico', 'N/A')}"
        self.pais_display.value = f"País: {user_data.get('pais', 'N/A')}"
        self.provincia_display.value = f"Provincia: {user_data.get('provincia', 'N/A')}"
        self.busco_display.value = f"Busco: {user_data.get('busco', 'N/A')}"

        self.display_controls[:] = [
            self.nombre_display, self.apellido1_display, self.apellido2_display,
            self.whatsapp_display, self.otro_telefono_display, self.email_display,
            self.pais_display, self.provincia_display, self.busco_display
        ]

    def populate_edit_fields(self):
        user_data = self.user_data
        self.nombre_edit.value = user_data.get("nombre_registrado", "")
        self.apellido1_edit.value = user_data.get("apellido1", "")
        self.apellido2_edit.value = user_data.get("apellido2", "")
        self.whatsapp_edit.value = user_data.get("telefono_whatsapp", "")
        self.otro_telefono_edit.value = user_data.get("otro_telefono", "")
        self.email_edit.value = user_data.get("correo_electronico", "")
        self.avatar_url_edit.value = user_data.get("avatar_url", "")
        
        self.country_edit.value = user_data.get("pais")
        self.update_provincia_options_edit()
        self.provincia_edit.value = user_data.get("provincia")

        busco_values = user_data.get("busco", "").split(", ")
        for cb in self.busco_checkboxes_edit:
            cb.value = cb.label in busco_values

        self.edit_controls[:] = [
            self.nombre_edit, self.apellido1_edit, self.apellido2_edit,
            self.whatsapp_edit, self.otro_telefono_edit, self.email_edit,
            self.avatar_url_edit,
            self.country_edit, self.provincia_edit,
            ft.Text("¿Qué buscas?", size=16, weight=ft.FontWeight.BOLD),
            ft.Column(self.busco_checkboxes_edit)
        ]

    def update_provincia_options_edit(self, e=None):
        selected_country = self.country_edit.value
        provincias = []
        if selected_country == "Costa Rica":
            provincias = ["Alajuela", "Cartago", "Heredia", "Puntarenas", "Guanacaste", "Limón", "San José"]
        elif selected_country == "Nicaragua":
            provincias = ["Boaco", "Carazo", "Chinandega", "Chontales", "Estelí", "Granada", "Jinotega", "León", "Madriz", "Managua", "Masaya", "Matagalpa", "Nueva Segovia", "Rivas", "Río San Juan"]
        elif selected_country == "Panamá":
            provincias = ["Panamá", "Colón", "Darién", "Bocas del Toro", "Veraguas", "Herrera", "Los Santos", "Coclé", "Chiriquí", "Panamá Oeste"]
        
        self.provincia_edit.options = [ft.dropdown.Option(p) for p in provincias]
        if len(provincias) > 0 and self.provincia_edit.value not in provincias:
            self.provincia_edit.value = None
        self.page.update()

    def toggle_edit_mode(self, e):
        self.edit_mode = not self.edit_mode
        self.update_content_visibility()
        self.page.update()

    def update_content_visibility(self):
        for control in self.display_controls:
            control.visible = not self.edit_mode
        for control in self.edit_controls:
            control.visible = self.edit_mode
        
        self.edit_button.visible = not self.edit_mode
        self.save_button.visible = self.edit_mode
        self.cancel_button.visible = self.edit_mode

    def save_profile(self, e):
        user_id = self.page.session.get("user_id")
        if not user_id:
            self.message_text.value = "No hay usuario logueado para guardar."
            self.page.update()
            return

        updates = {
            "nombre_registrado": self.nombre_edit.value,
            "apellido1": self.apellido1_edit.value,
            "apellido2": self.apellido2_edit.value,
            "telefono_whatsapp": self.whatsapp_edit.value,
            "otro_telefono": self.otro_telefono_edit.value,
            "correo_electronico": self.email_edit.value,
            "avatar_url": self.avatar_url_edit.value,
            "pais": self.country_edit.value,
            "provincia": self.provincia_edit.value,
            "busco": ", ".join([cb.label for cb in self.busco_checkboxes_edit if cb.value])
        }

        if update_user_profile(user_id, **updates):
            self.message_text.value = "Perfil actualizado exitosamente."
            self.message_text.color = ft.Colors.GREEN_500
            self.load_user_data()
            self.toggle_edit_mode(None)
        else:
            self.message_text.value = "Error al actualizar el perfil."
            self.message_text.color = ft.Colors.RED_500
        self.page.update()
# perfil.py
import flet as ft
from db import get_user_by_id, update_user_profile

class PerfilView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/perfil"
        self.appbar = ft.AppBar(
            title=ft.Text("Mi Perfil"),
            bgcolor="#FF00FF",
            leading=ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.page.go("/inicio"))
        )

        self.user_data = {}
        self.edit_mode = False

        self.avatar_image = ft.CircleAvatar(radius=50)
        self.username_display = ft.Text(size=20, weight=ft.FontWeight.BOLD)
        
        # Controles de VISUALIZACIÓN
        self.nombre_display = ft.Text()
        self.apellido1_display = ft.Text()
        self.apellido2_display = ft.Text()
        self.whatsapp_display = ft.Text()
        self.otro_telefono_display = ft.Text()
        self.email_display = ft.Text()
        self.pais_display = ft.Text()
        self.provincia_display = ft.Text()
        self.busco_display = ft.Text()

        # Controles de EDICIÓN
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

        # Contenedores para las listas de controles (modo display y edit)
        # Esto nos permite actualizar directamente los .controls de estas columnas
        self.display_column_container = ft.Column([], visible=not self.edit_mode, expand=True)
        self.edit_column_container = ft.Column([], visible=self.edit_mode, expand=True)

        self.content_column = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            self.avatar_image,
                            self.username_display,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=20, bottom=10)
                ),
                ft.Divider(),
                self.display_column_container, # Referencia directa a la columna contenedora
                self.edit_column_container,   # Referencia directa a la columna contenedora
                ft.Row([self.edit_button, self.save_button, self.cancel_button], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                self.message_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )
        
        self.controls = [self.content_column]
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.START

    def did_mount(self):
        print(f"DEBUG: did_mount() de PerfilView llamado. Cargando datos de usuario...")
        self.load_user_data()

    def load_user_data(self):
        user_id = self.page.session.get("user_id")
        print(f"DEBUG: load_user_data() - user_id de sesión: {user_id}")
        
        if user_id is None:
            self.message_text.value = "Debes iniciar sesión para ver tu perfil."
            self.message_text.color = ft.Colors.BLUE_500
            self.page.update()
            print("DEBUG: No hay user_id en sesión para PerfilView, redirigiendo a /login.")
            self.page.go("/login")
            return

        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            self.message_text.value = "Error: ID de usuario inválido en sesión."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            print(f"DEBUG: ID de usuario inválido en sesión: {user_id}")
            self.page.go("/login")
            return

        user = get_user_by_id(user_id_int)

        if user:
            self.user_data = dict(user)
            self.populate_display_fields()
            self.populate_edit_fields()
            self.update_content_visibility()
            print("DEBUG: Datos de usuario cargados y UI actualizada.")
        else:
            self.message_text.value = "Error: Usuario no encontrado en la base de datos."
            self.message_text.color = ft.Colors.RED_500
            print(f"DEBUG: Usuario no encontrado en DB para ID {user_id_int}.")
            self.page.session.set("user_id", None) 
            self.page.go("/login") 
        
        self.page.update()

    def populate_display_fields(self):
        user_data = self.user_data
        # Actualiza los valores de los controles
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

        # Asigna los controles directamente a la lista .controls de la columna contenedora
        self.display_column_container.controls = [
            self.nombre_display, self.apellido1_display, self.apellido2_display,
            self.whatsapp_display, self.otro_telefono_display, self.email_display,
            self.pais_display, self.provincia_display, self.busco_display
        ]
        print("DEBUG: populate_display_fields ejecutado.")


    def populate_edit_fields(self):
        user_data = self.user_data
        # Actualiza los valores de los campos de edición
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

        # Asigna los controles directamente a la lista .controls de la columna contenedora
        self.edit_column_container.controls = [
            self.nombre_edit, self.apellido1_edit, self.apellido2_edit,
            self.whatsapp_edit, self.otro_telefono_edit, self.email_edit,
            self.avatar_url_edit,
            self.country_edit, self.provincia_edit,
            ft.Text("¿Qué buscas?", size=16, weight=ft.FontWeight.BOLD),
            ft.Row(self.busco_checkboxes_edit, wrap=True, spacing=10, run_spacing=5)
        ]
        print("DEBUG: populate_edit_fields ejecutado.")

    def update_provincia_options_edit(self, e=None):
        selected_country = self.country_edit.value
        provincias = []
        if selected_country == "Costa Rica":
            provincias = ["Alajuela", "Cartago", "Heredia", "Puntarenas", "Guanacaste", "Limón", "San José"]
        elif selected_country == "Nicaragua":
            provincias = ["Boaco", "Carazo", "Chinandega", "Chontales", "Estelí", "Granada", "Jinotega", "León", "Madriz", "Managua", "Masaya", "Matagalpa", "Nueva Segovia", "Rivas", "Río San Juan"]
        elif selected_country == "Panamá":
            provincias = ["Panamá", "Colón", "Darién", "Bocas del Toro", "Veraguas", "Herrera", "Los Santos", "Coclé", "Chiriquí", "Panamá Oeste"]
        
        current_provincia_value = self.provincia_edit.value

        self.provincia_edit.options = [ft.dropdown.Option(p) for p in provincias]
        
        if current_provincia_value in provincias:
            self.provincia_edit.value = current_provincia_value
        elif provincias:
            self.provincia_edit.value = provincias[0]
        else:
            self.provincia_edit.value = None
        
        if e:
            self.page.update()
        print("DEBUG: update_provincia_options_edit ejecutado.")

    def toggle_edit_mode(self, e):
        self.edit_mode = not self.edit_mode
        self.update_content_visibility()
        self.page.update()
        print(f"DEBUG: Modo de edición: {self.edit_mode}")

    def update_content_visibility(self):
        # Ahora referenciamos directamente los contenedores de columnas
        self.display_column_container.visible = not self.edit_mode
        self.edit_column_container.visible = self.edit_mode
        
        self.edit_button.visible = not self.edit_mode
        self.save_button.visible = self.edit_mode
        self.cancel_button.visible = self.edit_mode
        print("DEBUG: Visibilidad de contenido actualizada.")

    def save_profile(self, e):
        user_id = self.page.session.get("user_id")
        print(f"DEBUG: Guardando perfil para user_id: {user_id}")
        if not user_id:
            self.message_text.value = "No hay usuario logueado para guardar."
            self.message_text.color = ft.Colors.RED_500
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

        try:
            user_id_int = int(user_id)
        except (ValueError, TypeError):
            self.message_text.value = "Error: ID de usuario inválido al guardar."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            print(f"DEBUG: ID de usuario inválido al guardar: {user_id}")
            return


        if update_user_profile(user_id_int, **updates):
            self.message_text.value = "Perfil actualizado exitosamente."
            self.message_text.color = ft.Colors.GREEN_500
            self.load_user_data()
            print("DEBUG: Perfil guardado, recargando datos.")
        else:
            self.message_text.value = "Error al actualizar el perfil."
            self.message_text.color = ft.Colors.RED_500
            print("DEBUG: Error al guardar perfil.")
        self.page.update()
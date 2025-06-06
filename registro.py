import flet as ft
from db import create_user

class RegistroView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/registro"
        self.appbar = ft.AppBar(title=ft.Text("Registrarse"), bgcolor="#FF00FF")

        self.username_field = ft.TextField(label="Usuario", hint_text="Define tu nombre de usuario", width=300)
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )
        self.nombre_field = ft.TextField(label="Nombre Registrado", width=300)
        self.apellido1_field = ft.TextField(label="Apellido 1", width=300)
        self.apellido2_field = ft.TextField(label="Apellido 2", width=300)
        self.whatsapp_field = ft.TextField(label="Teléfono WhatsApp", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9+ ]+$"), width=300)
        self.otro_telefono_field = ft.TextField(label="Otro Teléfono (Opcional)", input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9+ ]+$"), width=300)
        self.email_field = ft.TextField(label="Correo Electrónico", keyboard_type=ft.KeyboardType.EMAIL, width=300)
        self.avatar_url_field = ft.TextField(label="URL de Avatar (Opcional)", width=300)

        self.country_dropdown = ft.Dropdown(
            label="País",
            options=[
                ft.dropdown.Option("Costa Rica"),
                ft.dropdown.Option("Nicaragua"),
                ft.dropdown.Option("Panamá"),
            ],
            width=300,
            on_change=self.update_provincia_options
        )

        self.provincia_dropdown = ft.Dropdown(
            label="Provincia",
            width=300,
            # Aseguramos que la provincia se establezca correctamente al inicio
            on_focus=lambda e: self.update_provincia_options(e) # Forzar una actualización al enfocar
        )
        # Llama a update_provincia_options al inicio para poblar las opciones iniciales
        # Y también para establecer un valor por defecto si es posible
        self.update_provincia_options() 

        self.busco_options_list = [ # Renombrado para evitar conflicto con el control
            "Amiga con Derecho", "Amiga Bisexual", "Amiga Lesbiana", "Curiosa", "Novia",
            "Chat Erótico", "Video llamada", "Masajista", "Acompañante", "Aventurera",
            "Solo una Amiga", "Otra"
        ]
        self.busco_checkboxes = []
        for option in self.busco_options_list:
            self.busco_checkboxes.append(ft.Checkbox(label=option, value=False))

        # Contenedor para los checkboxes de "Busco" para asegurar el wrap y el espacio
        self.busco_checkbox_container = ft.Container(
            content=ft.Row(
                self.busco_checkboxes,
                wrap=True,
                spacing=10,
                run_spacing=5,
                alignment=ft.MainAxisAlignment.START, # Asegura que empiecen desde la izquierda
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            width=350, # Puedes ajustar este ancho si es necesario para el wrap
            # bgcolor=ft.Colors.YELLOW_100, # Para depuración: ver los límites del contenedor
        )

        self.message_text = ft.Text("", color=ft.Colors.RED_500)

        # Contenedor principal de la vista de registro
        self.main_content_column = ft.Column(
            [
                ft.Text("Crea tu cuenta", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Completa los datos para registrarte.", size=16),
                ft.Container(height=20),
                self.username_field,
                self.password_field,
                self.nombre_field,
                self.apellido1_field,
                self.apellido2_field,
                self.whatsapp_field,
                self.otro_telefono_field,
                self.email_field,
                self.avatar_url_field,
                self.country_dropdown,
                self.provincia_dropdown,
                ft.Text("¿Qué buscas?", size=16, weight=ft.FontWeight.BOLD),
                self.busco_checkbox_container, # Ahora usamos el contenedor
                ft.ElevatedButton("Registrarse", on_click=self.register_user),
                ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=self.go_to_login),
                self.message_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START, # Alineación del contenido de la columna al inicio (superior)
            spacing=10,
            scroll=ft.ScrollMode.ADAPTIVE, # Permite scroll si el contenido excede la altura
            expand=True # Permite que la columna se expanda y llene el espacio vertical disponible
            # bgcolor=ft.Colors.BLUE_50, # Para depuración: ver los límites de la columna principal
        )
        
        self.controls = [self.main_content_column] # La vista solo tiene esta columna como control principal
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.START # Alineación de la vista al inicio (superior)

    def update_provincia_options(self, e=None):
        selected_country = self.country_dropdown.value
        provincias = []
        if selected_country == "Costa Rica":
            provincias = ["Alajuela", "Cartago", "Heredia", "Puntarenas", "Guanacaste", "Limón", "San José"]
        elif selected_country == "Nicaragua":
            provincias = ["Boaco", "Carazo", "Chinandega", "Chontales", "Estelí", "Granada", "Jinotega", "León", "Madriz", "Managua", "Masaya", "Matagalpa", "Nueva Segovia", "Rivas", "Río San Juan"]
        elif selected_country == "Panamá":
            provincias = ["Panamá", "Colón", "Darién", "Bocas del Toro", "Veraguas", "Herrera", "Los Santos", "Coclé", "Chiriquí", "Panamá Oeste"]
        
        # Guardar el valor actual del dropdown antes de actualizar las opciones
        current_provincia_value = self.provincia_dropdown.value

        # Convertir cada provincia a un objeto ft.dropdown.Option
        self.provincia_dropdown.options = [ft.dropdown.Option(p) for p in provincias]
        
        # Intentar restaurar el valor si aún es válido, de lo contrario, establecer el primero o None
        if current_provincia_value in provincias:
            self.provincia_dropdown.value = current_provincia_value
        elif provincias: # Si hay nuevas opciones, seleccionar la primera por defecto
            self.provincia_dropdown.value = provincias[0]
        else: # Si no hay opciones, limpiar el valor
            self.provincia_dropdown.value = None
        
        # Asegúrate de actualizar la página para que los cambios se reflejen en la UI
        # Esto es crucial para que el dropdown se redibuje con las nuevas opciones
        # y su valor.
        self.page.update()

    def register_user(self, e):
        username = self.username_field.value
        password = self.password_field.value
        nombre_registrado = self.nombre_field.value
        apellido1 = self.apellido1_field.value
        apellido2 = self.apellido2_field.value
        telefono_whatsapp = self.whatsapp_field.value
        otro_telefono = self.otro_telefono_field.value
        correo_electronico = self.email_field.value
        avatar_url = self.avatar_url_field.value
        pais = self.country_dropdown.value
        provincia = self.provincia_dropdown.value
        busco_selected = [cb.label for cb in self.busco_checkboxes if cb.value]
        busco_str = ", ".join(busco_selected)

        if not (username and password and nombre_registrado and apellido1 and correo_electronico and telefono_whatsapp):
            self.message_text.value = "Por favor, completa todos los campos obligatorios (Usuario, Contraseña, Nombre, Apellido 1, Correo, WhatsApp)."
            self.message_text.color = ft.Colors.RED_500
            self.page.update()
            return

        if create_user(username, password, nombre_registrado, apellido1, apellido2,
                       telefono_whatsapp, otro_telefono, correo_electronico,
                       avatar_url, pais, provincia, busco_str):
            self.message_text.value = "¡Registro exitoso! Ahora puedes iniciar sesión."
            self.message_text.color = ft.Colors.GREEN_500
            self.page.go("/login")
        else:
            self.message_text.value = "Error al registrar usuario. El usuario o correo electrónico ya existen."
            self.message_text.color = ft.Colors.RED_500
        self.page.update()

    def go_to_login(self, e):
        self.page.go("/login")
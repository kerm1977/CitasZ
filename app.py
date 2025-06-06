# app.py

import flet as ft
from inicio import InicioView
from login import LoginView
from registro import RegistroView
from perfil import PerfilView
from recuperar import RecuperarView # Importar RecuperarView
from db import init_db

def main(page: ft.Page):
    page.title = "App Flet con DB"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    init_db()

    stored_user_id = page.client_storage.get("user_id")
    if stored_user_id is not None:
        page.session.set("user_id", stored_user_id)
        print(f"DEBUG: user_id cargado desde client_storage: {stored_user_id}")
    else:
        print("DEBUG: No hay user_id almacenado en client_storage.")

    # Instanciar todas las vistas una única vez al inicio
    login_view_instance = LoginView(page)
    registro_view_instance = RegistroView(page)
    inicio_view_instance = InicioView(page)
    recuperar_view_instance = RecuperarView(page)

    def route_change(e: ft.RouteChangeEvent):
        print(f"DEBUG: Navegando a la ruta: {page.route}")
        page.views.clear() # ¡Importante! Limpiar todas las vistas antes de añadir la nueva

        user_id_in_session = page.session.get("user_id")

        # Configuración de la barra de navegación inferior (NavigationBar)
        if user_id_in_session:
            page.navigation_bar = inicio_view_instance.navigation_bar
            print("DEBUG: NavigationBar activada (usuario logueado).")
        else:
            page.navigation_bar = None
            print("DEBUG: NavigationBar desactivada (usuario no logueado).")
        
        # Lógica para añadir la vista correcta a la pila de vistas
        if page.route == "/login":
            page.views.append(login_view_instance)
        elif page.route == "/registro":
            # Cuando navegamos a registro, aseguramos que la AppBar tenga el botón de retroceso
            registro_view_instance.appbar.leading = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/login")
            )
            page.views.append(registro_view_instance)
        elif page.route == "/perfil":
            if user_id_in_session is None:
                print("DEBUG: No hay user_id en sesión, redirigiendo a /login.")
                page.go("/login")
                return
            else:
                perfil_view_instance = PerfilView(page) # Recargar perfil para datos actualizados
                page.views.append(perfil_view_instance)
        elif page.route == "/recuperar":
            # Cuando navegamos a recuperar, aseguramos que la AppBar tenga el botón de retroceso
            recuperar_view_instance.appbar.leading = ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: page.go("/login")
            )
            page.views.append(recuperar_view_instance)
        elif page.route == "/inicio" or page.route == "/":
            page.views.append(inicio_view_instance)
        else:
            # Si la ruta no coincide con ninguna, redirigir a inicio por defecto
            page.go("/inicio")
            return

        # Solo llamar a update_appbar_buttons si la vista actual es InicioView
        if isinstance(page.views[-1], InicioView):
             inicio_view_instance.update_appbar_buttons()
        
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        print(f"DEBUG: Popping view: {e.view.route}")
        
        page.views.pop() # Elimina la vista actual de la pila
        if page.views: # Asegúrate de que hay una vista anterior
            top_view = page.views[-1]
            page.go(top_view.route) # Navega a la ruta de la vista anterior
            
            # Si al hacer pop, la vista superior es InicioView, actualiza sus botones
            if isinstance(top_view, InicioView):
                top_view.update_appbar_buttons()
        else:
            # Si no hay más vistas en la pila (por ejemplo, al cerrar la última vista)
            # puedes redirigir a una ruta predeterminada
            page.go("/inicio")
            
        page.update() # Asegurarse de que la página se actualice después del pop

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Asegura que la ruta inicial se procese correctamente al inicio de la aplicación
    page.go(page.route) 

ft.app(target=main)
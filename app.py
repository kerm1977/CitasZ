# app.py

import flet as ft
from inicio import InicioView
from login import LoginView
from registro import RegistroView
from perfil import PerfilView
from db import init_db

def main(page: ft.Page):
    page.title = "App Flet con DB"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    init_db()

    # --- NUEVO: Cargar user_id de client_storage al inicio ---
    stored_user_id = page.client_storage.get("user_id")
    if stored_user_id is not None:
        page.session.set("user_id", stored_user_id)
        print(f"DEBUG: user_id cargado desde client_storage: {stored_user_id}")
    else:
        print("DEBUG: No hay user_id almacenado en client_storage.")
    # --------------------------------------------------------

    login_view_instance = LoginView(page)
    registro_view_instance = RegistroView(page)
    inicio_view_instance = InicioView(page)

    def route_change(e: ft.RouteChangeEvent):
        print(f"DEBUG: Navegando a la ruta: {page.route}")
        page.views.clear()
        
        # --- MOVIMIENTO CLAVE: ASIGNAR page.navigation_bar AQUÍ ---
        # Si el usuario está logueado, se asigna la NavigationBar.
        # Si no, se asigna None, pero esto se hace antes de que update_appbar_buttons se llame.
        user_id_in_session = page.session.get("user_id")
        if user_id_in_session:
            page.navigation_bar = inicio_view_instance.navigation_bar
            print("DEBUG: NavigationBar activada (usuario logueado).")
        else:
            page.navigation_bar = None # Ocultar la NavigationBar si no está logueado
            print("DEBUG: NavigationBar desactivada (usuario no logueado).")

        page.views.append(inicio_view_instance)

        if page.route == "/login":
            page.views.append(login_view_instance)
        elif page.route == "/registro":
            page.views.append(registro_view_instance)
        elif page.route == "/perfil":
            user_id_in_session = page.session.get("user_id")
            print(f"DEBUG: Intentando acceder a /perfil. user_id en sesión: {user_id_in_session}")
            if user_id_in_session is None:
                print("DEBUG: No hay user_id en sesión, redirigiendo a /login.")
                page.go("/login")
                return
            else:
                perfil_view_instance = PerfilView(page)
                page.views.append(perfil_view_instance)
                # Seleccionar el ítem de usuario en la nav bar si se navega a perfil
                # Ten cuidado con el selected_index si la nav bar es dinámica.
                # Si 'Usuario' se oculta logueado, el índice 1 no existirá para Perfil.
                # Es mejor no establecerlo aquí si estás ocultando dinámicamente.
                # inicio_view_instance.navigation_bar.selected_index = 1 
        
        # Siempre llamar a update_appbar_buttons para reflejar el estado de login en la AppBar de Inicio
        # y para actualizar la NavigationBar después de que se ha asignado a page.navigation_bar
        inicio_view_instance.update_appbar_buttons() 
        page.update()

    def view_pop(e: ft.ViewPopEvent):
        popped_view = e.view 
        print(f"DEBUG: Popping view: {popped_view.route}")
        
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
        if isinstance(top_view, InicioView):
            top_view.update_appbar_buttons() # Asegúrate de actualizar los botones al volver a Inicio

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

ft.app(target=main, port=8550) # Añadido view y port para probar en navegador
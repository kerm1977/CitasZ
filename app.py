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

    # --- CAMBIO IMPORTANTE AQUÍ (aunque ya estaba en tu código anterior) ---
    # Asegúrate de que page.session esté disponible antes de que se use en las vistas
    # Flet lo inicializa automáticamente, pero es bueno saber que existe.
    # No necesitas añadir nada aquí explícitamente para page.session
    # ---------------------------------------------------------------------

    init_db()

    login_view_instance = LoginView(page)
    registro_view_instance = RegistroView(page)
    inicio_view_instance = InicioView(page)

    def route_change(route):
        print(f"DEBUG: Navegando a la ruta: {page.route}")
        page.views.clear()
        
        page.views.append(inicio_view_instance)
        page.navigation_bar = inicio_view_instance.navigation_bar

        if page.route == "/login":
            page.views.append(login_view_instance)
            inicio_view_instance.navigation_bar.selected_index = None
        elif page.route == "/registro":
            page.views.append(registro_view_instance)
            inicio_view_instance.navigation_bar.selected_index = None
        elif page.route == "/perfil":
            user_id_in_session = page.session.get("user_id")
            print(f"DEBUG: Intentando acceder a /perfil. user_id en sesión: {user_id_in_session}")
            if user_id_in_session is None: # Si no hay user_id, redirigir
                print("DEBUG: No hay user_id en sesión, redirigiendo a /login.")
                page.go("/login")
                return
            else:
                perfil_view_instance = PerfilView(page) # Nueva instancia para asegurar did_mount
                page.views.append(perfil_view_instance)
                inicio_view_instance.navigation_bar.selected_index = 1 
        
        inicio_view_instance.update_appbar_buttons() 
        page.update()

    def view_pop(view):
        print(f"DEBUG: Popping view: {view.route}")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
        if isinstance(top_view, InicioView):
            top_view.update_appbar_buttons()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/inicio")

if __name__ == "__main__":
    ft.app(target=main)
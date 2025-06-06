import flet as ft
from inicio import InicioView
from login import LoginView
from registro import RegistroView
from perfil import PerfilView
from db import init_db

def main(page: ft.Page):
    page.title = "App Flet con DB"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Mantener para el contenido de las vistas

    init_db()

    # Define la NavigationBar una vez aquí, si quieres que sea global en todas las vistas
    # O déjala dentro de InicioView y manéjala con page.navigation_bar en did_mount/will_unmount
    # Para este ejemplo, la dejo en InicioView y uso page.navigation_bar allí.

    def route_change(route):
        page.views.clear()
        
        # Crear la vista de inicio
        inicio_view = InicioView(page)
        page.views.append(inicio_view)

        # Configurar la NavigationBar para la página
        # La NavigationBar se gestiona en la vista de inicio, pero se asigna a page.navigation_bar
        # para que Flet la posicione correctamente.
        if page.route == "/login":
            page.views.append(LoginView(page))
            # Deseleccionar el destino de usuario en la nav bar si estamos en login
            if inicio_view.navigation_bar.selected_index != -1: # No está en inicio
                inicio_view.navigation_bar.selected_index = None # Deseleccionar todo si no es inicio/perfil
        elif page.route == "/registro":
            page.views.append(RegistroView(page))
            if inicio_view.navigation_bar.selected_index != -1:
                inicio_view.navigation_bar.selected_index = None
        elif page.route == "/perfil":
            if not page.session.get("user_id"):
                page.go("/login")
                return
            page.views.append(PerfilView(page))
            # Seleccionar el destino de usuario en la nav bar si estamos en perfil
            # Esto puede ser un poco más complicado si no hay un destino directo de "perfil"
            # Si el botón de "Usuario" lleva a login/registro/perfil, podemos mantenerlo seleccionado.
            inicio_view.navigation_bar.selected_index = 1 # Asume que el botón de usuario/perfil está en el índice 1

        # Asegurarse de que el page.navigation_bar esté configurado
        # Cada vista es responsable de su propio NavigationBar si no es global
        # En este caso, InicioView lo gestiona.
        page.navigation_bar = inicio_view.navigation_bar # Asegura que la nav bar de inicio siempre esté presente

        # Actualiza el estado del AppBar de la vista de inicio (si aplica)
        inicio_view.update_appbar_buttons()

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        
        # Asegúrate de que al volver, el appbar de inicio se actualice si es necesario
        if isinstance(top_view, InicioView):
            top_view.update_appbar_buttons()


    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/inicio")

if __name__ == "__main__":
    ft.app(target=main)
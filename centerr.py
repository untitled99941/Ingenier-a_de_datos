from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px 
import psycopg2 
import dash_bootstrap_components as dbc
from PIL import Image

# Conexión a la base de datos PostgreSQL
try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='123456789',
        database='proyec_vuelos',
        port='5433',
    )

    print("Conexión exitosa")
    cursor = connection.cursor()

    pil_image=Image.open("C:/Users/Public/proyecto_vuelos/logo.jpg")

    # Consultas a la base de datos y creación de DataFrames
    consulta1 = "select empresa.nombre_empresa, avg(vuelo.carga)::numeric(10,0) as tendencia_carga,rank() over (order by (avg(vuelo.carga)::numeric(10,0)) DESC) as Ranking_tendencias_R from empresa join vuelo on empresa.id_empresa=vuelo.id_empresa where vuelo.t_vuelo='R' group by empresa.nombre_empresa,vuelo.t_vuelo order by tendencia_carga DESC;"
    cursor.execute(consulta1)
    rows_empres_p = cursor.fetchall()
    df_empres_p = pd.DataFrame(rows_empres_p, columns=['nombre_empresa', 'tendencia_carga', 'Ranking_tendencias_R'])

    consulta2 = "select empresa.nombre_empresa, avg(vuelo.carga)::numeric(10,0) as tendencia_carga,rank() over (order by (avg(vuelo.carga)::numeric(10,0)) DESC) as Ranking_tendencias_T from empresa join vuelo on empresa.id_empresa=vuelo.id_empresa where vuelo.t_vuelo='T' group by empresa.nombre_empresa,vuelo.t_vuelo order by tendencia_carga DESC;"
    cursor.execute(consulta2)
    rows_empres_m = cursor.fetchall()
    df_empres_m = pd.DataFrame(rows_empres_m, columns=['nombre_empresa', 'tendencia_carga', 'Ranking_tendencias_T'])

    consulta3 = "select empresa.nombre_empresa, avg(vuelo.carga)::numeric(10,0) as tendencia_carga,rank() over (order by (avg(vuelo.carga)::numeric(10,0)) DESC) as Ranking_tendencias_C from empresa join vuelo on empresa.id_empresa=vuelo.id_empresa where vuelo.t_vuelo='C' group by empresa.nombre_empresa,vuelo.t_vuelo order by tendencia_carga DESC;"
    cursor.execute(consulta3)
    rows_empres_n = cursor.fetchall()
    df_empres_n = pd.DataFrame(rows_empres_n, columns=['nombre_empresa', 'tendencia_carga', 'Ranking_tendencias_C'])

    consulta4 = "select empresa.nombre_empresa, avg(vuelo.carga)::numeric(10,0) as tendencia_carga,rank() over (order by (avg(vuelo.carga)::numeric(10,0)) DESC) as Ranking_tendencias_A from empresa join vuelo on empresa.id_empresa=vuelo.id_empresa where vuelo.t_vuelo='A' group by empresa.nombre_empresa,vuelo.t_vuelo order by tendencia_carga DESC;"
    cursor.execute(consulta4)
    rows_empres_s = cursor.fetchall()
    df_empres_s = pd.DataFrame(rows_empres_s, columns=['nombre_empresa', 'tendencia_carga', 'Ranking_tendencias_A'])

    consulta5 = "select t_vuelo, count(t_vuelo) as cantidad_de_vuelos,rank () over (order by (count(t_vuelo)) desc) as Ranking_tipo_de_vuelo from vuelo group by t_vuelo order by cantidad_de_vuelos DESC;"
    cursor.execute(consulta5)
    rows_vuelo_t = cursor.fetchall()
    df_vuelo_t = pd.DataFrame(rows_vuelo_t, columns=['t_vuelo', 'cantidad_de_vuelos', 'Ranking_tendencias_A'])

    consulta6 = "select vuelo.trafico_vuelo, count (trafico_vuelo) as cantidad_de_vuelos, rank () over (order by ( count (trafico_vuelo))) as Ranking_trafico_vuelo from vuelo join utiliza on vuelo.id_vuelo=utiliza.id_vuelo where utiliza.cod_aero_origen in (select codigo from aeropuerto join ciudad on aeropuerto.id_ciudad=ciudad.id_ciudad where id_pais=1) group by vuelo.trafico_vuelo;"
    cursor.execute(consulta6)
    rows_trafico_t = cursor.fetchall()
    df_trafico_t = pd.DataFrame(rows_trafico_t, columns=['trafico_vuelo', 'cantidad_de_vuelos', 'Ranking_trafico_vuelo'])

    consulta7 = "select nombre_empresa, count (id_vuelo) as numero_de_vuelos, rank() over (order by (count (id_vuelo)) DESC) as Ranking_empresas_mayor_cantidad_de_vuelos_internacionales  from empresa join vuelo on empresa.id_empresa = vuelo.id_empresa where vuelo.trafico_vuelo = 'I' Group by nombre_empresa order by numero_de_vuelos DESC;"
    cursor.execute(consulta7)
    rows_empresa_t = cursor.fetchall()
    df_empresa_t = pd.DataFrame(rows_empresa_t, columns=['nombre_empresa', 'numero_de_vuelos', 'Ranking_empresas_mayor_cantidad_de_vuelos_internacionales'])

    consulta8 = "select nombre_empresa, count (id_vuelo) as numero_de_vuelos, rank() over (order by (count (id_vuelo)) DESC) as Ranking_empresas_mayor_cantidad_de_vuelos_nacionales from empresa join vuelo on empresa.id_empresa = vuelo.id_empresa where vuelo.trafico_vuelo = 'N' Group by nombre_empresa order by numero_de_vuelos DESC;"
    cursor.execute(consulta8)
    rows_empresa_tn = cursor.fetchall()
    df_empresa_tn = pd.DataFrame(rows_empresa_tn, columns=['nombre_empresa', 'numero_de_vuelos', 'Ranking_empresas_mayor_cantidad_de_vuelos_nacionales'])

    # Cerrar el cursor
    cursor.close()

    # Configuración de la aplicación Dash con Bootstrap
    app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

    # Layout de la aplicación Dash
    app.layout = dbc.Container(fluid=True, children=[
        dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=pil_image, height="60px"), width=3),
                            dbc.Col(dbc.NavbarBrand("Vuelos Analytics CO 2024", className="ml-2"), width=6),
                            dbc.Col(width=3)  # Columna vacía para alinear el contenido a la derecha
                        ],
                        align="center"
                    ),
                    dbc.Nav(   
                        [
                            dbc.NavItem(dbc.NavLink("Análisis de los Escenarios", href="/grafico")),
                            dbc.NavItem(dbc.NavLink("Conclusiones", href="/conclusiones")),
                        ],
                        navbar=True,
                        style={'margin-top': '30px'} 
                    ),
                ],
                fluid=True,
            ),
            color="dark",
            dark=True,
        ),
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', style={'padding': '20px'})
    ])

    # Callback para actualizar la página según la URL
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        if pathname == '/grafico':
            return html.Div([
                 html.H2('Análisis de los Escenarios', style={'textAlign': 'center','color': 'white', 'padding': '1rem', 'minHeight': '10px' }),
                # Resto del código para los gráficos y análisis
            ])
        elif pathname == '/inicio' or pathname == '/':
            return html.Div([
                html.H3('Introducción al análisis del proyecto', style={'textAlign': 'center','color': 'white', 'padding': '1rem', 'minHeight': '01px','fontSize': '2rem' }),  
                # Resto del código para la introducción y análisis del proyecto
            ])
        elif pathname == '/conclusiones':
            return html.Div([
                html.H2('Conclusiones',style={'textAlign': 'center','color': 'white', 'padding': '1rem', 'minHeight': '10px' }),
                # Resto del código para las conclusiones
            ])
        else:
            return html.Div([
                html.H2('Página no encontrada', style={'color': 'white', 'padding': '1rem', 'minHeight': '200px'}),
                html.P('La página que buscas no existe.')
            ])
                            
    if __name__== '__main__':
        print(app.run_server(debug=False))
    
except Exception as ex:
    print(ex) # Si ocurre algún error durante la ejecución del bloque try imprimira error
    
finally:
    connection.close()
    print("Conexión finalizada") # Mensaje para indicar que la conexión ha sido cerrada

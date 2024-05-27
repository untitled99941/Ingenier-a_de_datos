from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px 
import psycopg2 
import dash_bootstrap_components as dbc

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

    app= Dash(__name__)

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
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src="C:/Users/Public/proyecto_vuelos/logo.jpg", height="30px")),
                                dbc.Col(dbc.NavbarBrand("Vuelos Analytics CO 2024", className="ml-2")),
                            ],
                            align="center"
                        ),
                        href="/inicio",
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
                html.H4("Primer Escenario",style={'textAlign': 'center','color': 'white', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("descripcion primer analisis",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),

             dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='Tabla1',
                        figure=px.bar(df_empres_p.iloc[0:20], x='nombre_empresa', y='tendencia_carga', title='Top 20 de tendencia carga por empresa con tipo vuelo R', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                    )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del Primer grafica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

             dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='Tabla2',
                        figure=px.bar(df_empres_m.iloc[0:10], x='nombre_empresa', y='tendencia_carga', title='Top 10 de tendencia carga por empresa con tipo de vuelo T', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                    )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del Segundo grafica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

             dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='Tabla3',
                        figure=px.bar(df_empres_n.iloc[0:10], x='nombre_empresa', y='tendencia_carga', title='Top 10 de tendencia carga por empresa con tipo de vuelo C', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del tercera grafica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

             dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='Tabla4',
                        figure=px.bar(df_empres_s.iloc[0:20], x='nombre_empresa', y='tendencia_carga', title='Top 20 de tendencia carga por empresa con tipo de vuelo A', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                    )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del cuarta grafica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

            html.H4("Segundo Escenario",style={'textAlign': 'center','color': 'white', 'minHeight': '01px','fontSize': '2rem' }),
            html.P("descripcion segundo analisis",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),

             dbc.Row([
                dbc.Col(
                    dcc.Graph(
                         id='Tabla5',
                        figure=px.pie(df_vuelo_t.iloc[0:4], names='t_vuelo', values='cantidad_de_vuelos', title='Distribución de tipos de vuelos', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del segundo escenario"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

            html.H4("Tercer Escenario",style={'textAlign': 'center','color': 'white', 'minHeight': '01px','fontSize': '2rem' }),
            html.P("descripcion tercer analisis",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),

            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                         id='Tabla6',
                        figure=px.pie(df_trafico_t.iloc[0:2], names='trafico_vuelo', values='cantidad_de_vuelos', title='Tendencia de vuelo desde Colombia', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis del tercer escenario"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

            html.H4("Cuarto Escenario",style={'textAlign': 'center','color': 'white', 'minHeight': '01px','fontSize': '2rem' }),
            html.P("descripcion cuarto analisis",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),

            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                         id='Tabla7',
                        figure=px.bar(df_empresa_t.iloc[0:10], x='nombre_empresa', y='numero_de_vuelos', title='Top 10 empresas mas usadas para vuelos internacionales', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis de la primer grafica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                         id='Tabla8',
                        figure=px.bar(df_empresa_tn.iloc[0:10], x='nombre_empresa', y='numero_de_vuelos', title='Top 10 empresas mas usadas para vuelos nacionales', color_discrete_sequence=["#FFBB2F"]).update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'white'}})
                )
                ),
                dbc.Col(
                    html.Div([
                        html.H3("Análisis de la segunda gráfica"),
                        html.P("Aquí va tu análisis del escenario...")]))
            ]),

        ]) 

        
    
        elif pathname == '/inicio' or pathname == '/':
            return html.Div([
                html.H3('Introducción al análisis del proyecto', style={'textAlign': 'center','color': 'white', 'minHeight': '01px','fontSize': '2rem' }),  
                html.P("Para este proyecto se tomaron datos de la pagina principal de la aeronautica civil, en donde para el mes de febrero se registraron un total de 6805 vuelos que usaron el espacio aeréo perteneciente a Colombia.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("En este análisis vamos a comparar los siguientes datos divididos en 5 grupos los cuales seran : ",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("~ Pais"),
                html.P("~ Ciudad"),
                html.P("~ Aeropuerto"),
                html.P("~ Vuelo"),
                html.P("~ Empresa"),
                html.P("Cada uno de estos grupos cuenta con atributos diferentes y para mayor facilidad y un mejor analisis del proyecto se creo un grupo 6 de nombre Utiliza, este ultimo grupo junto a los demas se pueden visualizar sus atributos en la siguiente imagen: ",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.H3(children="Analisis del proyecto ",style={'textAlign': 'center','color': 'white', 'minHeight': '10px','fontSize': '2rem' }),
                html.P("En este paso procedemos a presentar los analisis que vamos a examinar en este proyecto: ",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("Se busca analizar un ranking de los Paises con mayores ciudades reportadas dentro de la base de datos.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("Se busca analizar un ranking de las ciudades en Colombia con mayores vuelos registrados en el mes de febrero del 2024, diferenciando origen y destino en diferentes gráfico.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("Se busca identificar cuál es la empresa que registra más número de vuelos.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("Se busca identificar el aeropuerto más usado en este periodo.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.P("Se busca identificar cuantos pasajeros trasportaron cada una de empresas en sus vuelos programados.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
            ])
        






        elif pathname == '/conclusiones':
            return html.Div([
                html.H2('Conclusiones',style={'textAlign': 'center','color': 'white', 'padding': '1rem', 'minHeight': '10px' }),
                html.P("Para concluir este analisis presentamos 4 puntos claves en donde podemos evidenciar los datos obtenidos del proyecto :",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.H3("Concentración de vuelos en ciudades principales:"),
                html.P("Los datos revelan una clara concentración de vuelos en las principales ciudades capitales de Colombia, como Bogotá, Medellín, Cartagena, Cali, y otras. Esta concentración sugiere una fuerte actividad económica y turística en estas áreas, lo que las convierte en puntos estratégicos para la aviación en el país.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.H3("Predominio de empresas extranjeras en el mercado:"),
                html.P("Aunque el análisis de las empresas con más vuelos registrados muestra una variedad de nombres, es notable la presencia dominante de empresas extranjeras en los primeros puestos del ranking. Esto puede indicar una competencia feroz en el mercado aéreo colombiano y posiblemente desafíos para las aerolíneas nacionales para mantener su participación de mercado.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }), 
                html.H3("Importancia del Aeropuerto El Dorado:"),
                html.P("Los datos demuestran que el Aeropuerto El Dorado en Bogotá es el aeropuerto más utilizado tanto para vuelos de origen como de destino. Este hallazgo subraya la posición estratégica de Bogotá como un centro neurálgico para la aviación en Colombia y posiblemente en América Latina.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
                html.H3("Liderazgo de Avianca en transporte de pasajeros:"),
                html.P("Avianca emerge como la empresa líder en el transporte de pasajeros durante el período analizado. Su predominio en este aspecto sugiere una fuerte presencia en el mercado y posiblemente una reputación sólida entre los viajeros colombianos y extranjeros que eligen volar dentro del país.",style={'textAlign': 'justify','color': 'white', 'minHeight': '1px' }),
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
    connection.close() #Hola
    print("Conexión finalizada") # Imprimimos un mensaje para indicar que la conexión ha sido cerrada
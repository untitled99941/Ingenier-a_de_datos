#Con este codigo podemos conectar la base de datos con python para hacer posteriores analisis
from dash import Dash, html, dcc, Output, Input
import pandas as pd
import plotly.express as px 
import psycopg2 # Importamos la librería psycopg2 para conectarnos a la base de datos PostgreSQL

try:
    # Intentamos establecer una conexión con la base de datos PostgreSQL
    connection = psycopg2.connect(
        host='localhost',  # Dirección del servidor de base de datos
        user='postgres',  # Nombre de usuario
        password='123456789',  # Contraseña del usuario
        database='Proyectosjo',  # Nombre de la base de datos a la que queremos conectarnos
        port='5433', # Puerto en el que está escuchando el servidor de base de datos
    )

    #La configuración anterior depende del computador, pero mostramos en la que nos funciona a nosotros 
    print("Conexión exitosa") # Si la conexión es exitosa, imprimimos un mensaje
    cursor = connection.cursor() # Creamos un objeto cursor para ejecutar comandos SQL

    # En esta parte del codigo vamos a visualizar cada una de las tablas de las que esta compuesta el proyecto

    #Visualización de la tabla Pais
    app= Dash(__name__)

    consulta1 = "SELECT pais.nombre_pais, COUNT(ciudad.id_ciudad) AS num_ciudades, RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_Paises FROM ciudad JOIN pais ON ciudad.id_pais = pais.id_pais GROUP BY pais.nombre_pais ORDER BY Ranking_Paises;"
    cursor.execute(consulta1)
    rows_pais = cursor.fetchall()
    df_pais = pd.DataFrame(rows_pais, columns=['nombre_pais', 'num_ciudades', 'Ranking_Paises'])

    consulta2 = "SELECT nombre_ciudad,COUNT(ciudad.id_ciudad) AS num_vuelos,RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_ciudades from ciudad join aeropuerto on ciudad.id_ciudad = aeropuerto.id_ciudad join utiliza on aeropuerto.codigo = utiliza.cod_aero_origen where ciudad.id_ciudad in(select id_ciudad from ciudad where id_pais = 1)GROUP BY ciudad.nombre_ciudad ORDER BY Ranking_ciudades;"
    cursor.execute(consulta2)
    rows_ciudad_o = cursor.fetchall()
    df_ciudad_o = pd.DataFrame(rows_ciudad_o, columns=['nombre_ciudad', 'num_vuelos', 'Ranking_ciudades'])

    consulta3 = "SELECT nombre_ciudad,COUNT(ciudad.id_ciudad) AS num_vuelos,RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_ciudades from ciudad join aeropuerto on ciudad.id_ciudad = aeropuerto.id_ciudad join utiliza on aeropuerto.codigo = utiliza.cod_aero_destino where ciudad.id_ciudad in(select id_ciudad from ciudad where id_pais = 1)GROUP BY ciudad.nombre_ciudad ORDER BY Ranking_ciudades"
    cursor.execute(consulta3)
    rows_ciudad_d = cursor.fetchall()
    df_ciudad_d = pd.DataFrame(rows_ciudad_d, columns=['nombre_ciudad', 'num_vuelos', 'Ranking_ciudades'])

    consulta4 = "SELECT nombre_empresa,COUNT(vuelo.id_empresa) AS num_vuelos, RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_empresas from empresa join vuelo on empresa.id_empresa = vuelo.id_empresa where empresa.id_empresa = vuelo.id_empresa GROUP BY empresa.nombre_empresa ORDER BY Ranking_empresas;"
    cursor.execute(consulta4)
    rows_empresa_v = cursor.fetchall()
    df_empresa_v = pd.DataFrame(rows_empresa_v, columns=['nombre_empresa', 'num_vuelos', 'Ranking_empresas'])

    consulta5 = "SELECT nombre_aeropuerto,COUNT(utiliza.cod_aero_origen) AS num_vuelos, RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_aeropuerto from aeropuerto join ciudad on ciudad.id_ciudad = aeropuerto.id_ciudad join utiliza on aeropuerto.codigo = utiliza.cod_aero_origen where ciudad.id_ciudad = aeropuerto.id_ciudad GROUP BY aeropuerto.nombre_aeropuerto ORDER BY Ranking_aeropuerto;"
    cursor.execute(consulta5)
    rows_aeropuerto_o = cursor.fetchall()
    df_aeropuerto_o = pd.DataFrame(rows_aeropuerto_o, columns=['nombre_aeropuerto', 'num_vuelos', 'Ranking_aeropuerto'])

    consulta6 = "SELECT nombre_aeropuerto,COUNT(utiliza.cod_aero_destino) AS num_vuelos, RANK() OVER (ORDER BY COUNT(*) DESC) AS Ranking_aeropuerto from aeropuerto join ciudad on ciudad.id_ciudad = aeropuerto.id_ciudad join utiliza on aeropuerto.codigo = utiliza.cod_aero_destino where ciudad.id_ciudad = aeropuerto.id_ciudad GROUP BY aeropuerto.nombre_aeropuerto ORDER BY Ranking_aeropuerto;"
    cursor.execute(consulta6)
    rows_aeropuerto_d = cursor.fetchall()
    df_aeropuerto_d = pd.DataFrame(rows_aeropuerto_d, columns=['nombre_aeropuerto', 'num_vuelos', 'Ranking_aeropuerto'])

    consulta7 = "SELECT nombre_empresa,sum(vuelo.pasajeros) AS total_pasajeros,RANK() OVER (ORDER BY sum(pasajeros) DESC) AS Ranking_empresas from empresa join vuelo on empresa.id_empresa = vuelo.id_empresa where empresa.id_empresa = vuelo.id_empresa GROUP BY empresa.nombre_empresa ORDER BY Ranking_empresas;"
    cursor.execute(consulta7)
    rows_empresa_p = cursor.fetchall()
    df_empresa_p = pd.DataFrame(rows_empresa_p, columns=['nombre_empresa', 'total_pasajeros', 'Ranking_empresas'])

    # Cerrar el cursor
    cursor.close()


    app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif',
                                'backgroundSize': 'cover',
                                'backgroundRepeat': 'no-repeat',
                                'backgroundPosition': 'absolute'}, 
                        children=[
                                html.Nav(style={'backgroundColor': '#333', 'padding': '1rem'}, children=[
                                    html.A('Inicio', href='/inicio', style={'color': 'white', 'marginRight': '2rem'}),
                                    html.A('Análisis de los Escenarios Planteados', href='/grafico', style={'color': 'white', 'marginRight': '2rem'}),
                                    html.A('Conclusiones del Proyecto', href='/conclusiones', style={'color': 'white'})
                                ]),
                                html.Div(children='''Proyecto Ingeneria de Datos Vuelos Analytics CO 2024 Profundizando en el Aire Colombiano
''', style={'textAlign': 'center', 'margin': '2rem', 'fontSize': '2rem','minHeight': '5px'}),
                                dcc.Location(id='url', refresh=False),
                                html.Div(id='page-content', style={'padding': '1rem'})
                                ]   
                            )
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )

    def display_page(pathname):
        if pathname == '/grafico':
            return html.Div([
                html.H1('Análisis de los Escenarios Planteados', style={'textAlign': 'center','color': 'Black', 'padding': '1rem', 'minHeight': '10px' }),
                html.H2("Primer Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("Empezando por el primer escenario, el cual dice que Se busca analizar un ranking de los Paises con mayores ciudades reportadas dentro de la base de datos.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),

        dcc.Graph(
            id='Tabla1',
            figure=px.bar(df_pais.iloc[0:10], x='nombre_pais', y='num_ciudades', title='Top 10 Países con más Ciudades en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),
                html.H1("Análisis del Primer Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("Analizando la gráfica que se acaba de generar, podemos identificar varios puntos importantes a simple vista, como la base de datos es propia de Colombia es evidente que el país con más ciudades sea Colombia pero además de eso encontramos que todos los primeros 10 en el ranking son países con los cuales Colombia posee relaciones internacionales muy sólidas además de ser potencias en sus regiones, por otro lado tenemos que tiene muy pocas conexiones con oriente en donde el país con más ciudades de la parte oriental del mundo es emiratos árabes con 2 ciudades, esto puede evidenciar que las relaciones actuales en Colombia tienden a ser más hacia la parte occidental del mundo. ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),

                html.H2("Segundo Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("En el Segundo Esceneario, se busca analizar un ranking de las ciudades en Colombia con mayores vuelos registrados en el mes de febrero del 2024, este analisis diferenciando los vuelos de origen y los de destino.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),

        dcc.Graph(
            id='Tabla2',
            figure=px.bar(df_ciudad_o.iloc[0:20], x='nombre_ciudad', y='num_vuelos', title='Top 20 Ciudades con más vuelos de Origen en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),
        dcc.Graph(
            id='Tabla3',
            figure=px.bar(df_ciudad_d.iloc[0:20], x='nombre_ciudad', y='num_vuelos', title='Top 20 Ciudades con más vuelos de Destino en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),
                html.H1("Análisis del Segundo Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem'}),
                html.P("Analizando la primera grafica que se acaba de generar, podemos visualizar una tendencia las ciudades en donde más vuelos se registran  son las ciudades capitales del país en donde podemos ver que tanto Bogotá con el Aeropuerto el Dorado, Medellín con el aeropuerto de Olaya Herrera, Cartagena con el Rafael Núñez, Cali con el Alfonso Bonilla Aragón y las demás ciudades capitales lideran este ranking, esto se debe también a que en todas esta ciudades mencionadas a una alta inversión económica tanto en lo empresarial como en lo turístico permite que la gente que habita en estas ciudades se permitan poder volar en avión, por lo que por estas razones se presentan que estas ciudades tienen la mayor cantidades de vuelos de origen, algo a mencionar dentro de este análisis es que la ciudad de Mitú presenta varios aeropuertos llegando a un total 32 aeropuertos pero investigando en como la característica en que la Aerocivil define como aeropuerto descubrí que en este caso se refiere a las pista que se poseen cerca de la área urbana entonces es por eso que aunque Mitú no sea una ciudad capital la vemos en unos puestos arriba de muchas otras ciudades. ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Analizando la segunda grafica que se acaba de generar, podemos visualizar que la tendencia con respecto a la primera grafica no cambia mucho a diferencia de que en esta segunda grafica se evidencia un mayor porcentaje de las ciudades turísticas del país tales como lo son Barranquilla, San Andrés, Cartagena y Bogotá. ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),

                html.H2("Tercer Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("En el Tercer Esceneario, Se busca identificar cuál es la empresa que registra más número de vuelos",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
        dcc.Graph(
            id='Tabla4',
            figure=px.bar(df_empresa_v.iloc[0:10], x='nombre_empresa', y='num_vuelos', title='Top 10 empresas con más vuelos', color_discrete_sequence=["#FFBB2F"])
        ),
                html.H1("Análisis del Tercer Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem'}),
                html.P("Analizando detenidamente la gráfica recién generada, es evidente que, entre los 10 primeros de empresas con más vuelos registrados en el periodo analizado, la predominancia de compañías extranjeras supera a las nacionales. Esta observación refleja la dinámica competitiva del mercado aéreo colombiano, donde las aerolíneas internacionales también juegan un papel significativo en la oferta de servicios aéreos. Un dato relevante que surge al examinar los datos es la marcada diferencia en el número de vuelos entre la primera y la décima posición en el ranking. Con una brecha de más de 1000 vuelos, esta disparidad resalta la posición de liderazgo de las principales empresas en comparación con el resto de la competencia. Esta brecha puede atribuirse a una combinación de factores, que van desde la capacidad operativa y la red de rutas hasta la demanda del mercado y las estrategias comerciales de cada empresa.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
            
                html.H2("Cuarto Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("En el Cuarto Esceneario, Se busca identificar el aeropuerto más usado en este periodo,este analisis diferenciando los vuelos de origen y los de destino.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
            dcc.Graph(
            id='Tabla5',
            figure=px.bar(df_aeropuerto_o.iloc[0:20], x='nombre_aeropuerto', y='num_vuelos', title='Top 20 aeropuertos con más vuelos de origen en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),
            dcc.Graph(
            id='Tabla6',
            figure=px.bar(df_aeropuerto_d.iloc[0:20], x='nombre_aeropuerto', y='num_vuelos', title='Top 20 aeropuertos con más vuelos de destino en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),        
                html.H1("Análisis del Cuarto Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem'}),

                html.P("Analizando la primera grafica que se acaba de generar, podemos visualizar una tendencia que ya habíamos analizado anteriormente esto debido a que como la base de datos es de Colombia la mayoría de los datos son respectivamente de Colombia, además de que el primer aeropuerto que no está en el territorio colombiano esta después del top 10 de este ranking. ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Analizando la segunda grafica que se acaba de generar, podemos visualizar que la tendencia con respecto a la primera grafica no cambia a mucho y en ambas graficas Bogotá con el Aeropuerto el Dorado lidera los rankings.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.H2("Quinto Escenario",style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),
                html.P("En el Cuarto Esceneario, Se busca identificar el aeropuerto más usado en este periodo,este analisis diferenciando los vuelos de origen y los de destino.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
            dcc.Graph(
            id='Tabla7',
            figure=px.pie(df_empresa_p.iloc[0:20], names='nombre_empresa', values='total_pasajeros', title='Top 10 empresas con mas pasajeros trasportados en el mes de febrero del 2024', color_discrete_sequence=["#FFBB2F"])
        ),  
                html.P("Analizando la gráfica que se acaba de generar, podemos identificar que Avianca es la empresa que más pasajeros movió en el periodo de febrero del 2024 en el espacio aéreo colombiano, doblando en su total de pasajeros al segundo, esto demostrando el poderío que tiene Avianca en la movilidad aérea, y algo curioso en este análisis es que la empresa que más vuelos tiene registrados ocupa el top 4 en el ranking. ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
            ])
        elif pathname == '/inicio' or pathname == '/':
            return html.Div([
                html.H3('Introducción al análisis del proyecto', style={'textAlign': 'center','color': 'Black', 'minHeight': '01px','fontSize': '2rem' }),  
                html.P("Para este proyecto se tomaron datos de la pagina principal de la aeronautica civil, en donde para el mes de febrero se registraron un total de 6805 vuelos que usaron el espacio aeréo perteneciente a Colombia.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("En este análisis vamos a comparar los siguientes datos divididos en 5 grupos los cuales seran : ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("~ Pais"),
                html.P("~ Ciudad"),
                html.P("~ Aeropuerto"),
                html.P("~ Vuelo"),
                html.P("~ Empresa"),
                html.P("Cada uno de estos grupos cuenta con atributos diferentes y para mayor facilidad y un mejor analisis del proyecto se creo un grupo 6 de nombre Utiliza, este ultimo grupo junto a los demas se pueden visualizar sus atributos en la siguiente imagen: ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.H3(children="Analisis del proyecto ",style={'textAlign': 'center','color': 'Black', 'minHeight': '10px','fontSize': '2rem' }),
                html.P("En este paso procedemos a presentar los analisis que vamos a examinar en este proyecto: ",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Se busca analizar un ranking de los Paises con mayores ciudades reportadas dentro de la base de datos.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Se busca analizar un ranking de las ciudades en Colombia con mayores vuelos registrados en el mes de febrero del 2024, diferenciando origen y destino en diferentes gráfico.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Se busca identificar cuál es la empresa que registra más número de vuelos.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Se busca identificar el aeropuerto más usado en este periodo.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.P("Se busca identificar cuantos pasajeros trasportaron cada una de empresas en sus vuelos programados.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
            ])
        elif pathname == '/conclusiones':
            return html.Div([
                html.H2('Conclusiones',style={'textAlign': 'center','color': 'Black', 'padding': '1rem', 'minHeight': '10px' }),
                html.P("Para concluir este analisis presentamos 4 puntos claves en donde podemos evidenciar los datos obtenidos del proyecto :",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.H3("Concentración de vuelos en ciudades principales:"),
                html.P("Los datos revelan una clara concentración de vuelos en las principales ciudades capitales de Colombia, como Bogotá, Medellín, Cartagena, Cali, y otras. Esta concentración sugiere una fuerte actividad económica y turística en estas áreas, lo que las convierte en puntos estratégicos para la aviación en el país.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.H3("Predominio de empresas extranjeras en el mercado:"),
                html.P("Aunque el análisis de las empresas con más vuelos registrados muestra una variedad de nombres, es notable la presencia dominante de empresas extranjeras en los primeros puestos del ranking. Esto puede indicar una competencia feroz en el mercado aéreo colombiano y posiblemente desafíos para las aerolíneas nacionales para mantener su participación de mercado.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }), 
                html.H3("Importancia del Aeropuerto El Dorado:"),
                html.P("Los datos demuestran que el Aeropuerto El Dorado en Bogotá es el aeropuerto más utilizado tanto para vuelos de origen como de destino. Este hallazgo subraya la posición estratégica de Bogotá como un centro neurálgico para la aviación en Colombia y posiblemente en América Latina.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
                html.H3("Liderazgo de Avianca en transporte de pasajeros:"),
                html.P("Avianca emerge como la empresa líder en el transporte de pasajeros durante el período analizado. Su predominio en este aspecto sugiere una fuerte presencia en el mercado y posiblemente una reputación sólida entre los viajeros colombianos y extranjeros que eligen volar dentro del país.",style={'textAlign': 'justify','color': 'Black', 'minHeight': '1px' }),
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
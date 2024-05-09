/*En este archivo encuentras el codigo para la creación en la Base de datos como su posterior carga masiva de los datos a la misma */

/*Creación de la tabla Pais*/
	
create table pais(
id_pais int primary key,
	nombre_pais varchar(21)
);

/*Creación de la tabla Ciudad'*/
	
create table ciudad(
id_ciudad int primary key,
	nombre_ciudad varchar(28),
	id_pais int,
	foreign key (id_pais) REFERENCES Pais(id_pais)
);

/*Creación de la tabla Aeropuerto'*/

create table aeropuerto(
codigo char(3) primary key,
	nombre_aeropuerto varchar(55),
	id_ciudad int,
	foreign key (id_ciudad) REFERENCES ciudad(id_ciudad)
);

/*Creación de la tabla Empresa'*/

create table empresa(
id_empresa integer primary key,
	siglas_empresa char(3),
nombre_empresa varchar(52)
);

/*Creación de la tabla vuelo'*/

create table vuelo (
id_vuelo int primary key,
	id_empresa int,
	trafico_vuelo char(1),
	t_vuelo char(1),
	pasajeros int,
	carga int,
	foreign key (id_empresa) REFERENCES empresa(id_empresa)
);

/*Creación de la tabla utiliza'*/

create table utiliza (
id_vuelo int primary key,
cod_aero_destino char(3),
cod_aero_origen char(3),
	foreign key (id_vuelo) REFERENCES vuelo(id_vuelo),
	foreign key (cod_aero_destino) REFERENCES aeropuerto(codigo),
	foreign key (cod_aero_origen) REFERENCES aeropuerto(codigo)	
);

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla pais con su debida noramlización en 3NF'*/

copy pais (id_pais,nombre_pais) 
from 'C:\Users\Public\pais.csv' delimiter ';' csv header

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla ciudad con su debida noramlización en 3NF'*/

copy ciudad (id_ciudad,nombre_ciudad,id_pais) 
from 'C:\Users\Public\ciudad.csv' delimiter ';' csv header

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla aeropuerto con su debida noramlización en 3NF'*/

copy aeropuerto (codigo,nombre_aeropuerto,id_ciudad) 
from 'C:\Users\Public\aeropuerto.csv' delimiter ';' csv header

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla empresa con su debida noramlización en 3NF'*/

copy empresa (id_empresa,siglas_empresa,nombre_empresa) 
from 'C:\Users\Public\empresa.csv' delimiter ';' csv header

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla vuelo con su debida noramlización en 3NF'*/

copy vuelo (id_vuelo,id_empresa,trafico_vuelo,t_vuelo,pasajeros,carga) 
from 'C:\Users\Public\vuelo.csv' delimiter ';' csv header

/*Con esta consulta se cargan de manera masiva los datos correspondientes a la tabla utiliza con su debida noramlización en 3NF'*/

copy utiliza (id_vuelo,cod_aero_destino,cod_aero_origen) 
from 'C:\Users\Public\utiliza.csv' delimiter ';' csv header

# Laboratorio: Ficheros XML (HR Oracle Scheme)

Este proyecto consiste en la migración, validación y consulta del esquema relacional HR de Oracle, transformándolo en un modelo jerárquico nativo XML. 
Para ello, se diseñó un esquema XSD a medida que unifica las tablas relacionales en una estructura de árbol optimizada para consultas.

## Estructura del proyecto

```text
lab1_hr_scheme/
├── data/
│   ├── hrscheme.xsd                   # Esquema de validación (XSD)
│   └── hrscheme.xml                   # XML definitivo
├── data_raw/
│   ├── countries.csv              
│   ├── departments.csv                
│   ├── employees.csv                 
│   ├── job_history.csv                
│   ├── jobs.csv                
│   ├── locations.csv                
│   └── regions.csv               
├── queries/
│   ├── xpath.xq                      # Consulta de filtrado en XPath
│   └── xquery.xq                     # Consulta analítica en XQuery (FLWOR)
├── myenv/                            # Entorno virtual de Python 
└── scripts/
    ├── convert_csv_to_xml.py         # Parsing inicial de CSV a XML
    └── fix_xml_dates.py              # Script de corrección de fechas a formato ISO

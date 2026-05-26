import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

def corregir_fechas_xml():
    # 1. Configurar rutas dinámicas basadas en la ubicación del script
    # script_dir apuntará a: /tu_ruta/lab1_hr_scheme/scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Apuntar directamente a la carpeta 'data' subiendo un nivel ('..') y entrando a 'data'
    xml_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'hrscheme.xml'))
    
    if not os.path.exists(xml_path):
        print(f"Error crítico: No se encontró el archivo XML en la ruta calculada:\n{xml_path}")
        print("Por favor, verifica que el archivo se llame exactamente 'hrscheme.xml' y esté dentro de la carpeta 'data'.")
        return

    print(f"Leyendo y procesando el archivo definitivo en: {xml_path}")
    
    # 3. Parsear el XML manteniendo la estructura intacta
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    contador_cambios = 0

    def transformar_texto_fecha(texto):
        """Convierte una cadena DD/MM/YY a AAAA-MM-DD si es necesario"""
        if not texto:
            return texto
        texto_limpio = texto.strip()
        try:
            # Si ya viene con el formato correcto AAAA-MM-DD, lo dejamos quieto
            datetime.strptime(texto_limpio, "%Y-%m-%d")
            return texto_limpio  
        except ValueError:
            pass

        try:
            # Intentar parsear el formato incorrecto DD/MM/YY (ej: 17/09/03)
            dt = datetime.strptime(texto_limpio, "%d/%m/%y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            try:
                # Por si acaso viene como DD/MM/AAAA (ej: 17/09/2003)
                dt = datetime.strptime(texto_limpio, "%d/%m/%Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                return texto

    # 4. Buscar y actualizar los elementos de fecha específicos sin tocar <geography>
    elementos_fecha = root.findall('.//hire_date') + root.findall('.//start_date') + root.findall('.//end_date')
    
    for elem in elementos_fecha:
        if elem.text:
            fecha_original = elem.text
            fecha_corregida = transformar_texto_fecha(fecha_original)
            
            if fecha_original != fecha_corregida:
                elem.text = fecha_corregida
                contador_cambios += 1

    print(f"Se identificaron y corrigieron {contador_cambios} fechas.")

    # 5. Guardar los cambios de vuelta en /data/hrscheme.xml manteniendo el formato
    print("Re-formateando el archivo XML...")
    xml_raw = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_raw)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    
    # Limpiar saltos de línea vacíos duplicados por minidom
    clean_xml = "\n".join([line for line in pretty_xml.split('\n') if line.strip()])
    
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(clean_xml)
        
    print(f"¡Éxito total! Archivo modificado y guardado en: {xml_path}")

if __name__ == '__main__':
    corregir_fechas_xml()
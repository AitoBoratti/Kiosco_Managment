from abc import ABC, abstractmethod
import sqlite3 as sql


class DataBase(ABC):
    def __init__(self,database):
        self.db_name = database
        
    def _conect(self):
        """Conecta con la base de datos y crea el cursor"""
        conexion = sql.connect(self.db_name)
        cursor = conexion.cursor()
        return conexion,cursor
    
    def _execute(self,query,params=(),fetchall=False,fetchone=False):
        """Ejecuta una unica query y devuelve los resultados de ser estos necesarios"""
        conexion,cursor = self._conect()
        # Iniciamos un try por la posibilidad de error. 
        try:
            #Ejecuta la Query
            cursor.execute(query,params) 
            #Si se marco el parametro, devuelve una lista de resultados
            if fetchall:
                data = cursor.fetchall()
                conexion.close()        
                return data
            #Si se marco el parametro, devuelve un unico resultado
            elif fetchone:
                data = cursor.fetchone()
                conexion.close()
                return data
            #Si no se requiere ningun resultado, se guardan los cambios
            else:
                conexion.commit()
        #Si se genera un error en la base de datos, lo informamos        
        except sql.Error as e:
            print(f"Error en la base de datos {self.db_name}: {e}")
        finally:
        #Finalmente, cerramos la base de datos si no fue cerrada anteriormente
            conexion.close()
  
    def _executemany(self,query,params):
        "Ejecuta multiples lineas. No puede devolver datos"
        conexion,cursor = self._conect()
        try:
            cursor.executemany(query,params)
            conexion.commit()
        except sql.Error as e:
            print(f"Error en la base de datos {self.db_name}: {e}")
        finally:
            conexion.close()    
  
    @abstractmethod
    def get_all_data(self):
        pass
  
class DB_Product(DataBase):          
        
    def __init__(self):
        super().__init__('Database\Test.db')
      
          
    def create_product_table(self):
        """Creamos la tabla producto en caso de ser necesaria"""
        
        query='''
            CREATE TABLE IF NOT EXISTS productos(
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre        TEXT NOT NULL,
                categoria     TEXT NOT NULL,
                cantidad      INTEGER NOT NULL,
                precio        REAL NOT NULL,
                codigo_barra  TEXT UNIQUE,
                fecha_ingreso DATE
            )'''
        self._execute(query)
        
        
    def add_new_product(self, nombre, categoria, cantidad, 
                        precio, codigo_barra, fecha_ingreso):
        query='''
                INSERT INTO productos (nombre, categoria, cantidad, precio, codigo_barra, fecha_ingreso) 
                VALUES (?,?,?,?,?,?)
              '''
        params = (nombre, categoria, cantidad, precio, codigo_barra, fecha_ingreso)
        self._execute(query,params)
        
        
    def delete_product(self, id):
        query='DELETE FROM productos WHERE id = ?'
        params=(id,)
        self._execute(query,params)        
   
     
    def get_all_data(self):
        query='SELECT * FROM productos'
        print(self._execute(query=query,fetchall=True))
      
        
    def decrease_quantity(self,bar_code=-1,id=-1):
        """Decrementamos la cantidad del producto"""
        if id == -1 and bar_code == -1:
            print("ERROR: At least one parameter is requiered")
        elif id == -1 and bar_code != -1:
            id = self._execute('SELECT id FROM productos WHERE codigo_barra = ?',(bar_code,),fetchone=True)[0]
        self._execute('UPDATE productos SET cantidad = cantidad - 1 WHERE id = ? AND cantidad > 0 ',(id,))
    
    
    def get_no_stock_items(self):
        """Se obtienen los productos sin stock"""
        items = self._execute('SELECT id, nombre FROM productos WHERE cantidad = 0',fetchall=True)
        for item in items:
            print(f'{item[0]}: {item[1]}') 


    def get_items_by_stock(self):
        """Se obtiene un listado de productos ordenados por stock"""
        items = self._execute('SELECT nombre, cantidad FROM productos ORDER BY cantidad DESC',fetchall=True)
        for item in items:
            print(f'{item[0]}: {item[1]}')
    
    
    
    
    
dataBase = DB_Product()
dataBase.get_items_by_stock()
from abc import ABC, abstractmethod

class Conexion(ABC):
    @abstractmethod
    def conectar(self):
        pass

class Query(ABC):
    @abstractmethod
    def ejecutar(self):
        pass

class ConexionMySQL(Conexion):
    def conectar(self):
        print("Conectando a MySQL")

class QueryMySQL(Query):
    def ejecutar(self):
        print("Ejecutando query en MySQL")

class ConexionPostgres(Conexion):
    def conectar(self):
        print("Conectando a PostgreSQL")

class QueryPostgres(Query):
    def ejecutar(self):
        print("Ejecutando query en PostgreSQL")

class DBFactory(ABC):
    @abstractmethod
    def crear_conexion(self) -> Conexion:
        pass

    @abstractmethod
    def crear_query(self) -> Query:
        pass

class MySQLFactory(DBFactory):
    def crear_conexion(self):
        return ConexionMySQL()

    def crear_query(self):
        return QueryMySQL()

class PostgresFactory(DBFactory):
    def crear_conexion(self):
        return ConexionPostgres()

    def crear_query(self):
        return QueryPostgres()

class Aplication:
  def __init__(self, fabrica: DBFactory):
      self.conexion = fabrica.crear_conexion()
      self.query = fabrica.crear_query()
  
  def ejecutar(self):
      self.conexion.conectar()
      self.query.ejecutar()

if __name__ == "__main__":
    print("=== Base de datos MySQL ===")
    fabricaMySQL = MySQLFactory()
    appMySQL = Aplication(fabricaMySQL)
    appMySQL.ejecutar()

    print("\n=== Base de datos PostgreSQL ===")
    fabricaPSQL = PostgresFactory()
    appPSQL = Aplication(fabricaPSQL)
    appPSQL.ejecutar()

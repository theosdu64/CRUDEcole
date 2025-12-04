from ecole.models.address import Address
from ecole.daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class AddressDao(Dao[Address]):

    def create(self, address: Address) -> int:
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO address (street, city, postal_code) VALUES (%s, %s, %s)"
            cursor.execute(sql, (address.street, address.city, address.postal_code))
            Dao.connection.commit()
            return cursor.lastrowid

    def read(self, id_course: int) -> Optional[Address]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""

        return True

    def read_all(self) -> Optional[Address]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""

        return True

    def update(self, id_address: int, address: Address) -> bool:
        try:
            with Dao.connection.cursor() as cursor:
                sql = """
                       UPDATE address 
                       SET street = %s, city = %s, postal_code = %s
                       WHERE id_address = %s
                   """
                cursor.execute(sql, (
                    address.street,
                    address.city,
                    address.postal_code,
                    id_address
                ))
                Dao.connection.commit()
                return True
        except Exception as e:
            Dao.connection.rollback()
            print(f"Erreur lors de la mise à jour de l'adresse : {e}")
            return False

    def delete(self, course: Address) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...
        return True
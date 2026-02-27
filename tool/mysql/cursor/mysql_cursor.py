from tool.mysql.connection.mysql_connection import getConnection


class MysqlCursor:
    def __init__(self):
        self.connection = getConnection()
        self.cursor = self.connection.cursor()

    def query(self, customer_code):
        sql = "SELECT muyu_region, customer_type, customer_name, product_name, mgmt_category FROM sales_detail WHERE customer_code = %s"
        self.cursor.execute(sql, (customer_code,))
        result = self.cursor.fetchone()
        return result

if __name__ == '__main__':
    cursor = MysqlCursor()
    print(cursor.query(customer_code='1900010454'))
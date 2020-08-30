import psycopg2


def connect_to_database():
    connection = psycopg2.connect(user="sinao",
                                  password="4143622",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="voicekit_db")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print(connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")


try:
    connect_to_database()
except psycopg2.OperationalError as error:
    print(error)

# connect_to_database()

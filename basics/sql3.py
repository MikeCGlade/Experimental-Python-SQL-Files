import sqlite3

# Reference:
# https://www.tutorialspoint.com/sql/sql-syntax.htm


#Establishes a connection to a database or creates a new one if it can't find it.
def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")
        raise
    
#Create a table
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("Table was created")
    except Exception as e:
        print(e)
        
#Add users to database example
def insert_user(connection, name:str, age:int, email:str):
    query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try: 
        with connection:
            #execute takes query and the inputs - see above
            connection.execute(query, (name, age, email))
        print(f"User: {name} was added to database")
    except Exception as e:
        print(e)

#Get users
def fetch_users(connection, condition: str = None) -> list[tuple]: #(josh, 27, email)
    query = "SELECT * FROM users"
    if condition:
        query += f" WHERE {condition}"
    
    try:
        with connection:
            rows = connection.execute(query).fetchall()
            return rows; 
    except Exception as e:
        print(e)

#Delete a user
def delete_user(connection, user_id:int):
    query = "DELETE FROM users WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (user_id,))
        print(f"USER ID: {user_id} was deleted")
    except Exception as e:
        print(e)
    
#Update a user
def update_user(connection, user_id:int, email:str):
    query = "UPDATE users SET email = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (email, user_id))
        print(f"User ID {user_id} has new email of {email}")
    except Exception as e:
        print(e)
    
#Insert users
def insert_users(connection, users:list[tuple[str, int, str]]):
    query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        with connection:
            connection.executemany(query, users)
            print(f"{len(users)} were added to the database!")
    except Exception as e:
        print(e)
    
def main():
    connection = None
    
    while input("Enter 0 to exit! ").trim() != '0':
        try:
            #Make database / connect
            connection = get_connection("data.db")
            #Make a table / use execute() to query
            create_table(connection)
            
            start = input("Enter Option (Add, Delete, Update, Search, Add Many): ").lower()
            if start == "add":
                name = input("Enter name: ")
                age = int(input("Enter age: "))
                email = input("Enter email: ")
                insert_user(connection, name, age, email)
                
            elif start == "search":
                print("All users")
                for user in fetch_users(connection):
                    print(user)
            
            elif start == "delete":
                user_id = int(input("Enter User ID: "))
                delete_user(connection, user_id)
                
            elif start == "update":
                user_id = int(input("Enter user ID: "))
                new_email = int(input("Enter a new email: "))
                update_user(connection, user_id, new_email)
            
            elif start == "add many":
                users = [("Axe", 29, "lol@gmail.com"), ("Mark", 20, "scent@gmail.com"), ("Zanny", 22, "zanny@gmail.com")]
                insert_users(connection, users)
                
        #default after end    
        finally:
            connection.close()
    
if __name__ == "__main__":
    main()
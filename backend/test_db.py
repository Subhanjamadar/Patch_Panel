from models import Session, PatchPort

def test_db_connection():
    try:
        session = Session()
        count = session.query(PatchPort).count()
        print(f"Successfully connected to database. Found {count} patch ports.")
        session.close()
        return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection()

import psycopg2
from psycopg2 import Error
from config import Config

class Database:
    """データベース接続および操作クラス"""

    @staticmethod
    def get_connection():
        """データベース接続を確立し、返します"""
        try:
            conn = psycopg2.connect(**Config.DB_CONFIG)
            return conn
        except Error as e:
            print(f"× データベース接続エラー: {e}")
            return None

    @staticmethod
    def init_db():
        """データベーステーブルを初期化します"""
        conn = Database.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Create students table if it doesn`t exit
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        student_number VARCHAR(20) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                # Create index for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_student_number ON students(student_number)")
                conn.commit()
                cursor.close()
                print("☑ データベースが正常に初期化されました。")
            except Error as e:
                print(f"× データベース初期化エラー: {e}")
            finally:
                conn.close()

    @staticmethod
    def add_student(name, student_number):
        """新しい学生をデータベースに追加します"""
        conn = Database.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO students (name, student_number) VALUES (%s, %s)",
                    (name, student_number)
                )
                conn.commit()
                cursor.close()
                return True, "学生が正常に追加されました！"
            except Error as e:
                conn.rollback()
                if "duplicate key" in str(e).lower():
                    return False, "学生番号はすでに存在します！"
                return False, f"データベースエラー: {e}"
            finally:
                conn.close()
        return False, "データベースに接続できませんでした。"

    @staticmethod
    def get_all_students():
        """データベースからすべての学生を取得します"""
        conn = Database.get_connection()
        students = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, student_number, created_at
                    FROM students
                    ORDER BY created_at DESC
                """)
                students = cursor.fetchall()
                cursor.close()
            except Error as e:
                print(f"× 学生情報の取得エラー: {e}")
            finally:
                conn.close()
        return students

    @staticmethod
    def search_students(query):
        """名前または学生番号で学生を検索します"""
        conn = Database.get_connection()
        students = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, name, student_number, created_at
                    FROM students
                    WHERE name ILIKE %s OR student_number ILIKE %s
                    ORDER BY created_at DESC
                """, (f'%{query}%', f'%{query}%'))
                students = cursor.fetchall()
                cursor.close()
            except Error as e:
                print(f"× 学生検索エラー: {e}")
            finally:
                conn.close()
            return students
        
        @staticmethod
        def delete_student(student_id):
            """IDで学生を削除します"""
        conn = Database.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id = %s", ("student_id,"))
                conn.commit()
                affected_rows = cursor.rowcount  # 削除された件数
                cursor.close()
                return affected_rows > 0
            except Error as e:
                conn.rollback()
                print(f"× 学生削除エラー: {e}")
                return False
            finally:
                conn.close()
        return False
        
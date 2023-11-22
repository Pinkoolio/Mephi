import sqlite3

courses_data = [(1, 'python', '21.07.21', '21.08.21'), (2, 'java', '13.07.21', '16.08.21')]

students_data = [
(1, 'Max', 'Brooks', 24, 'Spb'),
(2, 'John', 'Stones', 15, 'Spb'),
(3, 'Andy', 'Wings', 45, 'Manhester'),
(4, 'Kate', 'Brooks', 34, 'Spb')]

student_courses_data = [
(1, 1),
(2, 1),
(3, 1),
(4, 2)]

class Table():
    def __init__(self, table_name, foreign=None, **params):
        self.table_name = table_name
        self.params = params
        self.foreign = foreign

    def create(self, cursor):
        pie = ''.join('{} {},\n'.format(key, val) for key, val in self.params.items())[:-2]
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}({pie})''')

    def is_empty(self, cursor):
        cursor.execute(f"SELECT count(*) FROM (select 1 from {self.table_name} limit 1);")
        option = cursor.fetchall()[0][0]
        if option == 0: return True
        else: False

    def add(self, cursor, data):
        for i in data:
            for k in data:
                if len(i)!=len(k):
                    print('Ошибка в заполнении данных')
                    break
        values = ('?, '*len(data[0]))[:-2]
        cursor.executemany(f'''INSERT INTO {self.table_name} VALUES({values})''', data)

    def request(self, cursor, term):
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE {term}")
        return cursor.fetchall()

    # def check_course(self, cursor, table1, course):
    #     cursor.execute(f"SELECT * FROM {table1} WHERE course_id == {course}")
    #     ids = cursor.fetchall()
    #
    #     print(f'\nФамилии и имена студентов, на курсе:')
    #     for id in ids:
    #         cursor.execute(f"SELECT name, surname FROM {self.table_name} WHERE id == {0}".format(id[0]))
    #         student = cursor.fetchone()
    #         print(student)
    # почему-то не работает

students = Table(table_name='Students', id='INT UNIQUE', name='TEXT', surname='TEXT', age='INT', city='TEXT')
course = Table(table_name='Course', id='INT UNIQUE', name='TEXT NOT NULL', time_start='datetime', time_end='datetime')
students_courses = Table(table_name='Students_courses', student_id='INTEGER', course_id='INTEGER')

try:
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    print("База данных создана и успешно подключена к SQLite")
    students.create(cursor)
    course.create(cursor)

    students_courses.create(cursor)
    if students.is_empty(cursor):
        students.add(cursor, students_data)
    if course.is_empty(cursor):
        course.add(cursor, courses_data)
    if students_courses.is_empty(cursor):
        students_courses.add(cursor, student_courses_data)
    connection.commit()

    students30 = students.request(cursor, term='age>30')
    print('Список студентов, старше 30:')
    for i in students30:
        print(i[1]+' '+ i[2])

    # students.check_course(cursor, table1='Students_courses', course='1')
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (connection):
        connection.close()
        print("Соединение с SQLite закрыто")
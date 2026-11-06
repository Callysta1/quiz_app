# TUJUAN : SEGALA YANG BERKAITAN DENGAN DATABASE

import sqlite3
db_name = 'quiz.sqlite'
conn = None # Membuat Koneksi ke database
cursor = None # Cursor untuk akses datanase

# Mekanisme Akses Database
## Buka Database
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

## Tutup Database
def close():
    cursor.close()
    conn.close()

## Jelajah Database
def do(query):
    cursor.execute(query)

## Reset Database
def clear_db():
    open()
    query1 = '''DROP TABLE IF EXISTS quiz_content''' #tabel pertanyaan
    query2 = '''DROP TABLE IF EXISTS questions''' #tabel question
    query3 = '''DROP TABLE IF EXISTS quiz''' #tabel quiz
    do(query1)
    do(query2)
    do(query3)
    close()

## Membuat Tabel
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    query_create_quiz_table = '''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )
    '''
    query_create_questions_table = '''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
    )
    '''
    query_create_quiz_content_table = '''
    CREATE TABLE IF NOT EXISTS quiz_content(
      id            INTEGER PRIMARY KEY,
      quiz_id       INTEGER,
      question_id   INTEGER,
      
      FOREIGN KEY (quiz_id) REFERENCES quiz(id),
      FOREIGN KEY (question_id) REFERENCES questions(id)
    )
    '''
    do(query_create_quiz_table)
    print('Quiz Table Created')
    do(query_create_questions_table)
    print('Questions Table Created')
    do(query_create_quiz_content_table)
    print('Quiz Content Table Created')
    close()
        

## Membuat daftar pertanyaan
def add_questions():
    question = [
        ("Manakah jenis jaringan hewan yang berfungsi sebagai pelapis permukaan luar dan dalam organ tubuh serta membentuk kelenjar?", "Jaringan epitel", "Jaringan ikat", "Jaringan otot", "Jaringan saraf"),
        ("Otot yang bekerja secara tidak sadar (involunter), berbentuk gelendong dengan satu inti di tengah, dan ditemukan pada organ dalam seperti lambung adalah...", "Otot polos", "Otot lurik", "Otot jantung", "Otot rangka"),
        ("Sel darah putih yang berfungsi memproduksi antibodi untuk melawan patogen spesifik dalam sistem kekebalan tubuh adalah...", "Limfosit", "Eritrosit", "Trombosit", "Neutrofil"),
        ("Bagian dari neuron yang berfungsi membawa/meneruskan impuls atau rangsangan menuju ke badan sel saraf disebut...", "Dendrit", "Akson", "Nodus Ranvier", "Sel Schwann"),

        ("Aturan atau pedoman tertulis maupun tidak tertulis yang berisi perintah dan larangan untuk mengatur tingkah laku manusia dalam masyarakat disebut...", "Norma sosial", "Nilai sosial", "Sosialisasi", "Interaksi sosial"),
        ("Tahap sosialisasi menurut George Herbert Mead di mana anak mulai mampu mengambil peran orang lain secara lebih luas dan memahami aturan dalam masyarakat (generalized others) adalah...", "Game stage", "Preparatory stage", "Play stage", "Significant stage"),
        ("Seorang anak diajarkan oleh orang tuanya mengenai sopan santun, kejujuran, dan cara makan yang baik sejak kecil di lingkungan keluarga. Hal ini merupakan contoh dari...", "Sosialisasi primer", "Sosialisasi sekunder", "Sosialisasi represif", "Sosialisasi otoriter"),
        ("Nilai sosial yang bersumber dari akal pikiran, penalaran, dan kemampuan intelek manusia disebut sebagai nilai...", "Kebenaran (rasional)", "Keindahan (estetika)", "Moral (kebaikan)", "Agama (kerohanian)"),

        ("Berdasarkan Pasal 1 Ayat (1) UUD NRI Tahun 1945, bentuk negara Indonesia adalah negara kesatuan yang berbentuk...", "Republik", "Monarki", "Federasi", "Serikat"),
        ("Prinsip yang menegaskan bahwa seluruh wilayah daratan, lautan, dan udara Indonesia merupakan satu kesatuan yang utuh dan tidak terpisahkan adalah konsep...", "Wawasan Nusantara", "Otonomi Daerah", "Bhinneka Tunggal Ika", "Sistem Ketahanan Nasional"),
        ("Salah satu Pasal dalam UUD NRI Tahun 1945 yang secara tegas menyatakan bahwa bentuk Negara Kesatuan Republik Indonesia tidak dapat diubah adalah...", "Pasal 37 Ayat (5)", "Pasal 1 Ayat (2)", "Pasal 27 Ayat (3)", "Pasal 30 Ayat (1)"),
        ("Tindakan nyata seorang siswa dalam mendukung dan mempertahankan keutuhan NKRI di lingkungan sekolah adalah...", "Menghargai perbedaan suku dan agama teman", "Membentuk kelompok belajar yang eksklusif", "Menjauhi teman yang berbeda pandangan politik", "Menolak mempelajari budaya daerah lain"),
    ]

    open()
    cursor.executemany(
        '''
        INSERT INTO questions
        (question, answer, wrong1, wrong2, wrong3)
        VALUES(?, ?, ?, ?, ?)
        ''', question
    )
    conn.commit()
    close()

## Membuat daftar Type Quiz
def add_quiz():
    quizes = [
    ('Biologi',),
    ('Sosiologi',),
    ('PPKN',),
    ]
    open()
    cursor.executemany(
        '''
        INSERT INTO quiz
        (name)
        VALUES(?)
        ''', quizes
    )
    conn.commit()
    close()


## Membuat hubungan antara pertanyaan dan Type Quiz
def add_links():
    link = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 8),
    (3, 9),
    (3, 10),
    (3, 11),
    (3, 12),
    ]
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    cursor.executemany(
    '''
    INSERT INTO quiz_content(quiz_id, question_id) VALUES (?,?)
    ''', link
    )
    conn.commit()  
    close()
    print('Data seeded successfuly')

# Apa yang diperlukan untuk menampilkan pertanyaan berikutnya?
# Nomor pertanyaan yang sudah ditanyakann. 
# Nomor Quiz (Quiz id) 
def get_question_after(question_id = 0, quiz_id=1):
  open()
  query = '''
    SELECT 
        quiz_content.id,
        questions.question,
        questions.answer,
        questions.wrong1,
        questions.wrong2,
        questions.wrong3
    FROM
        questions,
        quiz_content
    WHERE 
        quiz_content.question_id == questions.id
        AND quiz_content.id > ?
        AND quiz_content.quiz_id == ?
    ORDER BY
        quiz_content.id
      
  '''
  
  cursor.execute(query, [question_id, quiz_id])
  result = cursor.fetchone() #untuk mengambil 1 data saja (1 row)
  close()
  return result

## Entry Point untuk menjalankan program
def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    add_links()
    # get_question_after(question_id = 0, quiz_id =1)
    print(get_question_after(3, 1))

if __name__ == "__main__":
  main()
import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():  #pendefinisian fungsi bernama create_database, Tidak memiliki parameter, artinya fungsi ini hanya perlu dipanggil untuk dijalankan.
    con = sqlite3.connect('nilai_siswa.db')   # sqlite3.connect() adalah metode untuk membuat atau membuka file database SQLite.'nilai_siswa.db' adalah nama file database yang akan dibuat jika belum ada.Variabel con menyimpan koneksi ke database tersebut.
    cursor = con.cursor() #Membuat objek cursor untuk eksekusi SQL.
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT)
    ''') #cursor.execute(''' ... '''):Digunakan untuk menjalankan perintah SQL di database, seperti membuat tabel atau manipulasi data.Dalam kasus ini, menjalankan query untuk membuat tabel nilai_siswa.
    con.commit() #Menyimpan perubahan ke database.
    con.close() #Menutup koneksi database.

# Fungsi untuk mengambil semua data dari tabel nilai_siswa.
def fetch_data(): #Definisi fungsi fetch_data untuk mengambil data dari database.
    con = sqlite3.connect('nilai_siswa.db') #Menghubungkan ke database nilai_siswa.db.
    cursor = con.cursor() #Membuat objek cursor untuk eksekusi SQL.
    cursor.execute('SELECT * FROM nilai_siswa') #Menjalankan perintah SQL untuk mengambil seluruh data dari tabel nilai_siswa.
    rows = cursor.fetchall() #Menyimpan semua hasil query ke dalam variabel rows.
    con.close() #Menutup koneksi database.
    return rows #Mengembalikan data hasil query dalam bentuk list.

# Fungsi untuk menyimpan data siswa baru ke dalam database.
def save_to_database(nama, biologi, fisika, inggris, prediksi): #Mendefinisikan fungsi untuk menyimpan data ke tabel nilai_siswa.
    con = sqlite3.connect('nilai_siswa.db') #Menghubungkan ke database nilai_siswa.db.
    cursor = con.cursor() #Membuat objek cursor untuk menjalankan perintah SQL.
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        ''', (nama, biologi, fisika, inggris, prediksi)) #Menjalankan perintah INSERT INTO untuk memasukkan data ke tabel nilai_siswa.? itu kayak tempat kosong buat diisi nilai nantinya.Jadi, nilai seperti nama, biologi, dll., akan dimasukkan ke dalam ? sesuai urutannya.
    con.commit() #Menyimpan perubahan ke database.
    con.close() #Menutup koneksi database.

# Fungsi untuk memperbarui data siswa berdasarkan ID.
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?,
        biologi = ?,
        fisika = ?'
        inggris = ?.
        prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    con.commit()
    con.close()

# Fungsi untuk menghapus data siswa berdasarkan ID.
def delete_database(record_id):
    con = sqlite3.connect('nilai_siswa.db')
    cursor = con.cursor()
    cursor.execute('''
        DELETE from nilai_siswa
        WHERE id = ?
''', (record_id,))
    con.commit()
    con.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai tertinggi.
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menambahkan data baru di form GUI.
def submit():
    try: #Mulai blok try-except untuk menangani error selama eksekusi fungsi.
        nama = nama_var.get() #Mengambil nilai nama dari input pengguna.
        biologi = int(biologi_var.get()) #Mengambil nilai mata pelajaran Biologi dan mengubahnya ke tipe data int.
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama: #Mengecek apakah nama kosong. Jika kosong, fungsi akan menimbulkan error dengan raise Exception
            raise Exception("Nama siswa tidak boleh kosong.")
        
        prediksi = calculate_prediction(biologi, fisika, inggris) #Fungsi ini akan menghitung atau menentukan prediksi fakultas berdasarkan nilai yang diberikan, lalu menyimpannya ke dalam variabel prediksi.
        save_to_database(nama, biologi, fisika, inggris, prediksi) #Fungsi save_to_database dipanggil untuk menyimpan data pengguna ke database.

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}") #Sebuah pesan pop-up akan muncul menggunakan messagebox.showinfo, yang memberikan notifikasi kepada pengguna bahwa data berhasil disimpan serta prediksi fakultas.
        clear_inputs() #Fungsi clear_inputs dipanggil untuk menghapus atau mereset semua input pengguna pada form. Hal ini memastikan form kosong kembali setelah data berhasil disimpan.
        populate_table() #Fungsi populate_table dipanggil untuk memperbarui tampilan tabel dalam aplikasi. Misalnya, tabel di aplikasi diperbarui dengan data baru yang baru saja disimpan ke database. Fungsi ini biasanya mengambil data dari database dan menampilkannya di GUI.
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}") #Jika ada error tipe ValueError, tampilkan pop-up dengan pesan "Input tidak valid".ValueError terjadi ketika sebuah fungsi menerima nilai (value) yang tidak sesuai dengan tipe atau format yang diharapkan.

# Fungsi untuk memperbarui data yang dipilih di form GUI.
def update():
    try:
        if not selected_record_id.get(): #Mengecek apakah pengguna belum memilih data dari tabel untuk di-update.Jika selected_record_id kosong munculkan error dengan pesan
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get()) ##Mengambil ID record yg dipilih dan mengubahnya ke tipe data int.
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih di form GUI.
def delete():
    try:
        if not selected_record_id.get(): #Mengecek apakah pengguna belum memilih data dari tabel untuk di-delete.Jika selected_record_id kosong munculkan error dengan pesan
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

#raise Exception: Kamu bikin error sendiri dan kasih pesan ke program.
#ValueError as e: Program bakal error karena kesalahan input, dan kamu bisa tangani atau lihat pesan kesalahannya.

# Fungsi untuk mengosongkan semua input di form GUI
def clear_inputs():
    nama_var.set("") #Mengosongkan input nama.
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk menampilkan data di tabel Tkinter. Fungsi ini menghapus data lama dari tabel dan kemudian memperbarui tabel dengan data baru yang diambil dari fungsi fetch_data().
def populate_table():
    for row in tree.get_children(): #Mengambil semua baris di tabel (tree).
        tree.delete(row) #Menghapus setiap baris dari tabel.
    for row in fetch_data(): #Mengambil data baru dari fetch_data().
        tree.insert('', 'end', values=row) #Menambahkan data baru ke tabel di posisi akhir.

# Fungsi mengisi input dari data tabel yang dipilih. 
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] #Mengambil baris yang dipilih dari tabel Indeks digunakan untuk mengakses data dalam urutan kolom di baris yang dipilih di tabel.
        selected_row = tree.item(selected_item)['values'] #Mengambil nilai-nilai dari baris yang dipilih. 

        selected_record_id.set(selected_row[0]) #Mengisi ID record dengan nilai dari kolom pertama.
        nama_var.set(selected_row[1]) #Mengisi nama dengan nilai dari kolom kedua.
        biologi_var.set(selected_row[2]) #Mengisi nilai biologi dengan nilai dari kolom ketiga.
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError: #Jika tidak ada baris yang dipilih atau terjadi kesalahan, maka muncul pesan error.
        messagebox.showerror("Error", "Pilih data yang valid!")

#IndexError Terjadi: Ketika mencoba mengakses elemen dari sebuah list, tuple, atau array dengan indeks yang di luar jangkauan.
#ValueError Terjadi: Ketika fungsi menerima nilai yang tidak sesuai dengan tipe data atau format yang diharapkan.

# Inisialisasi database : menyiapkan database pertama kali agar siap digunakan. Jika tidak memanggil fungsi ini, database atau tabel mungkin belum ada, sehingga aplikasi tidak dapat menyimpan data dengan benar.
create_database() 

# Membuat GUI dengan tkinter
root = Tk() #root = Tk(): Membuat jendela utama aplikasi.
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar() #Membuat objek StringVar() untuk menyimpan nilai input nama siswa. StringVar() adalah tipe data yang digunakan di Tkinter untuk menghubungkan variabel Python dengan widget GUI (seperti entry field).agar ketika nilai pada widget berubah, variabel ini juga otomatis terupdate.
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Label dan Input untuk Nama Siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) #menampilkan Label dengan teks "Nama Siswa".
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # menyediakan Entry field (kolom input) untuk nama siswa yang terhubung dengan variabel nama_var.

# Label dan Input untuk Nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

# Label dan Input untuk Nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

# Label dan Input untuk Nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol Aksi: Add, Update, dan Delete
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10) #Button(root, text="Add", command=submit): Membuat tombol dengan teks "Add". Ketika tombol ini diklik, fungsi submit akan dipanggil. Fungsi submit ini biasanya bertanggung jawab untuk menambah data ke dalam aplikasi (misalnya, menyimpan data siswa).
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10) #Membuat tombol dengan teks "Update". Ketika tombol ini diklik, fungsi update akan dipanggil. Fungsi update ini biasanya digunakan untuk memperbarui data yang sudah ada.
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10) #Membuat tombol dengan teks "Delete". Ketika tombol ini diklik, fungsi delete akan dipanggil. Fungsi delete biasanya digunakan untuk menghapus data.

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings') #Kode ini mendefinisikan sebuah tabel (menggunakan Treeview) yang terdiri dari beberapa kolom untuk menampilkan data siswa dan prediksi fakultasnya.

# Mengatur posisi isi tabel di tengah
for col in columns: #Melakukan perulangan untuk setiap kolom yang ada dalam tuple columns
    tree.heading(col, text=col.capitalize())  #tree.heading(col, text=col.capitalize()):Fungsi ini mengatur judul kolom pada tabel.col.capitalize() memastikan bahwa nama kolom (seperti "id") akan ditampilkan dengan huruf kapital pertama ("Id").
    tree.column(col, anchor='center') #Menentukan penempatan teks di kolom agar terpusat di tengah (anchor 'center').

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menempatkan tabel (treeview) di baris ke-5 dan kolom ke-0.
# columnspan=3 berarti tabel akan menggabungkan 3 kolom dalam grid (agar cukup untuk menampilkan tabel).
# padx=10, pady=10 memberikan padding horizontal 10 piksel dan vertikal 10 piksel di sekitar tabel untuk memberikan ruang di sekitarnya.

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

#tree.bind('<ButtonRelease-1>', fill_inputs_from_table)
# Mengikat event klik (menggunakan tombol kiri mouse, ButtonRelease-1) pada tabel tree.
# Ketika pengguna mengklik baris dalam tabel, fill_inputs_from_table akan dipanggil. Fungsi ini mengisi kolom input di form berdasarkan data dari baris yang dipilih di tabel.

populate_table()
#Fungsi ini digunakan untuk mengisi tabel dengan data yang diambil dari sumber data (misalnya, database atau daftar). Biasanya, ini akan menampilkan data yang sudah ada (seperti data siswa) dalam tabel yang telah dibuat.
root.mainloop()
#Menjalankan loop utama aplikasi Tkinter yang akan menjaga aplikasi tetap berjalan dan menangani semua interaksi pengguna dengan antarmuka (seperti klik tombol, input data, dll.).
#Tanpa baris ini, aplikasi akan segera berhenti setelah tampilan muncul.
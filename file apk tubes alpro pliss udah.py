import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

MAX_MAHASISWA = 100  
data_mahasiswa = [None] * MAX_MAHASISWA
current_sort_order = False  

COLOR_PRIMARY = "#f0f8ff"
COLOR_SECONDARY = "#e6f7ff" 
COLOR_ACCENT = "#f8cee3"
COLOR_BUTTON = "#d1e7ff"
COLOR_BUTTON_ACTIVE = "#a8d4ff"
COLOR_TEXT = "#2e2e2e"
COLOR_INPUT_BG = "#ffffff"
COLOR_LABEL_BG = "#e6f7ff"
COLOR_TABLE_HEADER = "#d1e7ff"
COLOR_TABLE_SELECTION = "#f8cee3"
COLOR_STATUS_BAR = "#d1e7ff"

def hitung_nilai_akhir(tugas, uts, uas):
    return (0.3 * tugas) + (0.3 * uts) + (0.4 * uas)

def konversi_kategori(nilai):
    if nilai >= 85: return "A"
    elif nilai >= 80: return "AB"
    elif nilai >= 75: return "B"
    elif nilai >= 70: return "BC"
    elif nilai >= 65: return "C"
    elif nilai >= 50: return "D"
    else: return "E"

def is_valid_name(nama):
    return all(char.isalpha() or char.isspace() for char in nama)

def tambah_data(nim, nama, tugas, uts, uas):
    try:
        if not nim or not nama:
            raise ValueError("NIM dan Nama harus diisi!")
        if not nim.isdigit():
            raise ValueError("NIM harus berupa angka!")
        if any(mhs is not None and mhs['nim'] == nim for mhs in data_mahasiswa):
            raise ValueError("NIM sudah terdaftar!")
        if not is_valid_name(nama):
            raise ValueError("Nama harus berupa huruf dan tidak boleh mengandung angka atau simbol!")
        
        # Konversi nilai ke float
        tugas = float(tugas)
        uts = float(uts)
        uas = float(uas)

        if not all(0 <= x <= 100 for x in (tugas, uts, uas)):
            raise ValueError("Nilai harus antara 0-100!")

        index_kosong = next((i for i, v in enumerate(data_mahasiswa) if v is None), None)
        if index_kosong is None:
            raise ValueError("Database penuh! Tidak bisa menambah data baru.")

        nilai_akhir = hitung_nilai_akhir(tugas, uts, uas)
        kategori = konversi_kategori(nilai_akhir)

        data_mahasiswa[index_kosong] = {
            'nim': nim,
            'nama': nama,
            'tugas': tugas,
            'uts': uts,
            'uas': uas,
            'nilai_akhir': nilai_akhir,
            'kategori': kategori
        }

        messagebox.showinfo("Sukses", "Data mahasiswa berhasil disimpan!")
        refresh_tabel()
        clear_form()
        return True

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False


def update_data():
    try:
        nim = entry_nim.get()
        if not nim:
            raise ValueError("Pilih data yang akan diupdate terlebih dahulu!")
        idx = next((i for i,v in enumerate(data_mahasiswa) if v and v['nim']==nim), None)
        if idx is None:
            raise ValueError("Data tidak ditemukan!")
        nama = entry_nama.get()
        tugas = float(entry_tugas.get())
        uts = float(entry_uts.get())
        uas = float(entry_uas.get())
        if not is_valid_name(nama) or not all(0<=x<=100 for x in (tugas,uts,uas)):
            raise ValueError("Input tidak valid!")
        nilai_akhir = hitung_nilai_akhir(tugas, uts, uas)
        data_mahasiswa[idx] = {
            'nim': nim,'nama': nama,
            'tugas': tugas,'uts': uts,'uas': uas,
            'nilai_akhir': nilai_akhir,
            'kategori': konversi_kategori(nilai_akhir)
        }
        messagebox.showinfo("Sukses", "Data mahasiswa berhasil diperbarui!")
        refresh_tabel()
        clear_form()
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

def delete_data():
    nim = entry_nim.get()
    idx = next((i for i,v in enumerate(data_mahasiswa) if v and v['nim']==nim), None)
    if idx is None:
        messagebox.showerror("Error", "Pilih data yang akan dihapus terlebih dahulu!")
        return
    data_mahasiswa[idx] = None
    messagebox.showinfo("Sukses","Data mahasiswa berhasil dihapus!")
    refresh_tabel()
    clear_form()

def cari_data(keyword):
    hasil = [None]*MAX_MAHASISWA
    c=0
    for v in data_mahasiswa:
        if v and (keyword.lower() in v['nim'].lower() or keyword.lower() in v['nama'].lower()):
            hasil[c]=v; c+=1
    return hasil[:c]

def urutkan_data():
    buf=[None]*MAX_MAHASISWA; n=0
    for v in data_mahasiswa:
        if v: buf[n]=v; n+=1
    for i in range(n):
        sel=i
        for j in range(i+1,n):
            if current_sort_order:
                if buf[j]['nilai_akhir']<buf[sel]['nilai_akhir']: sel=j
            else:
                if buf[j]['nilai_akhir']>buf[sel]['nilai_akhir']: sel=j
        buf[i],buf[sel]=buf[sel],buf[i]
    return buf[:n]

def refresh_tabel(data=None):
    for r in tabel.get_children(): tabel.delete(r)
    buf=[None]*MAX_MAHASISWA; c=0
    src = data if data is not None else data_mahasiswa
    for v in src:
        if v: buf[c]=v; c+=1
    for i,v in enumerate(buf[:c],start=1):
        tabel.insert("","end",values=(i,v['nim'],v['nama'],v['tugas'],v['uts'],v['uas'],f"{v['nilai_akhir']:.2f}",v['kategori']))

def clear_form():
    entry_nim.delete(0,tk.END)
    entry_nama.delete(0,tk.END)
    entry_tugas.delete(0,tk.END)
    entry_uts.delete(0,tk.END)
    entry_uas.delete(0,tk.END)
    btn_simpan.config(text="Simpan Data",command=save_data)

def save_data():
    nim = entry_nim.get()
    exists = any(v and v['nim']==nim for v in data_mahasiswa)
    if nim and exists: update_data()
    else: tambah_data(nim, entry_nama.get(), entry_tugas.get(), entry_uts.get(), entry_uas.get())

def on_table_select(event):
    """Handler ketika baris di tabel dipilih"""
    selected_item = tabel.focus()
    if selected_item:
        values = tabel.item(selected_item, 'values')
        clear_form()
        entry_nim.insert(0, values[1])
        entry_nama.insert(0, values[2])
        entry_tugas.insert(0, values[3])
        entry_uts.insert(0, values[4])
        entry_uas.insert(0, values[5])
        btn_simpan.config(text="Update Data", command=save_data)

def on_cari():
    """Handler tombol cari"""
    keyword = entry_cari.get()
    if keyword:
        hasil = cari_data(keyword)
        refresh_tabel(hasil)
    else:
        refresh_tabel()

def on_sort():
    """Handler tombol sort"""
    global current_sort_order
    current_sort_order = var_sort_order.get() == 1  
    
    hasil = urutkan_data()
    refresh_tabel(hasil)

def on_export():
    """Export data ke file CSV"""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", ".csv"), ("All Files", ".*")]
        )
        if not file_path:
            return
        
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'No', 'NIM', 'Nama', 'Tugas', 'UTS', 'UAS', 
                'Nilai Akhir', 'Kategori'
            ])
            
        data_aktif = [None] * MAX_MAHASISWA
        n = 0
        for mhs in data_mahasiswa:
            if mhs is not None:
                data_aktif[n] = mhs
                n += 1
        for i in range(n):
            mhs = data_aktif[i]
            writer.writerow([
                i+1, mhs['nim'], mhs['nama'],
                mhs['tugas'], mhs['uts'], mhs['uas'],
                f"{mhs['nilai_akhir']:.2f}", mhs['kategori']
            ])

        
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekspor data: {str(e)}")

def on_import():
    """Handler untuk mengimpor data dari CSV (format minimal: NIM, Nama, Tugas, UTS, UAS)"""
    try:
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", ".csv"), ("All Files", ".*")]
        )
        if not file_path:
            return
        
        jumlah_berhasil = 0
        jumlah_gagal = 0
        jumlah_duplikat = 0
        
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Baca header
            
            # Deteksi kolom berdasarkan header
            col_indices = {}
            for i, col in enumerate(headers):
                col_lower = col.strip().lower()
                if "nim" in col_lower:
                    col_indices['nim'] = i
                elif "nama" in col_lower:
                    col_indices['nama'] = i
                elif "tugas" in col_lower:
                    col_indices['tugas'] = i
                elif "uts" in col_lower:
                    col_indices['uts'] = i
                elif "uas" in col_lower:
                    col_indices['uas'] = i
            
            # Pastikan semua kolom penting ditemukan
            required_cols = ['nim', 'nama', 'tugas', 'uts', 'uas']
            if not all(col in col_indices for col in required_cols):
                messagebox.showerror("Error", "Format CSV tidak valid! Pastikan ada kolom: NIM, Nama, Tugas, UTS, UAS")
                return
            
            for row in reader:
                if not row:
                    continue
                
                try:
                    nim = row[col_indices['nim']].strip()
                    nama = row[col_indices['nama']].strip()
                    tugas = row[col_indices['tugas']].strip()
                    uts = row[col_indices['uts']].strip()
                    uas = row[col_indices['uas']].strip()
                    
                    # Validasi dasar
                    if not nim or not nama:
                        raise ValueError("NIM atau Nama kosong")
                    
                    if any(mhs and mhs['nim'] == nim for mhs in data_mahasiswa if mhs):
                        jumlah_duplikat += 1
                        continue
                    
                    # Konversi nilai
                    try:
                        tugas = float(tugas)
                        uts = float(uts)
                        uas = float(uas)
                    except ValueError:
                        raise ValueError("Nilai harus berupa angka")
                    
                    if not (0 <= tugas <= 100) or not (0 <= uts <= 100) or not (0 <= uas <= 100):
                        raise ValueError("Nilai harus antara 0-100")
                    
                    # Hitung nilai akhir dan kategori
                    nilai_akhir = hitung_nilai_akhir(tugas, uts, uas)
                    kategori = konversi_kategori(nilai_akhir)
                    
                    # Cari slot kosong
                    index_kosong = None
                    for i in range(MAX_MAHASISWA):
                        if data_mahasiswa[i] is None:
                            index_kosong = i
                            break
                    
                    if index_kosong is None:
                        messagebox.showwarning("Peringatan", "Database penuh! Data tidak bisa diimpor.")
                        jumlah_gagal += 1
                        continue
                    
                    # Simpan data
                    data_mahasiswa[index_kosong] = {
                        'nim': nim,
                        'nama': nama,
                        'tugas': tugas,
                        'uts': uts,
                        'uas': uas,
                        'nilai_akhir': nilai_akhir,
                        'kategori': kategori
                    }
                    jumlah_berhasil += 1
                    
                except Exception as e:
                    print(f"Gagal impor baris: {row}, Error: {str(e)}")
                    jumlah_gagal += 1
        
        messagebox.showinfo(
            "Impor Selesai",
            f"Hasil impor:\nBerhasil: {jumlah_berhasil}\nGagal: {jumlah_gagal}\nDuplikat: {jumlah_duplikat}"
        )
        refresh_tabel()
    
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengimpor data: {str(e)}")
        
def show_statistik():
    """Menampilkan grafik statistik nilai (dengan kategori huruf saja)"""
    if not any(data_mahasiswa):
        messagebox.showwarning("Data Kosong", "Tidak ada data untuk ditampilkan")
        return
    
    nilai_akhir = [0.0] * MAX_MAHASISWA
    n = 0
    for mhs in data_mahasiswa:
        if mhs:
            nilai_akhir[n] = mhs['nilai_akhir']
            n += 1
    nilai_akhir = nilai_akhir[:n]

    
    kategori_list = ["A", "AB", "B", "BC", "C", "D", "E"]
    kategori_count = {k: 0 for k in kategori_list}
    
    for mhs in data_mahasiswa:
        if mhs:
            kategori_count[mhs['kategori']] += 1
    
    stat_window = tk.Toplevel(root)
    stat_window.title("Statistik Nilai")
    stat_window.geometry("800x600")
    stat_window.configure(bg=COLOR_PRIMARY)
    
    fig1 = plt.Figure(figsize=(6, 4), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.hist(nilai_akhir, bins=10, edgecolor='black', alpha=0.7, color=COLOR_ACCENT)
    ax1.set_title('Distribusi Nilai Akhir')
    ax1.set_xlabel('Nilai Akhir')
    ax1.set_ylabel('Jumlah Mahasiswa')
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=stat_window)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)
    
    fig2 = plt.Figure(figsize=(6, 4), dpi=100)
    ax2 = fig2.add_subplot(111)
    labels = kategori_list
    values = [kategori_count[k] for k in labels]
    ax2.bar(labels, values, color=COLOR_SECONDARY)
    ax2.set_title('Distribusi Kategori Nilai')
    ax2.set_xlabel('Kategori')
    ax2.set_ylabel('Jumlah Mahasiswa')
    
    for i, v in enumerate(values):
        ax2.text(i, v + 0.2, str(v), ha='center', fontsize=9)
    
    canvas2 = FigureCanvasTkAgg(fig2, master=stat_window)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)

def focus_next_widget(event):
    """Fokus ke widget berikutnya saat menekan Enter"""
    event.widget.tk_focusNext().focus()
    return "break"

root = tk.Tk()
root.title("Aplikasi Manajemen Nilai Mahasiswa")
root.geometry("1200x600")
root.resizable(True, True)
root.configure(bg=COLOR_PRIMARY)

# Konfigurasi style
style = ttk.Style()
style.theme_use('clam')

# Konfigurasi tema umum dengan warna yang diperbaiki
style.configure(".", background=COLOR_PRIMARY, foreground=COLOR_TEXT)
style.configure("TFrame", background=COLOR_PRIMARY)
style.configure("TLabel", background=COLOR_PRIMARY, foreground=COLOR_TEXT, font=('Arial', 9))
style.configure("TButton", 
                background=COLOR_BUTTON,
                foreground=COLOR_TEXT,
                borderwidth=1,
                relief="solid",
                font=('Arial', 9))
style.map("TButton",
        background=[('active', COLOR_BUTTON_ACTIVE)],
        relief=[('pressed', 'sunken')])
        
style.configure("TEntry", 
                fieldbackground=COLOR_INPUT_BG,
                foreground=COLOR_TEXT,
                insertcolor=COLOR_TEXT,
                font=('Arial', 9))
                
style.configure("TLabelframe", 
                background=COLOR_SECONDARY,
                relief="solid",
                borderwidth=1)
style.configure("TLabelframe.Label", 
                background=COLOR_SECONDARY,
                foreground=COLOR_TEXT,
                font=('Arial', 9, 'bold'))

# Konfigurasi tabel dengan warna
style.configure("Treeview",
                background=COLOR_INPUT_BG,
                fieldbackground=COLOR_INPUT_BG,
                foreground=COLOR_TEXT,
                rowheight=25,
                font=('Arial', 9))
style.configure("Treeview.Heading", 
                background=COLOR_TABLE_HEADER,
                foreground=COLOR_TEXT,
                font=('Arial', 9, 'bold'))
style.map("Treeview",
        background=[('selected', COLOR_TABLE_SELECTION)])

# Style khusus untuk label input dan tombol aksi
style.configure("InputLabel.TLabel", 
                background=COLOR_LABEL_BG,
                padding=(5, 2),
                relief="solid",
                borderwidth=0,
                font=('Arial', 9))
style.configure("Action.TButton", 
                background=COLOR_SECONDARY,
                foreground=COLOR_TEXT,
                padding=5,
                font=('Arial', 9))
style.map("Action.TButton",
        background=[('active', COLOR_BUTTON_ACTIVE)],
        relief=[('pressed', 'sunken')])

# Frame Input
frame_input = ttk.LabelFrame(root, text="Form Input Data Mahasiswa", padding=(10, 5))
frame_input.pack(fill=tk.X, padx=10, pady=5)

labels = ["NIM:", "Nama:", "Nilai Tugas:", "Nilai UTS:", "Nilai UAS:"]
entries = [None] * len(labels)  

for i, label in enumerate(labels):
    lbl = ttk.Label(frame_input, text=label, style="InputLabel.TLabel")
    lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5, ipadx=5, ipady=2)

    entry_widget = ttk.Entry(frame_input, width=30)
    entry_widget.grid(row=i, column=1, padx=5, pady=5, sticky=tk.W)
    entry_widget.bind("<Return>", focus_next_widget)
    entries[i] = entry_widget

entry_nim, entry_nama, entry_tugas, entry_uts, entry_uas = entries

btn_frame = ttk.Frame(frame_input)
btn_frame.grid(row=0, column=2, rowspan=5, padx=20)

btn_simpan = ttk.Button(btn_frame, text="Simpan Data", width=15, style="Action.TButton", command=save_data)
btn_simpan.pack(pady=5)

btn_hapus = ttk.Button(btn_frame, text="Hapus Data", width=15, style="Action.TButton", command=delete_data)
btn_hapus.pack(pady=5)

# Frame Tools
frame_tools = ttk.Frame(root)
frame_tools.pack(fill=tk.X, padx=10, pady=5)

frame_cari = ttk.LabelFrame(frame_tools, text="Pencarian Data", padding=(10, 5))
frame_cari.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

ttk.Label(frame_cari, text="Cari (NIM/Nama):").pack(side=tk.LEFT, padx=5)
entry_cari = ttk.Entry(frame_cari, width=30)
entry_cari.pack(side=tk.LEFT, padx=5)
entry_cari.bind("<Return>", lambda e: on_cari())  
btn_cari = ttk.Button(frame_cari, text="Cari", width=10, command=on_cari)
btn_cari.pack(side=tk.LEFT, padx=5)

frame_sort = ttk.LabelFrame(frame_tools, text="Pengurutan Data", padding=(10, 5))
frame_sort.pack(side=tk.LEFT, fill=tk.X, expand=True)

ttk.Label(frame_sort, text="Berdasarkan Nilai Akhir :").pack(side=tk.LEFT, padx=5)

var_sort_order = tk.IntVar()
rb_asc = ttk.Radiobutton(frame_sort, text="Asc", variable=var_sort_order, value=1)
rb_asc.pack(side=tk.LEFT, padx=5)
rb_desc = ttk.Radiobutton(frame_sort, text="Desc", variable=var_sort_order, value=0)
rb_desc.pack(side=tk.LEFT, padx=5)
var_sort_order.set(0)  

btn_sort = ttk.Button(frame_sort, text="Urutkan", width=10, command=on_sort)
btn_sort.pack(side=tk.LEFT, padx=5)

frame_extra = ttk.LabelFrame(frame_tools, text="Fitur", padding=(10, 5))
frame_extra.pack(side=tk.LEFT, padx=(10, 0))

btn_export = ttk.Button(frame_extra, text="Ekspor CSV", width=12, command=on_export)
btn_export.pack(side=tk.LEFT, padx=5)

btn_import = ttk.Button(frame_extra, text="Impor CSV", width=12, command=on_import)
btn_import.pack(side=tk.LEFT, padx=5)

btn_stat = ttk.Button(frame_extra, text="Lihat Statistik", width=15, command=show_statistik)
btn_stat.pack(side=tk.LEFT, padx=5)

# Frame Tabel
frame_tabel = ttk.Frame(root)
frame_tabel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

columns = ("no", "nim", "nama", "tugas", "uts", "uas", "nilai_akhir", "kategori")
tabel = ttk.Treeview(frame_tabel, columns=columns, show="headings", height=15)

tabel.heading("no", text="No")
tabel.heading("nim", text="NIM")
tabel.heading("nama", text="Nama Mahasiswa")
tabel.heading("tugas", text="Tugas (30%)")
tabel.heading("uts", text="UTS (30%)")
tabel.heading("uas", text="UAS (40%)")
tabel.heading("nilai_akhir", text="Nilai Akhir")
tabel.heading("kategori", text="Kategori Nilai")

tabel.column("no", width=40, anchor=tk.CENTER)
tabel.column("nim", width=100, anchor=tk.CENTER)
tabel.column("nama", width=200)
tabel.column("tugas", width=80, anchor=tk.CENTER)
tabel.column("uts", width=80, anchor=tk.CENTER)
tabel.column("uas", width=80, anchor=tk.CENTER)
tabel.column("nilai_akhir", width=100, anchor=tk.CENTER)
tabel.column("kategori", width=150, anchor=tk.CENTER)

tabel.bind("<<TreeviewSelect>>", on_table_select)

scrollbar = ttk.Scrollbar(frame_tabel, orient=tk.VERTICAL, command=tabel.yview)
tabel.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tabel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Status Bar dan Footer
status_bar = ttk.Label(root, 
                    text="Siap | Jumlah Data: 0", 
                    relief=tk.SUNKEN, 
                    anchor=tk.W,
                    background=COLOR_STATUS_BAR,
                    foreground=COLOR_TEXT,
                    font=('Arial', 9))
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

footer = ttk.Label(root, 
                text="Aplikasi Manajemen Nilai Mahasiswa by Kelompok 8 © 2025", 
                foreground="#666666",
                background=COLOR_PRIMARY,
                font=('Arial', 9))
footer.pack(side=tk.BOTTOM, pady=5)

def update_status():
    count = sum(1 for mhs in data_mahasiswa if mhs is not None)
    status_bar.config(text=f"Siap | Jumlah Data: {count}")
    root.after(1000, update_status)  

update_status()
    
refresh_tabel()
root.mainloop()
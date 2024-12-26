import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd


class aplikasiNaiveBayesKelompok1:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Prediksi Kenaikan Jabatan (kelompok1)")
        self.root.resizable(False, False)

        # Frame untuk tabel (kiri)
        self.frame_table = tk.Frame(self.root)
        self.frame_table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Frame untuk tombol (kanan)
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.grid(row=0, column=1, padx=10, pady=40, sticky="nsew")

        # Label untuk judul tabel
        self.label_table_title = tk.Label(self.frame_table, text="", font=("Arial", 14, "bold"))
        self.label_table_title.pack(pady=5)
        
        self.tree_scroll = tk.Scrollbar(self.frame_table)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Tabel untuk menampilkan data
        self.tree = ttk.Treeview(
            self.frame_table,
            columns=("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9", "#10"),
            show="headings",height=20,yscrollcommand=self.tree_scroll.set
        )
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Konfigurasi style header tabel
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Kolom pada tabel
        columns = ["Nama", "NIK", "Jenis Kelamin", "Lama Bekerja", "Kualitas Kerja",
                "Perilaku", "Absensi", "Naik Jabatan", "Prediksi", "Hasil"]
        for i, col in enumerate(columns):
            self.tree.heading(f"#{i+1}", text=col, anchor="center")
            self.tree.column(f"#{i+1}", width=100, anchor=tk.W)

        # Tombol pada frame kanan
        self.btn_load = tk.Button(self.frame_buttons, text="Masukkan Dataset", command=self.load_dataset,width=20)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5,ipadx=30, ipady=10)

        self.btn_show_training = tk.Button(self.frame_buttons, text="Tampilkan Data Training", command=self.show_training_data, state=tk.DISABLED,width=20)
        self.btn_show_training.grid(row=1, column=0, padx=5, pady=5,ipadx=30)

        self.btn_show_testing = tk.Button(self.frame_buttons, text="Tampilkan Data Testing", command=self.show_testing_data, state=tk.DISABLED,width=20)
        self.btn_show_testing.grid(row=2, column=0, padx=5, pady=5,ipadx=30)
        
        self.info_frame = tk.Frame(self.frame_buttons)
        self.info_frame.grid(row=3, column=0, padx=5, pady=10)

        # Menambahkan tabel untuk informasi
        self.info_tree_scroll = tk.Scrollbar(self.info_frame)
        self.info_tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_tree = ttk.Treeview(self.info_frame, columns=("Info", "Value"), show="headings", height=5,yscrollcommand=self.tree_scroll.set)
        self.info_tree.pack(fill=tk.BOTH, expand=True)

        self.info_tree.heading("Info", text="Info")
        self.info_tree.heading("Value", text="Value")

        # Mengatur lebar kolom
        self.info_tree.column("Info", width=150, anchor="w")
        self.info_tree.column("Value", width=50, anchor="center")
        
        self.btn_predict = tk.Button(self.frame_buttons, text="Prediksi", command=self.run_prediction, state=tk.DISABLED,width=20)
        self.btn_predict.grid(row=4, column=0, padx=5, pady=5,ipady=5,ipadx=30)

        self.btn_show_probabilities = tk.Button(self.frame_buttons, text="Tampilkan Probabilitas", command=self.show_probabilities, state=tk.DISABLED,width=20)
        self.btn_show_probabilities.grid(row=5, column=0, padx=5, pady=5,ipady=5,ipadx=30)

        # Konfigurasi warna latar belakang baris tabel
        self.tree.tag_configure("even", background="lightblue")
        self.tree.tag_configure("odd", background="lightcyan")
        
        self.tree_scroll.config(command=self.tree.yview)
        self.info_tree_scroll.config(command=self.info_tree.yview)

    def load_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path, sep=',', encoding='utf-8')
                required_columns = ["Nama", "NIK", "Jenis Kelamin", "Lama Bekerja", 
                                    "Kualitas Kerja", "Perilaku", "Absensi", "Naik Jabatan"]
                missing_columns = [col for col in required_columns if col not in self.df.columns]

                if missing_columns:
                    raise ValueError(f"Dataset membutuhkan kolom: {', '.join(missing_columns)}")

                self.df_training = self.df.iloc[:84]
                self.df_testing = self.df.iloc[84:].copy()

                messagebox.showinfo("Mantap", "Dataset berhasil dimuat!!")
                self.btn_predict.config(state=tk.NORMAL)
                self.btn_show_training.config(state=tk.NORMAL)
                self.btn_show_testing.config(state=tk.NORMAL)
                self.btn_show_probabilities.config(state=tk.NORMAL)
                
                self.update_info_table()
                
            except Exception as e:
                messagebox.showerror("Waduh", f"Dataset gagal dimuat: {e}")
                
    def update_info_table(self):
        # Menghitung jumlah baris dan kolom pada data training dan testing
        training_rows, training_cols = self.df_training.shape
        testing_rows, testing_cols = self.df_testing.shape

        # Cek data kosong dan duplikat
        duplicate_data_training = self.df_training.duplicated().sum()
        duplicate_data_testing = self.df_testing.duplicated().sum()

        # Mengupdate tabel info dengan informasi yang dihitung
        self.info_tree.delete(*self.info_tree.get_children())
        self.info_tree.insert("", tk.END, values=("Data Training", f"{training_rows}"))
        self.info_tree.insert("", tk.END, values=("Data Testing", f"{testing_rows}"))
        self.info_tree.insert("", tk.END, values=("Data Duplikat (Training)", f"{duplicate_data_training}"))
        self.info_tree.insert("", tk.END, values=("Data Duplikat(Testing)", f"{duplicate_data_testing}"))

    def run_prediction(self):
        try:
            target_column = "Naik Jabatan"
            feature_columns = ["Lama Bekerja", "Kualitas Kerja", "Perilaku", "Absensi"]

            total_data = len(self.df_training)
            prob_yes_total = len(self.df_training[self.df_training[target_column] == "Ya"]) / total_data
            prob_no_total = len(self.df_training[self.df_training[target_column] == "Tidak"]) / total_data

            data_ya = self.df_training[self.df_training[target_column] == "Ya"]
            data_tidak = self.df_training[self.df_training[target_column] == "Tidak"]

            probabilities = {}
            for feature in feature_columns:
                unique_values = self.df_training[feature].unique()
                for value in unique_values:
                    probabilities[f"P({feature}={value}|Ya)"] = (len(data_ya[data_ya[feature] == value]) + 1) / (len(data_ya) + len(unique_values))
                    probabilities[f"P({feature}={value}|Tidak)"] = (len(data_tidak[data_tidak[feature] == value]) + 1) / (len(data_tidak) + len(unique_values))

            def predict_naive_bayes(row):
                prob_yes = prob_yes_total
                prob_no = prob_no_total

                for feature in feature_columns:
                    value = row[feature]
                    prob_yes *= probabilities.get(f"P({feature}={value}|Ya)", 1 / (len(data_ya) + len(self.df_training[feature].unique())))
                    prob_no *= probabilities.get(f"P({feature}={value}|Tidak)", 1 / (len(data_tidak) + len(self.df_training[feature].unique())))

                return "Ya" if prob_yes > prob_no else "Tidak"

            self.df_testing["prediksi"] = self.df_testing.apply(predict_naive_bayes, axis=1)
            self.df_testing["akurasi"] = self.df_testing["prediksi"] == self.df_testing[target_column]
            self.df_testing["hasil"] = self.df_testing["akurasi"].apply(lambda x: "Akurat" if x else "Tidak Akurat")

            
            self.label_table_title.config(text="Hasil Prediksi")
            
            for row in self.tree.get_children():
                self.tree.delete(row)

            for i, (_, row) in enumerate(self.df_testing.iterrows()):
                row_tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert("", tk.END, values=(
                    row["Nama"], row["NIK"], row["Jenis Kelamin"], row["Lama Bekerja"], 
                    row["Kualitas Kerja"], row["Perilaku"], row["Absensi"], 
                    row[target_column], row["prediksi"], row["hasil"]
                ), tags=(row_tag,))

            messagebox.showinfo("Berhasil", "Prediksi berhasil")
        except Exception as e:
            messagebox.showerror("Waduh", f"Prediksi gagal dilakukan: {e}")

    def show_training_data(self):
        self.label_table_title.config(text="Data Training")
        self.show_data(self.df_training)

    def show_testing_data(self):
        self.label_table_title.config(text="Data Testing")
        self.show_data(self.df_testing)

    def show_data(self, data):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, (_, row) in enumerate(data.iterrows()):
            row_tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=(
                row["Nama"], row["NIK"], row["Jenis Kelamin"], row["Lama Bekerja"], 
                row["Kualitas Kerja"], row["Perilaku"], row["Absensi"], row["Naik Jabatan"]
            ), tags=(row_tag,))

    def show_probabilities(self):
        prob_window = tk.Toplevel(self.root)
        prob_window.title("Feature Probabilities")

        tree = ttk.Treeview(prob_window, columns=("Feature", "Value", "P(Yes)", "P(No)"), show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        tree.heading("Feature", text="Feature")
        tree.heading("Value", text="Value")
        tree.heading("P(Yes)", text="P(Yes)")
        tree.heading("P(No)", text="P(No)")

        for feature in ["Lama Bekerja", "Kualitas Kerja", "Perilaku", "Absensi"]:
            unique_values = self.df_training[feature].unique()
            for value in unique_values:
                p_yes = (len(self.df_training[(self.df_training[feature] == value) & (self.df_training["Naik Jabatan"] == "Ya")]) + 1) / (len(self.df_training[self.df_training["Naik Jabatan"] == "Ya"]) + len(unique_values))
                p_no = (len(self.df_training[(self.df_training[feature] == value) & (self.df_training["Naik Jabatan"] == "Tidak")]) + 1) / (len(self.df_training[self.df_training["Naik Jabatan"] == "Tidak"]) + len(unique_values))
                tree.insert("", tk.END, values=(feature, value, p_yes, p_no))


if __name__ == "__main__":
    root = tk.Tk()
    app = aplikasiNaiveBayesKelompok1(root)
    root.mainloop()

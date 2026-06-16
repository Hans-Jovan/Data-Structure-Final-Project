import tkinter as tk
import os
import math

CANVAS_W, CANVAS_H = 500, 500
SIDEBAR_W = 250
NODE_R, HIT_R = 8, 12
NODE2_R, HIT2_R = 4, 6
MAP_PATH = "C:/Users/Hans/PycharmProjects/5024241005_Hans Jovan/.venv/MAPS1.png"


########============= DJIKKKSTRAAAAHAHHHHHHAHAHAHAHAH =================##########
class Node:
    def __init__(self, nama_node):
        self.nama_node = nama_node
        self.Next = []
        self.W = 9999999999999999
        self.asal = None


Lnode = []


def CariNode(namaNode):
    global Lnode
    for node in Lnode:
        if node.nama_node == namaNode:
            return node
    return None


def DjikStra(namaNode, Jarak, titik_awal=None):
    n = CariNode(namaNode)
    if n.W <= Jarak:
        return
    n.W = Jarak
    n.asal = titik_awal
    for NodeNext in n.Next:
        DjikStra(NodeNext[0], NodeNext[1] + Jarak, n)


########============= TNKIKERBELL=================##########
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Credit : Rahmat")
        self.geometry(f"{CANVAS_W}x{CANVAS_H + SIDEBAR_W}")
        # default node format: (x, y, tipe) but we keep compatibility if some entries are (x,y)
        self.nodes = [(1, 1, "besar")]
        self.mode = "add"

        # --- Kanvas ---
        # --- Frame utama: canvas di kiri, sidebar di kanan ---
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # --- Kanvas (kiri) ---
        self.canvas = tk.Canvas(main_frame, width=CANVAS_W, height=CANVAS_H, bg="pink")
        self.canvas.pack(side="left", fill="both", expand=True)

        # --- Sidebar (kanan) ---
        frame = tk.Frame(main_frame, width=SIDEBAR_W, padx=10, pady=10)
        frame.pack(side="right", fill="y")
        frame.pack_propagate(False)  # mencegah sidebar mengecil

        # 3x2 matrix buttons
        tombol = [
            ("Add Node Besar", lambda: self.set_mode("add")),
            ("Add Node Kecil", lambda: self.set_mode("add2")),
            ("Delete Node", lambda: self.set_mode("del")),
            ("Sambung", lambda: self.set_mode("con")),
            ("Delete Sambungan", lambda :self.set_mode("del_line")),
            ("Djikstra", lambda: self.set_mode("djk")),
            ("SIMPAN MAP", self.simpan_map),
            ("Clear MAP", self.clear_map)
        ]

        # buat grid 3 baris x 2 kolom
        for i, (label, cmd) in enumerate(tombol):
            r = i // 2
            c = i % 2
            tk.Button(frame, text=label, command=cmd, width=16).grid(row=r, column=c, padx=5, pady=5)

        self.info = tk.Label(frame, text="mode node ")
        self.info.grid(row=3, column=0, columnspan=2, pady=10)

        # --- Event ---
        self.canvas.bind("<Button-1>", self.on_click)

        self.sambungan = []
        self.djk_terpilih = None
        self.jalur = []
        # load image if exists; if not, ignore to avoid crash
        try:
            self.bg_img = tk.PhotoImage(file=MAP_PATH)
        except Exception:
            self.bg_img = None

    def jarak_titik_ke_garis(self, px, py, x1, y1, x2, y2):
        # panjang garis
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)

        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))

        cx = x1 + t * dx
        cy = y1 + t * dy

        return math.sqrt((px - cx) ** 2 + (py - cy) ** 2)

    def set_mode(self, m):
        self.mode = m
        self.update_info()

    def update_info(self):
        self.info.config(text=f"mode {self.mode} node {len(self.nodes)}")

    def on_click(self, e):
        if self.mode == "add":
            self.add_node(e.x, e.y)
        if self.mode == "add2":
            self.add_node2(e.x, e.y)
        if self.mode == "del":
            self.del_node(e.x, e.y)
        if self.mode == "con":
            self.con_node(e.x, e.y)
        if self.mode == "del_line":
            self.del_line(e.x,e.y)
        if self.mode == "djk":
            self.djk_node(e.x, e.y)
        if self.mode == "smpn":
            self.simpan_map()
        self.update_info()

    def add_node(self, x, y):
        # simpan tipe sebagai "besar"
        self.nodes.append((x, y, "besar"))
        self.canvas.create_oval(x - NODE_R, y - NODE_R, x + NODE_R, y + NODE_R, fill="red", outline="black")

    def add_node2(self, x, y):
        # simpan tipe sebagai "kecil"
        self.nodes.append((x, y, "kecil"))
        self.canvas.create_oval(x - NODE2_R, y - NODE2_R, x + NODE2_R, y + NODE2_R, fill="yellow", outline="black")

    # helper untuk mendapatkan komponen node secara aman (kompatibel format lama)
    def _node_components(self, node):
        # node bisa (x,y) atau (x,y,tipe)
        if len(node) >= 3:
            return node[0], node[1], node[2]
        else:
            return node[0], node[1], "besar"

    def del_node(self, x, y):
        for i, node in enumerate(self.nodes):
            px, py, tipe = self._node_components(node)
            if (x - px) ** 2 + (y - py) ** 2 <= HIT_R ** 2:
                self.nodes.pop(i)
                sambungan_baru = []
                for a, b in self.sambungan:
                    if a != i and b != i:
                        sambungan_baru.append((a, b))
                self.sambungan = sambungan_baru
                sambungan_final = []
                for a, b in sambungan_baru:
                    if a > i:
                        new_a = a - 1
                    else:
                        new_a = a
                    if b > i:
                        new_b = b - 1
                    else:
                        new_b = b
                    sambungan_final.append((new_a, new_b))
                self.sambungan = sambungan_final
                self.canvas.delete("all")
                self.redraw()
                break

    def con_node(self, x, y):
        indeks_terklik = None
        for i, node in enumerate(self.nodes):
            px, py, tipe = self._node_components(node)
            if (x - px) ** 2 + (y - py) ** 2 <= HIT_R ** 2:
                indeks_terklik = i
                print("terpencet indek :", i)
                break

        if indeks_terklik is not None:
            if self.djk_terpilih is None:
                self.djk_terpilih = indeks_terklik
            else:
                if self.djk_terpilih != indeks_terklik:
                    garis_baru = (min(self.djk_terpilih, indeks_terklik),
                                  max(self.djk_terpilih, indeks_terklik))
                    if garis_baru not in self.sambungan:
                        self.sambungan.append(garis_baru)
                        x1, y1, _ = self._node_components(self.nodes[self.djk_terpilih])
                        x2, y2, _ = self._node_components(self.nodes[indeks_terklik])
                        jarak = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                        print("jarak setelah connect :", jarak)
                else:
                    print("lu ngapain ngeklik node yang sama")
                self.djk_terpilih = None
                print("selected node jadi none")
            self.canvas.delete("all")
            self.redraw()

    def del_line(self, x, y):
        TOL = 6  # toleransi klik ke garis

        for i, (a, b) in enumerate(self.sambungan):
            x1, y1, _ = self._node_components(self.nodes[a])
            x2, y2, _ = self._node_components(self.nodes[b])

            jarak = self.jarak_titik_ke_garis(x, y, x1, y1, x2, y2)

            if jarak <= TOL:
                print(f"Garis {a}-{b} dihapus")
                self.sambungan.pop(i)
                self.canvas.delete("all")
                self.redraw()
                return

    def redraw(self):
        self.canvas.delete("all")
        if self.bg_img:
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        for a, b in self.sambungan:
            x1, y1, _ = self._node_components(self.nodes[a])
            x2, y2, _ = self._node_components(self.nodes[b])
            self.canvas.create_line(x1, y1, x2, y2, fill="lime", width=2)

        for node in self.nodes:
            x, y, tipe = self._node_components(node)
            # terima "besar" / "kecil" (bahasa indonesia)
            if tipe == "besar" or tipe == "big":
                r = NODE_R
                warna = "red"
            else:
                r = NODE2_R
                warna = "yellow"

            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=warna, outline="black")

    def clear_map(self):
        self.nodes = []
        self.sambungan = []
        self.djk_terpilih = None
        self.jalur = []
        self.canvas.delete("all")
        self.redraw()

    ########============= DJIKKKSTRAAAAHAHHHHHHAHAHAHAHAH =================#########
    def djk_node(self, x, y):
        indeks_terklik = None
        for i, node in enumerate(self.nodes):
            px, py, tipe = self._node_components(node)
            if (x - px) ** 2 + (y - py) ** 2 <= HIT_R ** 2:
                indeks_terklik = i
                print("terpencet indek untuk djikstat:", i)
                break
        global Lnode
        Lnode = []

        if indeks_terklik is not None:
            if self.djk_terpilih is None:
                self.djk_terpilih = indeks_terklik
                self.jalur = []
                self.redraw()
            else:
                if self.djk_terpilih != indeks_terklik:
                    for i in range(len(self.nodes)):
                        node_baru = Node(nama_node=i)
                        Lnode.append(node_baru)

                    for a, b in self.sambungan:
                        node_a = CariNode(a)
                        node_b = CariNode(b)

                        x1, y1, _ = self._node_components(self.nodes[a])
                        x2, y2, _ = self._node_components(self.nodes[b])
                        jarak = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

                        node_a.Next.append([b, jarak])
                        node_b.Next.append([a, jarak])

                    DjikStra(self.djk_terpilih, 0, None)

                    tujuan_akhir = CariNode(indeks_terklik)

                    if tujuan_akhir.W >= 999999999:
                        print("gaada jalan yg tersambung")
                    else:
                        print(f"jarak terpendek : ", tujuan_akhir.W)

                        self.jalur_hasil = []
                        curr = tujuan_akhir
                        while curr is not None:
                            self.jalur_hasil.append(curr.nama_node)
                            curr = curr.asal

                            # gambar jalur oranye
                            for i in range(len(self.jalur_hasil) - 1):
                                a = self.jalur_hasil[i]
                                b = self.jalur_hasil[i + 1]
                                x1, y1, _ = self._node_components(self.nodes[a])
                                x2, y2, _ = self._node_components(self.nodes[b])
                                self.canvas.create_line(x1, y1, x2, y2, fill="orange", width=3)


                else:
                    print("lu ngapain ngeklik node yang sama")
                self.djk_terpilih = None
                print("selected node jadi none")
            self.canvas.delete("all")
            self.redraw()
        # --- GAMBAR JALUR DI CANVAS (TAMBAHAN BARU) ---
        # Hapus jalur lama
        if hasattr(self, "garis_jalur"):
            for g in self.garis_jalur:
                self.canvas.delete(g)

        self.garis_jalur = []

        # Gambar jalur baru warna oranye
        if hasattr(self, "jalur_hasil"):
            for i in range(len(self.jalur_hasil) - 1):
                a = self.jalur_hasil[i]
                b = self.jalur_hasil[i + 1]

                x1, y1, _ = self._node_components(self.nodes[a])
                x2, y2, _ = self._node_components(self.nodes[b])

                garis = self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill="orange",
                    width=3,
                    smooth=True,  # BIAR MELIUK-LIUK
                    splinesteps=20  # SEMAKIN BESAR SEMAKIN HALUS
                )
                self.garis_jalur.append(garis)

    ########============= SASAAFEEE FILELEEEE=================##########
    def simpan_map(self):
        file_path = "C:/Users/Hans/PycharmProjects/5024241005_Hans Jovan/contoh1.txt"
        print("TOMBOL KEPENCET")

        try:
            with open(file_path, "w") as file:
                file.write("Node :\n")
                # simpan dalam format x,y,tipe agar konsisten
                for node in self.nodes:
                    x, y, tipe = self._node_components(node)
                    file.write(f"{x},{y},{tipe}\n")
                file.write("Sambungan :\n")
                for a, b in self.sambungan:
                    file.write(f"{a},{b}\n")

            print(f"AKHIRNYA TERSIMPANNNAS FASFDASONFJF: {file_path}")

        except Exception as e:
            print("idk error or sum", e)

    def buka_map(self):
        file_path = "C:/Users/Hans/PycharmProjects/5024241005_Hans Jovan/contoh1.txt"
        try:
            self.nodes = []
            self.sambungan = []
            self.djk_terpilih = None
            self.jalur = []

            mode_baca = ""

            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip()

                    if line == "Node :":
                        mode_baca = "node"
                        continue
                    elif line == "Sambungan :":
                        mode_baca = "sambungan"
                        continue

                    if not line:
                        continue

                    if mode_baca == "node":
                        data = line.split(",")
                        # dukungan backward: jika format lama hanya x,y -> default 'besar'
                        x = int(data[0])
                        y = int(data[1])
                        tipe = data[2] if len(data) >= 3 else "besar"
                        self.nodes.append((x, y, tipe))

                    elif mode_baca == "sambungan":
                        data = line.split(",")
                        a = int(data[0])
                        b = int(data[1])
                        self.sambungan.append((a, b))

            self.redraw()
            print("KELAR MEMBACA BOSQQQQ")

        except Exception as e:
            print("idk error or sum", e)


if __name__ == "__main__":
    print("BUKA PEMBACAAN DLUAN")
    app = App()
    # Jika file ada, buka; jika tidak ada, ignore
    try:
        app.buka_map()
    except Exception:
        pass
    print("BUKA YANG GAADA LOADING")
    app.mainloop()

##========= TO-DO MINGDEP ===========#####
### djikstra cuma cari jarak dari dua node
### bisa buat save save an

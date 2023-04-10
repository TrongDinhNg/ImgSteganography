import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from en_decrypt import Encrypt_Decrypt

class App:
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        master.title("Tkinter App")
        master.geometry("800x600")
        
        # tạo menu
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        master.config(menu=menubar)
        
        # tạo thanh sidebar
        sidebar = tk.Frame(master, bg="gray", width=100)
        sidebar.pack(side="left", fill="y")
        home_button = tk.Button(sidebar, text="Home", command=self.show_home)
        home_button.pack(pady=10)
        page1_button = tk.Button(sidebar, text="Page 1", command=self.show_page1)
        page1_button.pack(pady=10)
        page2_button = tk.Button(sidebar, text="Page 2", command=self.show_page2)
        page2_button.pack(pady=10)

        
        # tạo trang Home
        self.home_frame = tk.Frame(self.master)

        home_label = tk.Label(
            self.home_frame, text="Chào mừng đến với ứng dụng giấu tin trong ảnh số!")
        home_label.pack(pady=10)
        

        # tạo trang Page 1
        self.page1_frame = tk.LabelFrame(master, text="Trang 1", font=("Arial", 24), width=500, height=500)
        self.page1_frame.pack(fill='both', padx=10, pady=10)
        
        # tạo nút mở ảnh
        open_image_button = tk.Button(self.page1_frame, text="Mở ảnh", command=self.open_image1)
        open_image_button.pack(pady=10)
        # tạo một canvas để hiển thị ảnh
        self.canvas1 = tk.Canvas(self.page1_frame, width=200, height=200,background="red")
        self.canvas1.place(x=70,y=50)

        #canvas hiển thị ảnh đã giấu tin
        self.canvas2 = tk.Canvas(self.page1_frame, width=200, height=200,background="blue")
        self.canvas2.place(x=450,y=50)

        # tạo nội dung cho phần Encrypt
        self.encrypt_content = tk.LabelFrame(self.page1_frame, text="Encrypt", font=("Arial", 18), width=300, height=300)
        self.encrypt_content.place(x=0,y=250,relwidth=1)
        
        #lấy giao diện encrypt từ file en_decrypt.py để đưa vào self.encrypt_content
        encrypt = Encrypt_Decrypt(self.encrypt_content)
        encrypt.show_encrypt()

        #tạo button giấu tin vào hình ảnh
        self.encrypt_button = tk.Button(self.page1_frame, text="Giấu tin", command=self.encrypt)
        self.encrypt_button.place(x=350,y=250)



        # tạo trang Page 2
        self.page2_frame = tk.LabelFrame(master, text="Trang 2", font=("Arial", 24), width=500, height=500)
        self.page2_frame.pack(fill="both", padx=10, pady=10)
        # tạo nút mở ảnh
        open_image_button = tk.Button(self.page2_frame, text="Mở ảnh có giấu tin", command=self.open_image2)
        open_image_button.pack(pady=10)
        # tạo một canvas để hiển thị ảnh
        self.canvas3 = tk.Canvas(self.page2_frame, width=200, height=200,background="blue")
        self.canvas3.pack()
        # Gắn sự kiện resize vào khung ứng dụng
        # self.master.bind("<Configure>", self.resize_image)
        self.image = None  # Ảnh sẽ được hiển thị trên canvas
       
        # tạo nội dung cho phần Decrypt
        self.decrypt_content = tk.LabelFrame(self.page2_frame, text="Decrypt", font=("Arial", 18), width=300, height=300)
        self.decrypt_content.place(x=0,y=250,relwidth=1)

        #lấy giao diện decrypt từ file en_decrypt.py để đưa vào self.decrypt_content
        decrypt = Encrypt_Decrypt(self.decrypt_content)
        decrypt.show_decrypt()

        #tạo button lấy tin từ hình ảnh
        self.decrypt_button = tk.Button(self.page2_frame, text="Lấy tin", command=self.decrypt)
        self.decrypt_button.place(x=350,y=250)
    
    
    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(fill="both", expand=True)
        
    def show_page1(self):
        self.hide_all_frames()
        self.page1_frame.pack(fill="both", expand=True)
        
    def show_page2(self):
        self.hide_all_frames()
        self.page2_frame.pack(fill="both", expand=True)
        
     # Ẩn các frame
    def hide_all_frames(self):
        self.home_frame.pack_forget()
        self.page1_frame.pack_forget()
        self.page2_frame.pack_forget()

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def open_image1(self):
        # hiển thị hộp thoại chọn file
        file_path = filedialog.askopenfilename()
        # nếu người dùng đã chọn một file
        if file_path:
            # mở file ảnh và tạo một đối tượng Image
            image = Image.open(file_path)
            #lưu bản sao ảnh gốc vào thư mục image
            image.save("image/origin_image.png")

            # tính tỷ lệ mới cho ảnh
            width, height = image.size
            ratio = min(200/width, 200/height)
            # tính kích thước mới cho ảnh
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            # điều chỉnh kích thước ảnh
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            # cắt bớt phần của ảnh để tạo ra một ảnh có kích thước mong muốn
            x = (new_width - 200) / 2
            y = (new_height - 200) / 2
            image = image.crop((x, y, x+200, y+200))
            # tạo một đối tượng ImageTk từ Image
            photo = ImageTk.PhotoImage(image)
            # hiển thị ảnh trên canvas
            self.canvas1.create_image(0, 0, image=photo, anchor=tk.NW)
            # giữ một tham chiếu đến ảnh để ngăn việc ảnh bị xóa bởi garbage collector
            self.canvas1.image = photo

    def open_image2(self):
        # hiển thị hộp thoại chọn file
        file_path = filedialog.askopenfilename()
        # nếu người dùng đã chọn một file
        if file_path:
            # mở file ảnh và tạo một đối tượng Image
            image = Image.open(file_path)
            # tính tỷ lệ mới cho ảnh
            width, height = image.size
            ratio = min(200/width, 200/height)
            # tính kích thước mới cho ảnh
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            # điều chỉnh kích thước ảnh
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            # cắt bớt phần của ảnh để tạo ra một ảnh có kích thước mong muốn
            x = (new_width - 200) / 2
            y = (new_height - 200) / 2
            image = image.crop((x, y, x+200, y+200))
            # tạo một đối tượng ImageTk từ Image
            photo = ImageTk.PhotoImage(image)
            # hiển thị ảnh trên canvas
            self.canvas3.create_image(0, 0, image=photo, anchor=tk.NW)
            # giữ một tham chiếu đến ảnh để ngăn việc ảnh bị xóa bởi garbage collector
            self.canvas3.image = photo

    

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.show_home()
    root.mainloop()
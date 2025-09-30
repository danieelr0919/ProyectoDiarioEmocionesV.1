import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
import re
from PIL import Image, ImageTk
import os


# ----------------------------------------
# CLASE PRINCIPAL: DiarioEmocionesApp
# ----------------------------------------
class DiarioEmocionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diario de Emociones 🧠❤️")
        self.root.geometry("1000x800")
        self.root.configure(bg="#faf3e0")

        self.configurar_favicon()


        # Conexión a MySQL
        self.conn = self.crear_conexion_mysql()

        # Configurar estilo
        self.configurar_estilo()

        # Crear interfaz modular
        self.crear_notebook()
        self.crear_pestañas()
        self.crear_footer()

    def configurar_favicon(self):
        try:

            self.root.iconbitmap("favicon.ico")
            print("✅ Favicon ICO cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando favicon ICO: {e}")


    def crear_conexion_mysql(self):
        try:
            conexion = mysql.connector.connect(
                host='localhost',
                database='diario_emociones',
                user='root',
                password=''  # Cambia si usas contraseña
            )
            if conexion.is_connected():
                print("✅ Conexión a base de datos exitosa")
                return conexion
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#faf3e0")
        style.configure("TNotebook.Tab",
                        background="#e0d3c1",
                        foreground="#5a4a42",
                        font=("Arial", 11, "bold"),
                        padding=[12, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", "#d4a5a5")],
                  foreground=[("selected", "white")])

        # Estilo para Treeview (tablas)
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#5a4a42",
                        rowheight=25,
                        fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                        background="#d4a5a5",
                        foreground="white",
                        font=("Arial", 10, "bold"))
        style.map("Treeview",
                  background=[('selected', '#e77f67')])

    def crear_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

    def crear_pestañas(self):
        # Módulo 1: Usuarios
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_usuarios, text=" 👤 Usuarios ")
        self.crear_formulario_usuarios()

        # Módulo 2: Emociones
        self.tab_emociones = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_emociones, text=" 😊 Emociones ")
        self.crear_formulario_emociones()

        # Módulo 3: Entradas
        self.tab_entradas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_entradas, text=" 📖 Entradas ")
        self.crear_formulario_entradas()

        # Módulo 4: Reportes
        self.tab_reportes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reportes, text=" 📈 Reportes ")
        self.crear_formulario_reportes()

    # -------- VALIDACIONES DE LOS CAMPOS ----------
    def validar_id_usuario(self):
        user_id = self.usuario_id_entry.get()
        if user_id and not user_id.isdigit():
            messagebox.showerror("Error", "ID Usuario debe ser un número")
            return False
        return True

    def validar_id_emocion(self):
        emocion = self.emocion_id_entry.get()
        if emocion and not emocion.isdigit():
            messagebox.showerror("Error", "ID Emoción debe ser un número")
            return False
        return True

    def validar_id_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if entrada_id and not entrada_id.isdigit():
            messagebox.showerror("Error", "ID Entrada debe ser un número")
            return False
        return True

    def validar_usuario_id_entrada(self):
        usuario_id = self.entrada_usuario_id_entry.get()
        if usuario_id and not usuario_id.isdigit():
            messagebox.showerror("Error", "ID Usuario en Entradas debe ser un número")
            return False
        return True

    # ---------- VALIDACIONES DE TEXTO --------------
    def validar_texto_username(self, texto):
        if not texto:
            messagebox.showerror("Error", "Username es obligatorio")
            return False
        if not (3 <= len(texto) <= 50):
            messagebox.showerror("Error", "Username debe tener entre 3 y 50 caracteres")
            return False
        return True

    def validar_texto_nombre_emocion(self, texto):
        if not texto:
            messagebox.showerror("Error", "Nombre de la emoción es obligatorio")
            return False
        if not (1 <= len(texto) <= 50):
            messagebox.showerror("Error", "Nombre debe tener entre 1 y 50 caracteres")
            return False
        return True

    def validar_texto_password(self, texto):
        if not texto:
            messagebox.showerror("Error", "Password es obligatoria")
            return False
        if len(texto) < 6:
            messagebox.showerror("Error", "Password debe tener al menos 6 caracteres")
            return False
        return True

    def validar_entrada(self, texto):
        if not texto or texto.strip() == "":
            messagebox.showerror("Error", "El texto de la entrada es obligatorio")
            return False
        return True

    # -------- VALIDACIONES DE EMAIL---------
    def validar_email_usuario(self, email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not email:
            messagebox.showerror("Error", "Email es obligatorio")
            return False
        if not re.match(patron, email):
            messagebox.showerror("Error", "Formato de email incorrecto")
            return False
        return True

    # --------- VALIDACIONES DE IMAGEN ---
    def validar_imagen(self, filepath):
        if not filepath:
            return True
        try:
            img = Image.open(filepath)
            if img.format not in ["JPEG", "PNG", "GIF"]:
                messagebox.showerror("Error", "Formato de imagen no soportado")
                return False
            if img.width > 1920 or img.height > 1080:
                messagebox.showwarning("Advertencia", "Imagen muy grande.")
                return True
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Imagen Inválida: {e}")
            return False

    # -------- FUNCION PARA SELECCIONAR IMAGEN -----------
    def seleccionar_imagen(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if filepath and self.validar_imagen(filepath):
            self.imagen_path.set(filepath)


    def seleccionar_imagen_emocion(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar imagen para la Emocion",
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]

        )
        if filepath:
            if self.validar_imagen(filepath):

                self.imagen_emocion_path.set(filepath)

    # -------- FUNCIONES PARA CARGAR DATOS EN TABLAS -----------
    def cargar_usuarios_tabla(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, username, email, creado_en FROM usuarios")
            usuarios = cursor.fetchall()

            # Limpiar tabla
            for item in self.tabla_usuarios.get_children():
                self.tabla_usuarios.delete(item)

            # Insertar datos
            for usuario in usuarios:
                self.tabla_usuarios.insert("", "end", values=usuario)
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")

    def cargar_emociones_tabla(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, nombre, emoji FROM emociones")
            emociones = cursor.fetchall()

            # Limpiar tabla
            for item in self.tabla_emociones.get_children():
                self.tabla_emociones.delete(item)

            # Insertar datos
            for emocion in emociones:
                self.tabla_emociones.insert("", "end", values=emocion)
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar emociones: {e}")

    def cargar_entradas_tabla(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT e.id, u.username, e.fecha, SUBSTRING(e.texto, 1, 50) as resumen 
                FROM entradas e 
                JOIN usuarios u ON e.usuario_id = u.id 
                ORDER BY e.fecha DESC
            """)
            entradas = cursor.fetchall()

            # Limpiar tabla
            for item in self.tabla_entradas.get_children():
                self.tabla_entradas.delete(item)

            # Insertar datos
            for entrada in entradas:
                self.tabla_entradas.insert("", "end", values=entrada)
        except Error as e:
            messagebox.showerror("Error", f"Error al cargar entradas: {e}")

    # -------- FUNCIONES PARA SELECCIONAR FILAS EN TABLAS -----------
    def seleccionar_usuario_tabla(self, event):
        selected = self.tabla_usuarios.focus()
        if selected:
            values = self.tabla_usuarios.item(selected, 'values')
            self.usuario_id_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            self.usuario_id_entry.insert(0, values[0])
            self.username_entry.insert(0, values[1])
            self.email_entry.insert(0, values[2])

    def seleccionar_emocion_tabla(self, event):
        selected = self.tabla_emociones.focus()
        if selected:
            values = self.tabla_emociones.item(selected, 'values')
            self.emocion_id_entry.delete(0, tk.END)
            self.nombre_emocion_entry.delete(0, tk.END)

            self.emocion_id_entry.insert(0, values[0])
            self.nombre_emocion_entry.insert(0, values[1])

    def seleccionar_entrada_tabla(self, event):
        selected = self.tabla_entradas.focus()
        if selected:
            values = self.tabla_entradas.item(selected, 'values')
            self.entrada_id_entry.delete(0, tk.END)
            self.entrada_id_entry.insert(0, values[0])

    # ----------------------------------------
    # MÓDULO 1: USUARIOS
    # ----------------------------------------
    def crear_formulario_usuarios(self):
        # Título
        titulo = tk.Label(self.tab_usuarios, text="👤 Gestión de Usuarios", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.tab_usuarios, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Usuario:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w",
                                                                                        pady=5)
        self.usuario_id_entry = tk.Entry(form_frame, width=30)
        self.usuario_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Username:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w",
                                                                                      pady=5)
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Email:", bg="#f8f0e3", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Contraseña:", bg="#f8f0e3", font=("Arial", 12)).grid(row=3, column=0, sticky="w",
                                                                                        pady=5)
        self.password_entry = tk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=3, column=1, sticky="w", pady=5)

        # Campo de imagen
        tk.Label(form_frame, text="Imagen de Perfil:", bg="#f8f0e3", font=("Arial", 12)).grid(row=4, column=0,
                                                                                              sticky="w", pady=5)
        self.imagen_path = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.imagen_path, width=30).grid(row=4, column=1, sticky="w", pady=5)
        tk.Button(form_frame, text="Seleccionar Imagen", command=self.seleccionar_imagen).grid(row=4, column=2,
                                                                                               sticky="w", pady=5)

        # Botones
        btn_frame = tk.Frame(self.tab_usuarios, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_usuarios_tabla).pack(side=tk.LEFT, padx=5)

        # TABLA DE USUARIOS
        tabla_frame = tk.Frame(self.tab_usuarios, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Lista de Usuarios", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Username", "Email", "Fecha Registro")
        self.tabla_usuarios = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_usuarios.heading("ID", text="ID")
        self.tabla_usuarios.heading("Username", text="Username")
        self.tabla_usuarios.heading("Email", text="Email")
        self.tabla_usuarios.heading("Fecha Registro", text="Fecha Registro")

        self.tabla_usuarios.column("ID", width=50)
        self.tabla_usuarios.column("Username", width=120)
        self.tabla_usuarios.column("Email", width=150)
        self.tabla_usuarios.column("Fecha Registro", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scrollbar.set)

        self.tabla_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_usuarios.bind("<<TreeviewSelect>>", self.seleccionar_usuario_tabla)

        # Cargar datos iniciales
        self.cargar_usuarios_tabla()

    # FUNCIONES USUARIO
    def guardar_usuario(self):
        if not self.validar_id_usuario():
            return

        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        imagen = self.imagen_path.get()

        if not self.validar_texto_username(username):
            return
        if not self.validar_email_usuario(email):
            return
        if not self.validar_texto_password(password):
            return
        if not self.validar_imagen(imagen):
            return

        if not messagebox.askyesno("Confirmar", f"¿Guardar usuario {username}?"):
            return

        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO usuarios (username, password_hash, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, f"hash_{password}", email))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Usuario {username} guardado exitosamente")
            self.limpiar_usuario()
            self.cargar_usuarios_tabla()
        except Error as e:
            messagebox.showerror("Error", f"Error al guardar usuario {username}: {e}")
            self.conn.rollback()

    def actualizar_usuario(self):
        user_id = self.usuario_id_entry.get()
        if not user_id:
            messagebox.showwarning("Advertencia", "ID de usuario es obligatorio para actualizar")
            return
        if not self.validar_id_usuario():
            return

        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not self.validar_texto_username(username):
            return
        if not self.validar_email_usuario(email):
            return
        if password and not self.validar_texto_password(password):
            return

        if not messagebox.askyesno("Confirmar", f"¿Actualizar usuario con ID {user_id}?"):
            return

        try:
            cursor = self.conn.cursor()
            if password:
                query = "UPDATE usuarios SET username=%s, password_hash=%s, email=%s WHERE id=%s"
                cursor.execute(query, (username, f"hash_{password}", email, user_id))
            else:
                query = "UPDATE usuarios SET username=%s, email=%s WHERE id=%s"
                cursor.execute(query, (username, email, user_id))

            self.conn.commit()
            messagebox.showinfo("Éxito", f"Usuario con ID {user_id} actualizado exitosamente")
            self.limpiar_usuario()
            self.cargar_usuarios_tabla()
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar usuario {user_id}: {e}")
            self.conn.rollback()

    def eliminar_usuario(self):
        user_id = self.usuario_id_entry.get()
        if not user_id:
            messagebox.showwarning("Advertencia", "ID de usuario es obligatorio")
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar a este usuario?"):
            try:
                cursor = self.conn.cursor()
                query = "DELETE FROM usuarios WHERE id=%s"
                cursor.execute(query, (user_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Usuario {user_id} eliminado exitosamente")
                self.limpiar_usuario()
                self.cargar_usuarios_tabla()
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
                self.conn.rollback()

    def limpiar_usuario(self):
        self.usuario_id_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.imagen_path.set("")

    # ----------------------------------------
    # MÓDULO 2: EMOCIONES
    # ----------------------------------------
    def crear_formulario_emociones(self):
        # Título
        titulo = tk.Label(self.tab_emociones, text="😊 Catálogo de Emociones", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.tab_emociones, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Emoción:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w",
                                                                                        pady=5)
        self.emocion_id_entry = tk.Entry(form_frame, width=30)
        self.emocion_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Nombre:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_emocion_entry = tk.Entry(form_frame, width=30)
        self.nombre_emocion_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Imagen de la Emocion: ", bg="#f8f0e3", font =("Arial", 12)).grid(row=2, column=0, sticky="w",)
        self.imagen_emocion_path = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.imagen_emocion_path, width=30).grid(row=2, column=1, sticky="w", pady=5)
        tk.Button(form_frame,text="Seleccionar Imagen", command=self.seleccionar_imagen).grid(row=3, column=1, sticky="w", padx=5, pady=5)


        # Botones
        btn_frame = tk.Frame(self.tab_emociones, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_emocion).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_emociones_tabla).pack(side=tk.LEFT, padx=5)

        # TABLA DE EMOCIONES
        tabla_frame = tk.Frame(self.tab_emociones, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Catálogo de Emociones", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Nombre", "Emoji")
        self.tabla_emociones = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_emociones.heading("ID", text="ID")
        self.tabla_emociones.heading("Nombre", text="Nombre")
        self.tabla_emociones.heading("Emoji", text="Emoji")

        self.tabla_emociones.column("ID", width=50)
        self.tabla_emociones.column("Nombre", width=150)
        self.tabla_emociones.column("Emoji", width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_emociones.yview)
        self.tabla_emociones.configure(yscrollcommand=scrollbar.set)

        self.tabla_emociones.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_emociones.bind("<<TreeviewSelect>>", self.seleccionar_emocion_tabla)

        # Cargar datos iniciales
        self.cargar_emociones_tabla()

    # FUNCIONES EMOCIONES (se mantienen igual que antes)
    def guardar_emocion(self):
        if not self.validar_id_emocion():
            return

        nombre = self.nombre_emocion_entry.get()

        imagen = self.imagen_emocion_path.get().strip()
        if imagen and not self.validar_imagen(imagen):
            return

        if not self.validar_texto_nombre_emocion(nombre):
            return

        if not messagebox.askyesno("Confirmar", f"¿Guardar emoción {nombre}?"):
            return

        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO emociones (nombre) VALUES (%s)"
            cursor.execute(query, (nombre,))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Emoción {nombre} guardada exitosamente")
            self.limpiar_emocion()
            self.cargar_emociones_tabla()
        except Error as e:
            messagebox.showerror("Error", f"Error al guardar emoción: {e}")
            self.conn.rollback()

    def actualizar_emocion(self):
        emocion_id = self.emocion_id_entry.get()
        if not emocion_id:
            messagebox.showwarning("Advertencia", "ID de la emoción es obligatorio")
            return
        if not self.validar_id_emocion():
            return

        nombre = self.nombre_emocion_entry.get()

        if not self.validar_texto_nombre_emocion(nombre):
            return

        if not messagebox.askyesno("Confirmar", f"¿Actualizar emoción con ID {emocion_id}?"):
            return

        try:
            cursor = self.conn.cursor()
            query = "UPDATE emociones SET nombre=%s WHERE id=%s"
            cursor.execute(query, (nombre, emocion_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Emoción {emocion_id} actualizada exitosamente")
            self.limpiar_emocion()
            self.cargar_emociones_tabla()
        except Error as e:
            messagebox.showerror("Error", f"Error al actualizar emoción: {e}")
            self.conn.rollback()

    def eliminar_emocion(self):
        emocion_id = self.emocion_id_entry.get()
        if not emocion_id:
            messagebox.showwarning("Advertencia", "ID de la emoción es obligatorio")
            return
        if not self.validar_id_emocion():
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta emoción?"):
            try:
                cursor = self.conn.cursor()
                query = "DELETE FROM emociones WHERE id=%s"
                cursor.execute(query, (emocion_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Emoción con ID {emocion_id} eliminada exitosamente")
                self.limpiar_emocion()
                self.cargar_emociones_tabla()
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar emoción: {e}")
                self.conn.rollback()

    def limpiar_emocion(self):
        self.emocion_id_entry.delete(0, tk.END)
        self.nombre_emocion_entry.delete(0, tk.END)

    # ----------------------------------------
    # MÓDULO 3: ENTRADAS
    # ----------------------------------------
    def crear_formulario_entradas(self):
        # Título
        titulo = tk.Label(self.tab_entradas, text="📖 Entradas del Diario", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        # Frame del formulario
        form_frame = tk.Frame(self.tab_entradas, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        # Campos del formulario
        tk.Label(form_frame, text="ID Entrada:", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0, sticky="w",
                                                                                        pady=5)
        self.entrada_id_entry = tk.Entry(form_frame, width=30)
        self.entrada_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Usuario ID:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w",
                                                                                        pady=5)
        self.entrada_usuario_id_entry = tk.Entry(form_frame, width=30)
        self.entrada_usuario_id_entry.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Fecha:", bg="#f8f0e3", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.fecha_entry = DateEntry(form_frame, width=28, date_pattern="yyyy-mm-dd")
        self.fecha_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Texto:", bg="#f8f0e3", font=("Arial", 12)).grid(row=3, column=0, sticky="nw", pady=5)
        self.texto_entry = tk.Text(form_frame, width=30, height=5)
        self.texto_entry.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Emociones (IDs):", bg="#f8f0e3", font=("Arial", 12)).grid(row=4, column=0,
                                                                                             sticky="w", pady=5)
        self.emociones_ids_entry = tk.Entry(form_frame, width=30)
        self.emociones_ids_entry.grid(row=4, column=1, sticky="w", pady=5)

        # Botones
        btn_frame = tk.Frame(self.tab_entradas, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="💾 Guardar", bg="#88c9a1", fg="white", width=12,
                  command=self.guardar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Actualizar", bg="#a2b9bc", fg="white", width=12,
                  command=self.actualizar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", bg="#e77f67", fg="white", width=12,
                  command=self.eliminar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🧹 Limpiar", bg="#f5c091", fg="#5a4a42", width=12,
                  command=self.limpiar_entrada).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔄 Cargar Datos", bg="#a2b9bc", fg="white", width=12,
                  command=self.cargar_entradas_tabla).pack(side=tk.LEFT, padx=5)

        # TABLA DE ENTRADAS
        tabla_frame = tk.Frame(self.tab_entradas, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📋 Historial de Entradas", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview
        columns = ("ID", "Usuario", "Fecha", "Resumen")
        self.tabla_entradas = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_entradas.heading("ID", text="ID")
        self.tabla_entradas.heading("Usuario", text="Usuario")
        self.tabla_entradas.heading("Fecha", text="Fecha")
        self.tabla_entradas.heading("Resumen", text="Resumen")

        self.tabla_entradas.column("ID", width=50)
        self.tabla_entradas.column("Usuario", width=100)
        self.tabla_entradas.column("Fecha", width=100)
        self.tabla_entradas.column("Resumen", width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_entradas.yview)
        self.tabla_entradas.configure(yscrollcommand=scrollbar.set)

        self.tabla_entradas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind evento de selección
        self.tabla_entradas.bind("<<TreeviewSelect>>", self.seleccionar_entrada_tabla)

        # Cargar datos iniciales
        self.cargar_entradas_tabla()

    # FUNCIONES ENTRADAS (se mantienen igual que antes)
    def guardar_entrada(self):
        if not self.validar_usuario_id_entrada():
            return

        usuario_id = self.entrada_usuario_id_entry.get()
        texto = self.texto_entry.get("1.0", tk.END).strip()
        emociones_ids = self.emociones_ids_entry.get()

        if not self.validar_entrada(texto):
            return

        if not messagebox.askyesno("Confirmar", f"¿Guardar entrada para Usuario {usuario_id}?"):
            return

        try:
            cursor = self.conn.cursor()
            fecha = self.fecha_entry.get()

            query_entrada = "INSERT INTO entradas (usuario_id, fecha, texto) VALUES (%s, %s, %s)"
            cursor.execute(query_entrada, (usuario_id, fecha, texto))
            entrada_id = cursor.lastrowid

            if emociones_ids:
                emociones_lista = [eid.strip() for eid in emociones_ids.split(',')]
                for emocion_id in emociones_lista:
                    if emocion_id and emocion_id.isdigit():
                        query_relacion = "INSERT INTO entrada_emocion (entrada_id, emocion_id) VALUES (%s, %s)"
                        cursor.execute(query_relacion, (entrada_id, emocion_id))

            self.conn.commit()
            messagebox.showinfo("Éxito", f"Entrada guardada para Usuario ID: {usuario_id}")
            self.limpiar_entrada()
            self.cargar_entradas_tabla()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            self.conn.rollback()

    def actualizar_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if not entrada_id:
            messagebox.showwarning("Advertencia", "ID de entrada es obligatorio")
            return
        if not self.validar_id_entrada():
            return

        usuario_id = self.entrada_usuario_id_entry.get()
        texto = self.texto_entry.get("1.0", tk.END).strip()

        if not self.validar_usuario_id_entrada():
            return
        if not self.validar_entrada(texto):
            return

        if not messagebox.askyesno("Confirmar", f"¿Actualizar entrada con ID {entrada_id}?"):
            return

        try:
            cursor = self.conn.cursor()
            fecha = self.fecha_entry.get()
            query = "UPDATE entradas SET usuario_id=%s, fecha=%s, texto=%s WHERE id=%s"
            cursor.execute(query, (usuario_id, fecha, texto, entrada_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", f"Entrada con ID: {entrada_id} actualizada correctamente")
            self.limpiar_entrada()
            self.cargar_entradas_tabla()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            self.conn.rollback()

    def eliminar_entrada(self):
        entrada_id = self.entrada_id_entry.get()
        if not entrada_id:
            messagebox.showwarning("Advertencia", "ID de entrada es obligatorio")
            return
        if not self.validar_id_entrada():
            return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta entrada?"):
            try:
                cursor = self.conn.cursor()
                query = "DELETE FROM entradas WHERE id=%s"
                cursor.execute(query, (entrada_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Entrada con ID {entrada_id} eliminada correctamente")
                self.limpiar_entrada()
                self.cargar_entradas_tabla()
            except Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")
                self.conn.rollback()

    def limpiar_entrada(self):
        self.entrada_id_entry.delete(0, tk.END)
        self.entrada_usuario_id_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.texto_entry.delete("1.0", tk.END)
        self.emociones_ids_entry.delete(0, tk.END)

    # ----------------------------------------
    # MÓDULO 4: REPORTES
    # ----------------------------------------
    def crear_formulario_reportes(self):
        titulo = tk.Label(self.tab_reportes, text="📈 Resumen Emocional", font=("Arial", 16, "bold"), fg="#b86d6d",
                          bg="#faf3e0")
        titulo.pack(pady=(20, 10))

        form_frame = tk.Frame(self.tab_reportes, bg="#f8f0e3", padx=20, pady=20, relief="groove", bd=1)
        form_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(form_frame, text="Selecciona un usuario (ID):", bg="#f8f0e3", font=("Arial", 12)).grid(row=0, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=5)
        self.reporte_usuario_id_entry = tk.Entry(form_frame, width=30)
        self.reporte_usuario_id_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Período:", bg="#f8f0e3", font=("Arial", 12)).grid(row=1, column=0, sticky="w",
                                                                                     pady=5)
        self.periodo_var = tk.StringVar(value="semana")
        ttk.Radiobutton(form_frame, text="Semana", variable=self.periodo_var, value="semana").grid(row=1, column=1,
                                                                                                   sticky="w")
        ttk.Radiobutton(form_frame, text="Mes", variable=self.periodo_var, value="mes").grid(row=1, column=2,
                                                                                             sticky="w")

        btn_frame = tk.Frame(self.tab_reportes, bg="#faf3e0")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="📊 Generar Reporte", bg="#88c9a1", fg="white", width=20,
                  command=self.generar_reporte).pack(padx=5)

        # TABLA DE REPORTES
        tabla_frame = tk.Frame(self.tab_reportes, bg="#faf3e0")
        tabla_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(tabla_frame, text="📊 Estadísticas Emocionales", font=("Arial", 14, "bold"),
                 fg="#b86d6d", bg="#faf3e0").pack(pady=(0, 10))

        # Crear Treeview para reportes
        columns = ("Emoción", "Frecuencia", "Última Registro")
        self.tabla_reportes = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=8)

        # Configurar columnas
        self.tabla_reportes.heading("Emoción", text="Emoción")
        self.tabla_reportes.heading("Frecuencia", text="Frecuencia")
        self.tabla_reportes.heading("Última Registro", text="Última Registro")

        self.tabla_reportes.column("Emoción", width=150)
        self.tabla_reportes.column("Frecuencia", width=100)
        self.tabla_reportes.column("Última Registro", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla_reportes.yview)
        self.tabla_reportes.configure(yscrollcommand=scrollbar.set)

        self.tabla_reportes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def generar_reporte(self):
        usuario_id = self.reporte_usuario_id_entry.get()
        periodo = self.periodo_var.get()

        if not usuario_id:
            messagebox.showwarning("Advertencia", "Por favor, Ingrese un ID de usuario para generar reporte")
            return
        if not usuario_id.isdigit():
            messagebox.showerror("Error", "ID de usuario debe ser un número")
            return

        try:
            cursor = self.conn.cursor()

            # Consulta para obtener emociones más frecuentes
            query = """
            SELECT e.nombre, COUNT(ee.emocion_id) as frecuencia, MAX(en.fecha) as ultima_fecha
            FROM entrada_emocion ee 
            JOIN emociones e ON ee.emocion_id = e.id 
            JOIN entradas en ON ee.entrada_id = en.id 
            WHERE en.usuario_id = %s 
            GROUP BY e.nombre 
            ORDER BY frecuencia DESC
            """

            cursor.execute(query, (usuario_id,))
            resultados = cursor.fetchall()

            # Limpiar tabla
            for item in self.tabla_reportes.get_children():
                self.tabla_reportes.delete(item)

            # Insertar datos en la tabla
            if resultados:
                for emocion, frecuencia, ultima_fecha in resultados:
                    self.tabla_reportes.insert("", "end", values=(emocion, f"{frecuencia} veces", ultima_fecha))
                messagebox.showinfo("Éxito", f"Reporte generado para usuario {usuario_id}")
            else:
                messagebox.showinfo("Reporte", "No hay datos para generar el reporte")

        except Error as e:
            messagebox.showerror("Error", f"Error al generar reporte: {e}")

    def crear_footer(self):
        footer = tk.Label(self.root, text="Diario de Emociones v1.0 — Tu espacio seguro para sentir 🌿",
                          font=("Arial", 10, "italic"), fg="#7d6e65", bg="#faf3e0")
        footer.pack(side=tk.BOTTOM, pady=15)


# ----------------------------------------
# INICIAR LA APLICACIÓN
# ----------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DiarioEmocionesApp(root)
    root.mainloop()
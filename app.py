from flask import Flask, render_template,redirect,request,session
from flask.sessions import SecureCookieSession
from werkzeug.security import generate_password_hash, check_password_hash
import db
import os

app = Flask(__name__)
sesion_iniciada = False
user = None
id = None
idp = 0
nom= None
app.secret_key= os.urandom(32)
productoV = []
nombre = None
añadidoC = ""
@app.route("/", methods=["GET", "POST"])
def home():
    global sesion_iniciada
    productos = db.obtenerAllProductos()

    if sesion_iniciada:
        if request.method == "POST":
            sesion_iniciada = False
            return redirect("/")
        else:
            return render_template("home.html", sesion_iniciada = sesion_iniciada,perfil = nom,productos= productos)
    else:
        return render_template("home.html",productos= productos)
    


@app.route("/login", methods=["GET", "POST"])
#SI LA PERSONA ES ADMIN LO MANDA AL DASHBOARD, SINO, VA AL INICIO
def login():
    global sesion_iniciada
    global id
    global nom
    mensaje = "Error al iniciar Sesión"
    mensaje2 = "Contraseña Incorrecta"
    
    if sesion_iniciada:
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("Login.html")
        else:
            session.pop("user_id", None)

            nombre = request.form["username"]
            contra = request.form["password"]

            try:
                fila = db.obtenerUsuarios(nombre)
                print(fila)

                if len(fila) > 0:
                    user = fila[4]
                    nom = fila[4]
                    password = fila[5]
                    id = fila[0]


                    if nombre == "admin":
                        if contra == str(password):
                            sesion_iniciada = True
                            return redirect("/dashboard")
                        else:
                            return render_template("Login.html", men2 = mensaje2)
                    else:
                        valide = check_password_hash(password,contra)
                        if valide == True:  
                                
                            sesion_iniciada = True
                            print(id)
                            session["user_id"] = id
                            return redirect("/")
                        else:
                            return render_template("Login.html",men2 = mensaje2)
                else : 
                    return render_template('Login.html')
            except:
                return render_template("Login.html",men = mensaje)



@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["celular"]
        correo = request.form["correo"]
        usuario = request.form["usuario"]
        password = request.form["password"]

        db.registrarUsuario(nombre,telefono,correo,usuario,generate_password_hash(password))
        
        return redirect("/login")
    else:
        return render_template("Registrar.html")

@app.route("/cerrar")
def cerrar():
    global sesion_iniciada
    sesion_iniciada = False
    session.pop("user_id", None)
    return redirect("/")

@app.route("/gestionarU")
def gestionarUsuario():
    global sesion_iniciada
    return render_template("GestionarUsuario.html")
@app.route("/dashboard/", methods=["GET","POST"])
def dashboard():
    global sesion_iniciada
    if sesion_iniciada:
        return render_template("Dashboard-Administrativo.html")
    else:
        return redirect("/login")

@app.route("/ofertas/", methods=["GET"])
def oferta():
    global nom
    return render_template("Ofertas.html",sesion_iniciada=sesion_iniciada,perfil = nom)

@app.route("/categorias/", methods=["GET","POST"])
def categorias():
    global nom
    if request.method == "POST":
        categoria = request.form["nombre"]
        productos = db.obtenerProductoCate(categoria)
        return render_template("categoria2.html",sesion_iniciada = sesion_iniciada,perfil = nom,productos= productos,categoria=categoria)
    else:
        return render_template("Categorias.html",sesion_iniciada = sesion_iniciada,perfil = nom)




@app.route("/agregar", methods=["GET","POST"])
def agregarP():
    global sesion_iniciada
    men = None
    if sesion_iniciada:
        if request.method == "POST":
            id = request.form["codigo"]
            nombre = request.form["nombre"]
            categoria = request.form["categoria"]
            cantidad = request.form["cantidad"]
            precio = request.form["precio"]
            descripcion = request.form["descripcion"]
            foto = request.form["foto"]

            db.agregarPBase(id,nombre,categoria,cantidad,precio,descripcion,foto)
            mensaje = "Producto Agregado!"
            return render_template("Agregar.html",men = mensaje)
        else:
            return render_template("Agregar.html")
    else:
        return redirect("/login")




@app.route("/editar", methods=["GET","POST"])
def editarP():
    global sesion_iniciada
    if sesion_iniciada:
        if request.method == "POST":
            codigo = request.form["codigo"]
            
            fila = db.obtenerProducto(codigo)
            cd = fila[0]
            nb = fila[1]
            cg = fila[2]
            ct = fila[3]
            pr = fila[4]
            ds = fila[5]
            ft = fila[6]
            return render_template("Editar.html", codi = cd, nomb = nb, cate = cg, cant = ct, prec = pr, desc = ds) 
        else:
            return render_template("Editar.html")
    else:
        return redirect("/login")

@app.route("/editarPro", methods=["GET","POST"])
def editarPro():
    global sesion_iniciada
    mensaje = "Producto Editado"
    if sesion_iniciada:
        if request.method == "POST":
            id = request.form["codigo"]
            nombre = request.form["nombre"]
            categoria = request.form["categoria"]
            cantidad = request.form["cantidad"]
            precio = request.form["precio"]
            descripcion = request.form["descripcion"]

            db.actualizarProducto(id,nombre,categoria,cantidad,precio,descripcion)

            return render_template("Editar.html",men = mensaje)
        else:
            return render_template("Editar.html")
    else:
        return redirect("/login")

@app.route("/eliminar", methods=["GET","POST"])
def eliminarP():
    global sesion_iniciada
    if sesion_iniciada:
        if request.method == "POST":
            id = request.form["buscar"]
            fila = db.obtenerProducto(id)
            cd = fila[0]
            nb = fila[1]
            cg = fila[2]
            ct = fila[3]
            pr = fila[4]
            ds = fila[5]
            ft = fila[6]
            return render_template("Eliminar.html", codi = cd, nomb = nb, cate = cg, cant = ct, prec = pr, desc = ds)   
        else:
            return render_template("Eliminar.html")
    else:
        return redirect("/login")

@app.route("/eliminarPro", methods=["GET","POST"])
def eliminarPro():
    global sesion_iniciada
    men = None
    men2 = None
    if sesion_iniciada:
        if request.method == "POST":
            id = request.form["codigo"]
            print(id)
            mensaje="Producto Eliminadoo"
            mensaje2="No se encontró el producto"

            ok = db.eliminarProducto(id)

            if ok == False:
                return render_template("Eliminar.html", men = mensaje2) 
            else:
               return render_template("Eliminar.html", men = mensaje)  
        else:
            return render_template("Eliminar.html")
    else:
        return redirect("/login")




@app.route("/eliminarUsuario", methods=["GET","POST"])
def eliminarUsuario():
    global sesion_iniciada
    mensaje = None
    mensaje2 = None
    if sesion_iniciada:
        if request.method == "POST":
            usuario = request.form["usuario"]
            ok = db.eliminarUsuario(usuario)
            if ok ==False:
                mensaje="No se encontró el usuario"
                return render_template("GestionarUsuario.html",men = mensaje)
                
            else:
                mensaje2="Usuario Eliminado"
                return render_template("GestionarUsuario.html",men = mensaje2)
        else:
            return render_template("GestionarUsuario.html")
    else:
        return redirect("/login")

@app.route("/buscarUsuario", methods=["GET","POST"])
def buscarUsuario():
    global user
    global sesion_iniciada
    mensaje = "Usuario No encontrado"
    if sesion_iniciada:
        if request.method == "POST":

            usuario = request.form["usuario"]
            fila = db.obtenerUsuarios(usuario)
            if fila != None:
                correo = fila[3]
                usua = fila[4]
                contra = fila[5]
                user = fila[4]
                return render_template("GestionarUsuario.html",user=usua,contra=contra,correo=correo)
            else:
                return render_template("GestionarUsuario.html",men = mensaje)
        else:
            return render_template("GestionarUsuario.html")
    else:
        return redirect("/login")

@app.route("/editarUsuario", methods=["GET","POST"])
def editarUsuario():
    global sesion_iniciada
    global user
    mensaje = "Usuario Actualizado"
    if sesion_iniciada:
        if request.method == "POST":
            usuario = request.form["usuario"]
            correo = request.form["correo"]
            contra= request.form["contra"]
            db.actualizarUsuario(usuario,correo,contra,user)

            return render_template("GestionarUsuario.html", men = mensaje)
        else:
            return render_template("GestionarUsuario.html")
    else:
        return redirect("/login")
        

@app.route("/producto/tal", methods=["GET","POST"])
def producto():
    global sesion_iniciada
    global productoV
    productoV = []
    global idp
    global id
    global nombre
    global añadidoC
    if request.method == "POST":
        try:
            comentario = request.form["comentario"]
            nombre = request.form["nomPro"]
            if sesion_iniciada:    
                db.agregarComentario(idp,id,comentario)
                return redirect("/producto/tal")
            else:
                return redirect("/login")
        except:
            try:
                nombre = request.form["titulo"]
            except:
                print("f")
            fila = db.obtenerProductoNom(nombre)
            print(nombre)
            idp = fila[0]
            titulo = fila[1]
            descripcion = fila[5]
            precio = fila[4]
            foto = fila[6]
            productoV.append(idp)
            productoV.append(titulo)
            productoV.append(descripcion)
            productoV.append(precio)
            productoV.append(foto)
            
            filas = db.obtenerComentarios(idp)
            coments = []

            for x in filas:
                datos = db.obtenerUsuariosID(x[2])
                persona = (datos[4],x[3],x[2])
                coments.append(persona)

               
            print(coments)
            
            return render_template("Productoo.html",sesion_iniciada = sesion_iniciada,productoV = productoV,coments=coments,perfil = nom,perfil2 = id)
    else:
        print("al inicio")
        print("metodo post=")
        print(nombre)
        fila = db.obtenerProductoNom(nombre)
        print(nombre)
        idp = fila[0]
        titulo = fila[1]
        descripcion = fila[5]
        precio = fila[4]
        foto = fila[6]
        productoV.append(idp)
        productoV.append(titulo)
        productoV.append(descripcion)
        productoV.append(precio)
        productoV.append(foto)
        
        filas = db.obtenerComentarios(idp)
        coments = []

        for x in filas:
            datos = db.obtenerUsuariosID(x[2])
            persona = (datos[4],x[3],x[2])
            coments.append(persona)
        print(coments)
        return render_template("Productoo.html",sesion_iniciada = sesion_iniciada,productoV = productoV,coments=coments,perfil = nom,perfil2 = id,men=añadidoC) 


@app.route("/Pcomentario", methods=["GET","POST"])
def Pcomentario():
    global sesion_iniciada
    global id
    global productoV
    global idp
    if sesion_iniciada:
        if request.method == "POST":
            comentario = request.form["comentario"]
            db.agregarComentario(idp,id,comentario)
            return redirect("/producto/tal")
        else:
            return redirect("/producto/tal")
    else:
        return redirect("/login")




@app.route("/producto/gestionar_comentarios/", methods=["GET","POST"])
def gesComentario():
    return "<h1>Página de Gestión de Comentarios</h1>"

@app.route("/producto/comprar/<id_producto>", methods=["GET","POST"])
def comprar(id_producto):
    return f"<h1>Página de Compra del producto: {id_producto}</h1>"

@app.route("/producto/calificar/", methods=["GET","POST"])
def calificar():
    return "<h1>Página de Calificar Producto</h1>"



@app.route("/eliminarComentario", methods=["GET","POST"])
def eliminarComentario():
    if sesion_iniciada: 
        if request.method == "POST":
            comentario = request.form["coment"]
            print(comentario)
            db.eliminarComentario(comentario)

            return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/login")


@app.route("/aLista", methods=["GET","POST"])
def agregarLista():
    global sesion_iniciada
    men = None
    global id
    if sesion_iniciada:
        if request.method == "POST":
            codigo = request.form["codigo"]
            
            db.agregarALista(id,codigo)

            return redirect("/lista")
        else:
            return redirect("/lista")
    else:
        return redirect("/login")


@app.route("/lista", methods=["GET","POST"])
def listaD():
    global id
    global sesion_iniciada
    if(sesion_iniciada==True):
        if(request.method =="GET"):
            listaDeseos=[]
            dba = db.conectar()
            for row in dba.execute(
                'SELECT * FROM LISTAD, Productos WHERE LISTAD.PRODUCTO = PRODUCTOS.codigo AND LISTAD.USUARIO = ? ', (id,)
            ):
                listaDeseos.append(row)
            return render_template('lista-de-deseos-.html',listaDeseos=listaDeseos,sesion_iniciada = sesion_iniciada,perfil = nom) 
        else:
            print("f")
    else:return redirect('/login')

@app.route("/eliminarLista", methods=["GET","POST"])
def eliminarLista():
    if sesion_iniciada: 
        if request.method == "POST":
            nombre = request.form["codigo"]
            print(nombre)
            db.eliminarListaDeseos(nombre)

            return redirect("/lista")
        else:
            return render_template("Lista-de-deseos-.html")
    else:
        return redirect("/login")

@app.route("/aCarrito", methods=["GET","POST"])
def agregarCarrito():
    global sesion_iniciada
    global id
    global añadidoC
    if sesion_iniciada:
        if request.method == "POST":
            añadidoC = "Producto añadido al Carrito"
            codigo = request.form["codigo"]
            print("el codigo es: ",codigo)
            db.agregarACarrito(id,codigo)

            return redirect("/producto/tal")
        else:
            return redirect("/carrito")
    else:
        return redirect("/login")

@app.route("/carrito", methods=["GET"])
def carrito():
    global id
    global sesion_iniciada
    if(sesion_iniciada==True):
        if(request.method =="GET"):
            Carrito=[]
            total=0
            dba = db.conectar()
            for row in dba.execute('SELECT * FROM Carrito, Productos WHERE Carrito.PRODUCTO = PRODUCTOS.codigo AND Carrito.USUARIO = ? ', (id,)):
                Carrito.append(row)
                cadena = row[7]
                nuevaC = cadena.replace('.','')
                precio = int(nuevaC) 
                total = total + precio
            
            p = str(total)
            pre = ""
            x = 0
            for i in range(len(p)-1, -1, -1):
                x=x+1
                if x == 4 or x == 7 or x == 10 or x== 13:
                    pre = pre + "."
                pre = pre + p[i]
            pre2 = ""
            for i in range(len(pre)-1, -1, -1):
                pre2 = pre2 + pre[i]


            return render_template('Carrito.html',carrito=Carrito,sesion_iniciada = sesion_iniciada,perfil = nom, precio = pre2) 
        else:
            print("f")
    else:return redirect('/login')

@app.route("/eliminarCarrito", methods=["GET","POST"])
def eliminarCarrito():
    if sesion_iniciada: 
        if request.method == "POST":
            nombre = request.form["codigo"]
            print(nombre)
            db.eliminarCarrito(nombre)

            return redirect("/carrito")
        else:
            return redirect("/")
    else:
        return redirect("/login")



if __name__ == "__main__":
    app.run(debug=True)
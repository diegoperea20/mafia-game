from flask import Flask, render_template, request
import random

app = Flask(__name__)

jugadores = {}
eliminados = []
ganador = None
roles = []
civiles = None
mafia = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' or request.method == 'GET':
        
        global ganador
        if ganador:
            return render_template('index.html', ganador=ganador, eliminados=eliminados)
        else:
            return render_template('index.html', jugadores=jugadores, roles=roles, civiles=civiles, mafia=mafia)
        
def contar_roles(jugadores):
    civiles_total = 0
    mafia_total = 0
    for rol in jugadores.values():
        if rol == "civil":
            civiles_total += 1
        else:
            mafia_total += 1
    return civiles_total, mafia_total

def determinar_ganador(civiles_total, mafia_total):
    if civiles_total == mafia_total:
        return "mafia"
    elif civiles_total < mafia_total:
        return "mafia"
    else:
        return "civil"

@app.route('/jugar', methods=['POST'])
def jugar():
    global jugadores, roles, eliminados, ganador
    
    nombre = request.form['nombre']
    if len(nombre) == 0:
        mensaje_rol = "You must enter a name"
    elif nombre in jugadores:
        mensaje_rol = "This name is already in use"
    elif ganador:
        mensaje_rol = "The game is over"
    else:
        if len(roles) == 0:
            mensaje_limite="Maximum Players"
            return render_template('index.html',mensaje_limite=mensaje_limite)
        else:
            rol = roles.pop()
            jugadores[nombre] = rol
            if rol == "civil":
                mensaje_rol = f"{nombre}, are a civilian"
            else:
                mensaje_rol = f"{nombre}, are a mafia"
        
   
    print(jugadores.keys())
    print("total roles",len(roles))
    return render_template('index.html',nombresjugador=jugadores.keys(),nombre=nombre,mensaje_rol=mensaje_rol if mensaje_rol else '')



@app.route('/configurar', methods=['POST'])
def configurar():
    global roles
    civiles = int(request.form['civiles'])
    mafia = int(request.form['mafia'])
    if civiles == mafia:
        mensaje="The number of civilians and mafia should be different."
    elif civiles < mafia:
        mensaje="The number of civilians must be greater than the number of mobs or mafia."
    else:
        roles = ["civil"] * civiles + ["mafia"] * mafia
        random.shuffle(roles)
        return render_template('index.html')
    return render_template('index.html', mensaje=mensaje)


@app.route('/eliminar', methods=['POST'])
def eliminar():
    global jugadores, civiles, mafia

    civiles_total, mafia_total = contar_roles(jugadores)

    nombre_e = request.form['nombre_eliminar'].lower()
    if nombre_e in jugadores:
        rol = jugadores[nombre_e]
        del jugadores[nombre_e]
        if rol == "civil":
            civiles_total -= 1
        else:
            mafia_total -= 1
        mensaje_delete = f"{nombre_e} ({rol}) has been eliminated."
        if civiles_total == 0:
            mensaje_delete += " Mafia wins."
            civiles = 0
            mafia = 0
        elif mafia_total == 0:
            mensaje_delete += " Civilians win"
            civiles = 0
            mafia = 0
        elif mafia_total == civiles_total:
            mensaje_delete += " Mafia wins."
            civiles = 0
            mafia = 0
        else:
            civiles = civiles_total
            mafia = mafia_total
    else:
        mensaje_delete = "The entered player does not exist."

    return render_template('index.html', mensaje_delete=mensaje_delete, jugadores=jugadores, roles=roles, civiles=civiles, mafia=mafia,nombresjugador=jugadores.keys())



@app.route('/how', methods=['POST'])
def how():
    return render_template('how.html')



if __name__ == '__main__':
    app.run(debug=True)



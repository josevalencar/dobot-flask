from flask import Flask, render_template, request
from datetime import datetime
from tinydb import TinyDB, Query
from pydobot import Dobot
from serial.tools import list_ports
from dobot import DobotMoves

app = Flask(__name__)

db = TinyDB('db.json')

conectado = True
robo=DobotMoves()

# Rota de teste
@app.route('/')
def ola():
    db.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "Página inicial",
    })
    return render_template('index.html')

# Rota de logs
@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/dobot')
def dobot():
    return render_template('dobot.html')

# Rota que retorna os acessos
@app.route('/atualiza-logs')
def retorna_acessos():
    return render_template('item-log.html', itens=db)

@app.route('/conectar')
def connect():
    global conectado
    print(list_ports.comports()[1].device)
    port = list_ports.comports()[1].device
    robo.conectar(port)
    conectado=True
    # robot_move()
    db.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "acao": "Conecta ao Robô",
    "hora":str(datetime.now()),
    })
    
    return render_template('robot-move.html', conectado=conectado)

@app.route('/desconectar')
def disconnect():
    global conectado
    robo.desconectar()
    conectado=False
    robo.robot_move()
    db.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "acao": "desconectar robô",
    "hora":str(datetime.now()),
    })
    return 'Desconectado com sucesso'

@app.route('/conexao')
def conexao():
    return render_template('connect-button.html')

@app.route('/robot-move')
def robot_move():
    # global conectado
    return render_template('robot-move.html')

@app.route('/mover_distancia', methods=['POST'])
def mover_distancia():
    global conectado
    if not conectado:
        return 'Robô não conectado'
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    robo.mover_distancia(x, y, z, r)
    db.insert({
    "endereco":str(request.environ['REMOTE_ADDR']),
    "metodo": str(request.method),
    "hora":str(datetime.now()),
    "acao": "Moveu o robo",
    "posicao_atual": "Posição movida: ",
    'x': x,
    'y': y,
    'z': z,
    'r': r
    })
    return 'Movido com sucesso'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
from flask import Flask, render_template, request, redirect, url_for
import csv
from matplotlib import pyplot as plt
from os import path
import os
import collections

if path.isdir('static/graph.png'):
    os.remove('static/graph.png')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect(url_for("teste"))
    return render_template('formulario.html')



@app.route('/teste')
def teste():
    req = request.args

    listaData = list()
    listaPreco = list()


    with open('2018-1_CA.csv', newline='', encoding='iso-8859-1') as csvfile:
        readCSV = csv.reader((line.replace('  ', '\t') for line in csvfile), delimiter='\t')
        for raw in readCSV:
            if (raw[2] == req.get("cidade").upper() and raw[5] == req.get("gasolina").upper()):
                listaData.append(raw[6])
                listaPreco.append(float(raw[8].replace(",",".")))

        #print(listaData)
        #print(listaPreco)

        d = list(zip(listaData, listaPreco))

        result = {}

        val = collections.Counter([x for (x, y) in d])
        valtuple = val.items()

        for datinhas, precinhos in d:
            total = result.get(datinhas, 0) + precinhos
            result[datinhas] = total

    datasnorepeat = [x[0] for x in result.items()]
    somadeprecos = [x[1] for x in result.items()]
    qntrepeatdata = [x[1] for x in valtuple]
    divisao = [i / j for i, j in zip(somadeprecos, qntrepeatdata)]




    fig = plt.figure()
    ax = fig.gca()
    ax.plot(datasnorepeat, divisao)
    plt.xlabel('Datas')
    plt.ylabel('Precos')
    fig.suptitle('Evolucao dos precos de ' + req.get("gasolina") + ' na cidade de ' + req.get("cidade") + ' no 1 Sem/2018',fontsize=10)
    fig.autofmt_xdate()

    every_nth = 4
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    fig.savefig('static/graph.png')


    return render_template('hello.html')

app.run()
#1: Session er röð af response og request samskiptum á milli client og server
#2: Session minni er minni sem að endist bara jafn langt og session-ið meðan cookies endast (eiginlega) eins lengi og maður vill (eins lengi og þeim er ekki eitt)
#3: Session ID er tala sem að vefsíða gefur einhverjum user til þess að muna efter þeim

from bottle import *
from beaker.middleware import SessionMiddleware

heads = {
    "cpu"  : "Intel Core i7 8700K örgjörvi",
    "gpu"  : "Asus GTX1080 Ti Turbo skjákort",
    "mobo" : "Asus Z370-A Prime móðurborð",
    "mem"  : "Corsair Dom 4x8GB 2400 minni"
}
pics  = {
    "cpu"  : "https://cdn.att.is//skrar/image/AJQ804/ITL-I78700K_370_370_2.jpg",
    "gpu"  : "https://cdn.att.is//skrar/image/HKT367/ASU-TURBOGTX1080TI11_370_370_2.png",
    "mobo" : "https://cdn.att.is//skrar/image/AJQ804/ASU-Z370A_370_370_2.png",
    "mem"  : "https://cdn.att.is//skrar/image/HKT367/COR-CMD32GX4M4B2410_370_370_2.png"
}

#Session kóði hér fyrir neðan, er alltaf eins, þurfum ekkert að spá í þessu...
session_opts = {
    'session.type': 'file',
    # 'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)
#Eiginlegur Session kóði hér fyrir ofan...

def shopInfo(product=None):
    sesh = request.environ.get('beaker.session')
    sesh['counter'] = sesh.get('counter', 0) + 1
    sesh.save()
    ans = []
    if product == "page":
        for x in [[key, value] for key, value in dict(request.environ.get('beaker.session')).items()]:
            ans += ([[str(x[0]), str(x[1])]]) if x[0] != "_accessed_time" and x[0] != "_creation_time" and x[0] != "counter" else []
    return template("products", counter=sesh["counter"], product=product, page=ans, heads=heads, pics=pics)

@route("/products")
def products():
    return shopInfo()
@route("/products", method="POST")
def productPost():
    sesh = request.environ.get('beaker.session')
    sesh[request.forms.get("product")] = sesh.get(request.forms.get("product"), 0) + 1
    return shopInfo()
@route("/products/cpu")
def cpu():
    return shopInfo("cpu")
@route("/products/gpu")
def gpu():
    return shopInfo("gpu")
@route("/products/mobo")
def mobo():
    return shopInfo("mobo")
@route("/products/mem")
def mem():
    return shopInfo("mem")
@route("/cart")
def cart():
    rem = request.query.get("rem")
    if rem != None:
        sesh = request.environ.get('beaker.session')
        sesh[rem] = sesh.get(rem) - 1
    return shopInfo("page")
@error(404)
def e(err):
    return "Þessi síða er ekki til"
if os.environ.get("IS_HEROKU") is not None:
    run(host="0.0.0.0", port=os.environ.get("PORT"), app=app)
else:
    run(app=app)#þessi aðeins öðruvísi...

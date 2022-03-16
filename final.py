from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname
import folium
import pandas as pd
from folium.plugins import MeasureControl








app = Flask(__name__)
app.secret_key="final"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/atageomatic/nice2/final.db'

db = SQLAlchemy(app)


def create_map(lati_list,longi_list,title_list,height_list,type_list):
    try:
        int_lat = [float(i) for i in lati_list]
        int_long = [float(i) for i in longi_list]

        # Make a data frame with dots to show on the map
        data = pd.DataFrame({
                'lat': int_long,
                'lon': int_lat,
                'title': title_list,
                'height': height_list,
                'type': type_list,
            })


            # Make an empty map
        m = folium.Map(
                location=[data.iloc[0]['lon'], data.iloc[0]['lat']],
                control_scale=True,
                zoom_start=5
            )
        m.add_child(folium.LatLngPopup())

        for i in range(len(data)):
            html = """
                                        <h1 style="color:green;"> %s</h1><br>
                                        <p>
                                        <code>
                                            Lat: %s<br>
                                            Long: %s<br>
                                        </code>
                                        Height : %s .m<br>
                                        Entered by: %s
                                        </p>
                                        """ % ((data.iloc[i]['type']),(data.iloc[i]['lon']),(data.iloc[i]['lat']),(data.iloc[i]['height']), (data.iloc[i]['title']))

            folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']],
                              popup=html,
                              tooltip="Get İnfo"
                              ).add_to(m)

        folium.raster_layers.TileLayer(  # Farklı tür harita desenleri
                tiles='http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr='google',
                name='google maps',
                max_zoom=20,
                subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                overlay=False,
                control=True,
            ).add_to(m)
        folium.raster_layers.TileLayer(
                tiles='http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                attr='google',
                name='google street view',
                max_zoom=20,
                subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                overlay=False,
                control=True,
            ).add_to(m)
        folium.LayerControl().add_to(m)
        m.add_child(MeasureControl())  # Mesafe ve Alan ölçer

            # Save it as html
        m.save('/home/atageomatic/nice2/templates/mapper.html')
            #newPath = shutil.copy('mapper.html', '/home/atageomatic/nice2/templates/mapper54.html')
    except IndexError:
        pass

@app.route('/sena-kalp-ben')
def sena ():
    return render_template("sena.html")

@app.route('/iletisim')
def iletisim ():
    return render_template("iletisim.html")

@app.route('/map')
def map():
    return render_template("mapper.html")



@app.route("/register",methods=["POST"])
def register():
    title = request.form.get("title")
    lati = request.form.get("lati")
    longi = request.form.get("longi")
    height = request.form.get("height")
    type = request.form.get("type")


    new_TodoList = [title,lati,longi,height,type]
    for i in new_TodoList:
        if i == "sena":
            return redirect(url_for("sena"))
        elif i == "Choose...":
            type="Unspecified"
        elif i == "senailter":
            return redirect(url_for("sena"))
        elif i == "SENA":
            return redirect(url_for("sena"))
        elif i == "Sena":
            return redirect(url_for("sena"))
        elif i == "Senaİlter":
            return redirect(url_for("sena"))




    newTodo = Todo(title=title, lati=lati, longi=longi, height=height, type=type, complete=False)

    db.session.add(newTodo)
    db.session.commit()

    flash("Data Successfully Added", "success")




    return redirect(url_for("index"))


@app.route("/update/<string:id>")
def update(id):
    enrty= Todo.query.get((id))
    todos = list()
    todos.append(enrty.id)
    todos.append(enrty.title)
    todos.append(enrty.lati)
    todos.append(enrty.longi)
    todos.append(enrty.height)
    todos.append(enrty.type)


    title = request.form.get("title")
    lati = request.form.get("lati")
    longi = request.form.get("longi")
    height = request.form.get("height")
    type = request.form.get("type")

    newTodo = Todo(id=enrty.id,title=title, lati=lati, longi=longi, height=height, type=type, complete=False)

    toodo = Todo.query.filter_by(id=enrty.id).first()
    db.session.delete(toodo)
    db.session.commit()

    return render_template("update.html",todos=todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete

    db.session.commit()
    return redirect(url_for("update"))


@app.route("/delete/<string:id>")
def deleteToDo(id):
    toodo= Todo.query.filter_by(id=id).first()
    db.session.delete(toodo)
    db.session.commit()
    flash("Data Successfully Deleted", "danger")
    return redirect(url_for("index"))



@app.route("/")
def index():
    todos = Todo.query.all()  #Liste
    lati_list = []
    longi_list = []
    title_list = []
    height_list = []
    type_list = []
    for i in todos:
        lati_list.append(i.lati)
        longi_list.append(i.longi)
        title_list.append(i.title)
        height_list.append(i.height)
        type_list.append(i.type)


    create_map(lati_list,longi_list,title_list,height_list,type_list)
    return render_template("index.html",todos=todos)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    lati = db.Column(db.String(80))
    longi = db.Column(db.String(80))
    height = db.Column(db.String(80))
    type = db.Column(db.String(80))
    complete = db.Column(db.Boolean)




if __name__ == "__main__":
    db.create_all()
    if 'liveconsole' not in gethostname():
        app.run(debug=True)

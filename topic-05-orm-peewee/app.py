from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.initialize("pets.db")

# Creating Pet Routes

@app.route("/")
@app.route("/list")
def get_list():
    pets = database.get_pets()
    return render_template("list.html", pets=pets)


@app.route("/create", methods=["GET"])
def get_create():
    kinds = database.get_kinds()
    return render_template("create.html", kinds=kinds)


@app.route("/create", methods=["POST"])
def post_create():
    data = {
        "name": request.form.get("name", ""),
        "age": request.form.get("age", "0"),
        "kind_id": request.form.get("kind_id"), 
        "owner": request.form.get("owner", ""),
    }

    print("FORM DATA:", request.form)
    print("DATA DICT:", data)

    database.create_pet(data)
    return redirect(url_for("get_list"))



@app.route("/delete/<int:id>")
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for("get_list"))


@app.route("/update/<int:id>", methods=["GET"])
def get_update(id):
    pet = database.get_pet_by_id(id)
    if pet is None:
    
        return redirect(url_for("get_list"))
    return render_template("update.html", data=pet)


@app.route("/update/<int:id>", methods=["POST"])
def post_update(id):
    data = dict(request.form)  # {"name":..., "age":..., "type":..., "owner":...}
    database.update_pet(id, data)
    return redirect(url_for("get_list"))

# create kind routes

@app.route("/kind")
@app.route("/kind/list")
def get_kind_list():
    kinds = database.get_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/kind/create", methods=["GET"])
def get_kind_create():
    return render_template("kind_create.html")


@app.route("/kind/create", methods=["POST"])
def post_kind_create():
    data = dict(request.form)  # {"name":..., "food":..., "sound":...}
    database.create_kind(data)
    return redirect(url_for("get_kind_list"))


@app.route("/kind/delete/<int:id>")
def get_kind_delete(id):
    try:
        database.delete_kind(id)
        return redirect(url_for("get_kind_list"))
    except Exception as e:
        return render_template("error.html", error_text=str(e))


@app.route("/kind/update/<int:id>", methods=["GET"])
def get_kind_update(id):
    kind = database.get_kind_by_id(id)
    if kind is None:
        return redirect(url_for("get_kind_list"))
    return render_template("kind_update.html", data=kind)


@app.route("/kind/update/<int:id>", methods=["POST"])
def post_kind_update(id):
    data = dict(request.form)  # {"name":..., "food":..., "sound":...}
    database.update_kind(id, data)
    return redirect(url_for("get_kind_list"))

if __name__ == "__main__":
    app.run(debug=True)

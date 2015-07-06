from flask import render_template, flash, request
from app import app, db, models
from .forms import BeerForm, KegForm

@app.route('/')
@app.route('/index')
def index():
    beer = {"Name": "Bud Light"}
    return render_template('index.html',
            beer=beer)

@app.route('/beers')
def beers():
    return render_template('beers.html',
            beers=sorted(models.Beer.query.all(), key=lambda x: x.name,
                reverse=False))

def update_beer(form, beer):
    beer.abv=form.abv.data
    beer.ba_score=form.ba_score.data
    beer.brewer=form.brewer.data
    beer.isi_score=form.isi_score.data
    beer.link=form.link.data
    beer.name=form.name.data
    beer.style=form.style.data
    return beer

@app.route('/beer/<id>', methods=['GET', 'POST'])
def beer(id):
    form = BeerForm()
    if id ==  "add":
        if form.validate_on_submit():
            newbeer = update_beer(form, models.Beer())
            db.session.add(newbeer)
            db.session.commit()
            flash('{0} created'.format(newbeer))
            form.populate_obj(newbeer)
            return render_template('beer.html',
                    id=newbeer.id,
                    form=form)
        else:
            return render_template('beer.html',
                    beer=None,
                    form=form)
    # we are updating not adding
    else:
        beer = models.Beer.query.get(id)
        if beer == None:
            # beer does not exist
            return render_template('404.html'), 404
        else:
            form = BeerForm(obj=beer)
            if form.validate_on_submit():
                newbeer = update_beer(form, beer)
                form.populate_obj(beer)
                db.session.commit()
                flash('{0} updated'.format(beer))

            return render_template('beer.html',
                    beer=beer,
                    form=form)

@app.route('/kegs')
def kegs():
    return render_template('kegs.html',
            kegs=sorted(models.Keg.query.all()))

def update_keg(keg):
    print(keg)
    return

@app.route('/keg/<id>', methods=['GET', 'POST'])
def keg(id):
    if id == "add":
        keg = models.Keg()
    else:
        keg = models.Keg.query.get(id)

    form = KegForm(obj=keg)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("HERE")
        update_keg(keg)

    return render_template('keg.html',
            form=form)

@app.route('/kegerators')
def kegerators():
    kegerators = ["kegera", "kegerb", "kegerc"]
    return render_template('kegerators.html',
            kegerators=kegerators)

@app.route('/kegerator/<id>')
def kegerator(id):
    kegerator = ["kegera", "kegerb", "kegerc"]
    return render_template('kegerator.html',
            kegerator=kegerator[int(id)])

@app.route('/floors')
def floors():
    floors = ["floora", "floorb", "floorc"]
    return render_template('floors.html',
            floors=floors)

@app.route('/floor/<id>')
def floor(id):
    floors = ["floora", "floorb", "floorc"]
    return render_template('floor.html',
            floor=floors[int(id)])

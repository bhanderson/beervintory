from flask import render_template, flash, request
from app import app, db, models
from .forms import BeerForm, KegForm, KegeratorForm, FloorForm

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
            kegs=sorted(models.Keg.query.all(), key=lambda x: x.beer.name,
                reverse=False))

@app.route('/keg/<id>', methods=['GET', 'POST'])
def keg(id):
    if id == "add":
        keg = models.Keg()
    else:
        keg = models.Keg.query.get(id)

    form = KegForm(obj=keg)
    form.beer.beer=keg.beer_id
    if form.validate_on_submit():
        keg.beer_id = form.beer.data
        keg.chilled = form.chilled.data
        keg.filled = form.filled.data
        keg.tapped = form.tapped.data
        db.session.add(keg)
        db.session.commit()

    return render_template('keg.html',
            form=form,
            keg=keg)

@app.route('/kegerators')
def kegerators():
    return render_template('kegerators.html',
            kegerators=sorted(models.Kegerator.query.all(), key=lambda x:
                x.name, reverse=False))

@app.route('/kegerator/<id>', methods=['GET', 'POST'])
def kegerator(id):
    if id == "add":
        kegerator = models.Kegerator()
    else:
        kegerator = models.Kegerator.query.get(id)

    form = KegeratorForm(obj=kegerator)
    if form.validate_on_submit():
        kegerator.co2 = form.co2.data
        kegerator.floor = form.floor.data
        kegerator.name = form.name.data
        db.session.add(kegerator)
        db.session.commit()

    return render_template('kegerator.html',
            form=form)

@app.route('/floors')
def floors():
    return render_template('floors.html',
            floors=sorted(models.Floor.query.all(), key=lambda x: x.number,
                reverse=False))

@app.route('/floor/<id>', methods=['GET', 'POST'])
def floor(id):
    if id == "add":
        floor = models.Floor()
    else:
        floor = models.Floor.query.get(id)

    form = FloorForm(obj=floor)
    if form.validate_on_submit():
        floor.number = form.number.data
        floor.kegerators = form.kegerators.data
        db.session.add(floor)
        db.session.commit()

    return render_template('floor.html',
            floor=floor,
            form=form)

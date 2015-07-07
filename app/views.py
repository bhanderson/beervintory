from flask import render_template, flash, request
from app import app, db, models
from .forms import BeerForm, KegForm, KegeratorForm, FloorForm

@app.route('/')
@app.route('/index')
def index():
    floors = models.Floor.query.all()
    kegerators = models.Kegerator.query.all()
    kegs = models.Keg.query.all()
    beers = models.Beer.query.all()
    return render_template('index.html',
            floors=floors,
            kegerators=kegerators,
            kegs=kegs,
            beers=beers)

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
    if id == "add":
        beer = models.Beer()
    else:
        beer = models.Beer.query.get(id)
        if beer == None:
            return render_template('404.html'), 404
        else:
            form.obj = beer

    if form.validate_on_submit():
        beer.abv=form.abv.data
        beer.ba_score=form.ba_score.data
        beer.brewer=form.brewer.data
        beer.isi_score=form.isi_score.data
        beer.link=form.link.data
        beer.name=form.name.data
        beer.style=form.style.data
        if id == "add":
            db.session.add(beer)
        db.session.commit()
        flash(beer)
    return render_template('beer.html',
            form=form,
            beer=beer)

@app.route('/kegs')
def kegs():
    return render_template('kegs.html',
            kegs=sorted(models.Keg.query.all(), key=lambda x: x.beer.name,
                reverse=False))

@app.route('/keg/<id>', methods=['GET', 'POST'])
def keg(id):
    form = KegForm()
    beers = models.Beer.query.all()
    form.beer.choices = [(b.id, b.__repr__()) for b in beers]
    if id == "add":
        keg = models.Keg()
    else:
        keg = models.Keg.query.get(id)
        if keg == None:
            return render_template('404.html'), 404

    if form.validate_on_submit():
        keg.beer_id = int(form.beer.data)
        keg.chilled = form.chilled.data
        keg.filled = form.filled.data
        keg.tapped = form.tapped.data
        if id == "add":
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
    form = KegeratorForm()
    floors = models.Floor.query.all()
    form.floor.choices = [(f.id, f.__repr__()) for f in floors]
    kegs = models.Keg.query.all()
    form.keg.choices = [(k.id, k.__repr__()) for k in kegs]
    if id == "add":
        kegerator = models.Kegerator()
    else:
        kegerator = models.Kegerator.query.get(id)
        if kegerator == None:
            return render_template('404.html'), 404
        else:
            form.obj = kegerator

    if form.validate_on_submit():
        kegerator.co2 = form.co2.data
        kegerator.keg_id = form.keg.data
        kegerator.floor_id = form.floor.data
        kegerator.name = form.name.data
        if id == "add":
            db.session.add(kegerator)
        db.session.commit()

    return render_template('kegerator.html',
            form=form,
            kegerator=kegerator)

@app.route('/floors')
def floors():
    return render_template('floors.html',
            floors=sorted(models.Floor.query.all(), key=lambda x: x.number,
                reverse=False))

@app.route('/floor/<id>', methods=['GET', 'POST'])
def floor(id):
    form = FloorForm()
    kegerators = models.Kegerator.query.all()
    form.kegerators.choices = [(k.id, k.__repr__()) for k in kegerators]
    if id == "add":
        floor = models.Floor()
    else:
        floor = models.Floor.query.get(id)
        if floor == None:
            return render_template('404.html'), 404

    if form.validate_on_submit():
        floor.number = form.number.data
        floor.kegerators = form.kegerators.data
        if id == "add":
            db.session.add(floor)
        db.session.commit()

    return render_template('floor.html',
            floor=floor,
            form=form)

from app import db

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kegerators = db.relationship("Kegerator", backref="floor")
    number = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        s = ['st','nd','rd','th']
        suffix = s[0]
        if self.number > 3:
            suffix = s[3]
        else:
            suffix = s[self.number-1]
        return "{0}{1}".format(self.number, suffix)

class Kegerator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clean_date = db.Column(db.Date)
    co2 = db.Column(db.Boolean)
    keg_id = db.Column(db.Integer, db.ForeignKey('keg.id'))
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'))
    name = db.Column(db.String(32))

    def __repr__(self):
        return 'Kegerator {0}>'.format(self.name)

class Keg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beer_id  = db.Column(db.Integer, db.ForeignKey('beer.id'))
    chilled = db.Column(db.Boolean)
    filled = db.Column(db.Boolean)
    kegerator = db.relationship('Kegerator', backref='keg')
    tapped = db.Column(db.Boolean)

    def __repr__(self):
        cold = "Warm"
        full = "Empty"
        if self.chilled:
            cold = "Cold"
        if self.filled:
            full = "Full"
        beer = Beer.query.get(self.beer_id)

        return '{0} {1} | {2}, {3}'.format(beer.name, beer.style, full,
                cold)

class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abv = db.Column(db.Float(precision=4))
    ba_score = db.Column(db.Integer)
    brewer = db.Column(db.String(64), index=True)
    isi_score = db.Column(db.Integer)
    keg = db.relationship('Keg', backref='beer')
    link = db.Column(db.String(128))
    name = db.Column(db.String(64), index=True)
    style = db.Column(db.String(64), index=True)

    def __repr__(self):
        return "<{0} {1} | {2}>".format(self.name, self.style, self.brewer)

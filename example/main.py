# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pyuploadcare_sqlalchemy import ImageType
from pyuploadcare import conf

app = Flask(__name__)
conf.pub_key = 'demopublickey'
conf.secret = 'demoprivatekey'

Base = declarative_base()


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)
    photo = Column(ImageType(effects='-/resize/x100/'))


engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    session = Session()
    items = session.query(Photo).all()
    session.close()
    return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_photo():
    session = Session()

    photo = Photo(photo=request.form['my_file'])
    session.add(photo)
    session.commit()
    session.close()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)

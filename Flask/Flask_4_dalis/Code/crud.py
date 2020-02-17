from app import db, Book, Publisher

pub1 = Publisher('Baltos Lankos')
db.session.add(pub1)
db.session.commit()
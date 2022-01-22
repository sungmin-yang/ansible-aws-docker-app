from app import db, Students

db.create_all()


test_rec = Students(
        'Marco Hemken',
        'Los Angeles',
        '123 Foobar Ave',
        '12345'
        )


db.session.add(test_rec)
db.session.commit()

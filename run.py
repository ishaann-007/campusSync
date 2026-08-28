from app import create_app, db
from app.models import User, Department, Issue, Assignment
from seed import seed_data

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    seed_data()
    app.run(debug=True)


from my_flask import create_app, db
import json
from my_flask.models import Customer


app = create_app()
db.create_all(app=app)

# with app.app_context():
#     with open("C:/Users/eco/Downloads/MOCK_DATA.json") as f:
#         data = json.load(f)
#         for c in data:
#             customer = Customer(
#                 first_name=c["first_name"],
#                 last_name=c["last_name"],
#                 email=c["email"],
#                 user_id=c["user_id"],
#             )
#             db.session.add(customer)

#         db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

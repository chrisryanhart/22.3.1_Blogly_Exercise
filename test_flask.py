from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test cases for flask routes"""

    def setUp(self):
        User.query.delete()

        user = User(first_name='Petry',last_name='Jones',image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX_FJrccL0udXqC4zEjHTBxpDZl7zztfrlmA&usqp=CAU')
    
        db.session.add(user)
        db.session.commit()

        self.user_id=user.id
        self.image_url=user.image_url

    def tearDown(self):
        db.session.rollback()

    
    def test_post_new_user(self):
        with app.test_client() as client:
            d={"first_name":'bobby', 'last_name':'sue', 'image_url':'https://upload.wikimedia.org/wikipedia/commons/a/ae/Jimi_Hendrix_1967.png'}
            resp = client.post('/users/new',data=d,follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('bobby sue',html)

    def test_show_all_users(self):
        with app.test_client() as client:
            resp=client.get('/users')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Petry Jones', html)


    # @app.route('/users/<int:user_id>')
    def test_show_user_info(self):
        with app.test_client() as client:
            resp=client.get(f'/users/{self.user_id}')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("<h3>Petry Jones</h3>",html)

        # """Show infor about given user
        # -have button to edit/delete user
        # """
        # user = User.query.get(user_id)

        # return render_template('userInfo.html', user=user)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user_id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('Petry Jones',html)


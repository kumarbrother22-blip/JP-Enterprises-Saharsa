import os
import tempfile
import unittest

from app import create_app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app(
            {
                'TESTING': True,
                'SECRET_KEY': 'test',
                'DATABASE': self.db_path,
                'ADMIN_USERNAME': 'admin',
                'ADMIN_PASSWORD': 'jp@2022',
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Trusted Mobile Store in Saharsa', response.data)

    def test_admin_login_and_add_product(self):
        login_response = self.client.post(
            '/admin/login',
            data={'username': 'admin', 'password': 'jp@2022'},
            follow_redirects=True,
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(b'Inventory Admin Panel', login_response.data)

        add_response = self.client.post(
            '/admin/products/add',
            data={
                'name': 'Test Device',
                'category': 'Samsung',
                'price': '₹9,999',
                'condition': 'New',
                'image_url': 'https://example.com/image.jpg',
            },
            follow_redirects=True,
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertIn(b'Product added successfully.', add_response.data)


if __name__ == '__main__':
    unittest.main()

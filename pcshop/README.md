# PC Hardware Shop

A modern e-commerce website for selling computer hardware, built with Django.

## Features

- **Home Page**: Clean and professional design with categories, featured products, and special offers.
- **Category Selection**: Browse products by categories and companies/brands.
- **Product Pages**: Detailed product information with multiple images, specifications, and reviews.
- **Shopping Cart**: Add products to cart, update quantities, and proceed to checkout.
- **Checkout Process**: User-friendly checkout with shipping and payment options.
- **User Authentication**: Sign-up, login, and user dashboard.
- **Responsive Design**: Mobile-friendly interface for all devices.
- **Compatibility Checker**: Tool to check if components are compatible with each other.

## Technology Stack

- **Backend**: Django 5.1
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Additional Libraries**: jQuery, Font Awesome

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pcshop.git
   cd pcshop
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the site at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/

## Project Structure

- `pcapp/`: Main application directory
  - `models.py`: Database models
  - `views.py`: View functions
  - `urls.py`: URL patterns
  - `forms.py`: Form classes
  - `admin.py`: Admin site configuration
  - `templates/`: HTML templates
  - `static/`: Static files (CSS, JS, images)
- `pcshop/`: Project settings directory
  - `settings.py`: Project settings
  - `urls.py`: Main URL configuration
- `media/`: User-uploaded files
- `static/`: Project-wide static files

## Usage

1. Access the admin panel to add categories, companies, and products.
2. Upload product images and set prices, discounts, and specifications.
3. Users can browse products, add them to cart, and place orders.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design
- Font Awesome for the icons
- Django community for the excellent documentation 
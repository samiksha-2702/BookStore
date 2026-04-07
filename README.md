<div align="center">

# 📚 BiblioCart

### A Full-Stack Django E-Commerce Platform for Books

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Razorpay](https://img.shields.io/badge/Razorpay-Payment%20Gateway-02042B?style=flat-square&logo=razorpay&logoColor=white)](https://razorpay.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Demo](https://img.shields.io/badge/Demo-Coming%20Soon-orange?style=flat-square)](#)

<br/>

> BiblioCart is a full-stack e-commerce web application for buying books online.  
> Browse books, manage your cart, pay securely, and track every order — all in one place.

<br/>

[Overview](#-overview) · [Features](#-features) · [Tech Stack](#-tech-stack) · [Architecture](#-architecture) · [Installation](#-installation) · [Project Structure](#-project-structure) · [Screenshots](#-screenshots) · [Future Improvements](#-future-improvements) · [Author](#-author)

</div>

---

## 🧭 Overview

BiblioCart is a real-world e-commerce platform built with Django, targeting book lovers and readers. It implements a complete end-to-end purchase workflow — from browsing and searching books to placing an order and tracking its delivery status.

This project demonstrates practical full-stack development skills including backend architecture, payment gateway integration, order lifecycle management, and a responsive, user-friendly interface.

---

## ✨ Features

### 🔐 Authentication
- User registration, login, and logout
- Session-based secure access
- User-specific data isolation (orders, cart, history)

### 📖 Books & Browsing
- Browse the full book catalog
- Search books by title, author, or category
- Detailed book view with description and pricing
- Curated bestsellers listing

### 🛒 Cart Management
- Add books to the cart and update quantities
- Remove items individually
- Real-time cart summary with price calculation via custom template filters

### 💳 Checkout & Payments
- Streamlined checkout flow
- **Razorpay integration** (test mode) for secure payment processing
- Order creation and storage on successful payment

### 📦 Order Management
- Order history dashboard per user
- Detailed order view with itemized summary
- Order tracking with visual status progression:

  ```
  Pending → Processing → Shipped → Completed
                                 ↘ Cancelled
  ```

### 🧾 Invoice
- Invoice download for completed orders

### 📱 Responsive UI
- Built with Bootstrap 5
- Mobile-friendly layout across all pages

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Django |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | SQLite (default) · MySQL (configurable) |
| **Payment** | Razorpay (Test Mode) |
| **Version Control** | Git & GitHub |

---

## 🏗 Architecture

BiblioCart follows Django's modular app pattern for clean separation of concerns:

```
bibliocart/
│
├── books/          # Book catalog, browsing, search
├── cart/           # Cart logic, session management
├── orders/         # Order creation, tracking, history
├── users/          # Authentication, profile
│
├── templates/      # HTML templates (per-app + shared base)
├── static/         # CSS, JS, images
├── media/          # Uploaded book covers
│
├── bibliocart/     # Project settings, URLs, WSGI
└── manage.py
```

**Key architectural decisions:**
- Django ORM for all database interactions — no raw SQL
- Template-based rendering for clean server-side HTML
- Custom template filters for dynamic price calculations (e.g., `quantity × price`)
- User-scoped querysets to prevent unauthorized order access
- Razorpay's JS SDK integrated at the frontend, verified server-side

---

## ⚙️ Installation

Follow these steps to run BiblioCart locally.

### Prerequisites

- Python 3.10+
- pip
- Git
- A [Razorpay](https://razorpay.com) account (for test API keys)

### 1. Clone the Repository

```bash
git clone https://github.com/samiksha-2702/bibliocart.git
cd bibliocart
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

> ⚠️ Never commit your `.env` file. It is already included in `.gitignore`.

### 5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

### 7. (Optional) Load Sample Data

```bash
python manage.py loaddata books_sample.json
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 🗂 Project Structure

```
bibliocart/
│
├── bookstore/
│   └── settings.py
│
├── books/
│   ├── models.py              # Book model (title, author, price, cover, etc.)
│   ├── views.py               # Book listing, search, detail views
│   └── urls.py
│
├── cart/
│   ├── views.py               # Add, update, remove cart items
│   ├── templatetags/          # Custom template filters (e.g. quantity × price)
│   └── context_processors.py  # Cart count available globally
│
├── orders/
│   ├── models.py              # Order, OrderItem models with status tracking
│   ├── views.py               # Checkout, order history, order detail, tracking
│   └── urls.py
│
├── users/
│   ├── views.py               # Register, login, logout
│   └── forms.py
│
├── templates/
│   ├── base.html                  # Shared layout, navbar, footer
│   ├── books/
│   │   ├── book_list.html         # Full book catalog with search
│   │   ├── book_detail.html       # Individual book page with add to cart
│   │   └── bestseller.html        # Curated bestsellers listing
│   ├── accounts/
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   ├── cart/
│   │   └── cart.html              # Cart items, quantities, subtotal
│   └── orders/
│       ├── checkout.html
│       ├── payment.html           # Razorpay payment trigger page
│       ├── order_success.html
│       ├── order_history.html
│       └── track_order.html       # Visual status progress tracker
│
├── static/
│   ├── css/
│   └── js/
│
├── bibliocart/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── manage.py
```

---

## 📸 Screenshots

### 🏠 Home Page (Light)
![Home Light](screenshots/home-white.png)

### 🌙 Home Page (Dark)
![Home Dark](screenshots/home-dark.png)

### 🔐 Signup
![Signup](screenshots/signup.png)

### 🔐 Login
![Login](screenshots/login.png)

### 👤 Profile
![Profile](screenshots/profile.png)

### 🛒 Cart
![Cart](screenshots/cart.png)

### 🏁 Checkout
![Checkout](screenshots/checkout.png)

### 💳 Payment Detail
![Payment](screenshots/payment.png)

### 💰 Razorpay Gateway
![Razorpay](screenshots/razorpay2.png)

### ✅ Order Successful
![Order Success](screenshots/successful.png)

### 📦 Track Order
![Track Order](screenshots/track-orders.png)

### ⭐ Bestsellers
![Bestsellers](screenshots/bestseller.png)

---

## 🔮 Future Improvements

- [ ] Deploy to [Railway](https://railway.app) or [Render](https://render.com) with a live demo URL
- [ ] Switch production database to **PostgreSQL or MySQL**
- [ ] Add **book reviews and ratings** system
- [ ] Implement **wishlist** functionality
- [ ] Build **admin dashboard** for inventory and order management
- [ ] Introduce **discount codes and coupons**
- [ ] Integrate **email notifications** for order updates
- [ ] Add **pagination** to book listings
- [ ] Write unit and integration **tests** for core modules
- [ ] Implement a **REST API** layer using Django REST Framework

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👩‍💻 Author

**Samiksha**  
Final Year MCA Student · Django Backend Developer

[![GitHub](https://img.shields.io/badge/GitHub-samiksha--2702-181717?style=flat-square&logo=github)](https://github.com/samiksha-2702)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/your-linkedin)

---

<div align="center">

⭐ If you found this project useful, give it a star — it means a lot!

</div>
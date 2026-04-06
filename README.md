<div align="center">

# 📚 BiblioCart

### A Full-Stack Django E-Commerce Platform for Books

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Razorpay](https://img.shields.io/badge/Razorpay-Payment%20Gateway-02042B?style=flat-square&logo=razorpay&logoColor=white)](https://razorpay.com)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20%2F%20MySQL-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

<br/>

> BiblioCart is a full-stack e-commerce web application designed for buying and selling books online.  
> Browse books, manage your cart, pay securely, and track every order — all in one place.

<br/>

[Features](#-features) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [Project Structure](#-project-structure) · [Screenshots](#-screenshots) · [Future Improvements](#-future-improvements) · [Author](#-author)

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
- User-specific data isolation (orders, history)

### 📖 Books & Browsing
- Browse the full book catalog
- Search books by title, author, or category
- Detailed book view with description and pricing

### 🛒 Cart Management
- Add books to the cart
- Update quantities and remove items
- Real-time cart summary with price calculation (via custom template filters)

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
- Optional invoice download for completed orders

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

Create a `.env` file in the project root and add the following:

```env
SECRET_KEY=your_django_secret_key

DEBUG=True

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

> ⚠️ Never commit your `.env` file. It is included in `.gitignore` by default.

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
├── books/
│   ├── models.py          # Book model (title, author, price, cover, etc.)
│   ├── views.py           # Book listing, search, detail views
│   ├── urls.py
│   └── templates/books/
│
├── cart/
│   ├── views.py           # Add, update, remove cart items
│   ├── context_processors.py  # Cart count available globally
│   └── templates/cart/
│
├── orders/
│   ├── models.py          # Order, OrderItem models with status tracking
│   ├── views.py           # Checkout, order history, order detail, tracking
│   ├── urls.py
│   └── templates/orders/
│
├── users/
│   ├── views.py           # Register, login, logout
│   ├── forms.py
│   └── templates/users/
│
├── templates/
│   ├── base.html                  # Shared layout, navbar, footer
│   ├── accounts/
│   │   ├── login.html             # User login page
│   │   ├── signup.html            # User registration page
│   │   ├── profile.html           # View user profile
│   │   └── edit_profile.html      # Edit profile details
│   ├── cart/
│   │   └── cart.html              # Cart items, quantities, subtotal
│   └── orders/
│       ├── checkout.html          # Checkout form
│       ├── payment.html           # Razorpay payment trigger page
│       ├── order_success.html     # Post-payment confirmation
│       ├── order_history.html     # List of all past orders
│       └── track_order.html       # Order status progress tracker
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

> 🚧 Live screenshots will be added after deployment. The following screens are available in the application:

<br/>

<div align="center">

<!-- SCREENSHOT GUIDE:
  To add screenshots:
  1. Create a folder: /docs/screenshots/
  2. Add your images there (e.g., home.png, cart.png, etc.)
  3. Replace each placeholder block below with:
     <img src="docs/screenshots/your-image.png" alt="Page Name" width="100%" />
-->

| 🏠 Home — Book Listing | 📖 Book Detail |
|:---:|:---:|
| ![Home](https://placehold.co/600x380/1a1a2e/ffffff?text=Home+%E2%80%94+Book+Listing&font=lato) | ![Book Detail](https://placehold.co/600x380/16213e/ffffff?text=Book+Detail+Page&font=lato) |
| Browse and search the full catalog | View description, price, and add to cart |

<br/>

| 🛒 Cart | 💳 Checkout & Razorpay |
|:---:|:---:|
| ![Cart](https://placehold.co/600x380/0f3460/ffffff?text=Cart+Management&font=lato) | ![Checkout](https://placehold.co/600x380/533483/ffffff?text=Checkout+%2B+Razorpay&font=lato) |
| Manage items and view subtotal | Secure payment via Razorpay (test mode) |

<br/>

| 📦 Order History | 🔍 Order Tracking |
|:---:|:---:|
| ![Order History](https://placehold.co/600x380/1b4332/ffffff?text=Order+History&font=lato) | ![Order Tracking](https://placehold.co/600x380/1d3557/ffffff?text=Order+Tracking+%E2%80%94+Status+Progress&font=lato) |
| View all past orders per user | Visual status bar: Pending → Shipped → Completed |

</div>

<br/>

> 💡 **Want to see it in action?** Clone the repo, run locally, and explore all screens.  
> Deployment coming soon on [Railway](https://railway.app) / [Render](https://render.com).

---

## 🔮 Future Improvements

- [ ] Deploy to [Railway](https://railway.app) or [Render](https://render.com) with a live demo URL
- [ ] Switch production database from SQLite to **PostgreSQL or MySQL**
- [ ] Add **book reviews and ratings** system
- [ ] Implement **wishlist** functionality
- [ ] Add **admin dashboard** for inventory and order management
- [ ] Introduce **discount codes and coupons**
- [ ] Integrate **email notifications** for order updates
- [ ] Add **pagination** to book listings
- [ ] Write unit and integration **tests** for core modules
- [ ] Implement **REST API** layer using Django REST Framework

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
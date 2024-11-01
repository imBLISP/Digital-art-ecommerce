# Vinfei

**An eCommerce website for individuals passionate about digital artwork and supporting artists**

## Key Features

### User Management

- Login/signup with **email link authentication**.
- The website supports **persistent cookies** and **session cookies**.

### Buy Digital Art

- Purchase digital art by visiting the art page (*email authentication required*).
- Payments require a card and use the **Stripe API** to handle transactions.
- Utilizes a **webhook** to update/add purchase information to the database and manage artwork transactions.

### Sell Digital Art

- Create digital art cards and **upload your own art** on the profile page using **responsive cards** that adjust to form changes, allowing you to preview what your art will look like on the front page (*email authentication required*).
- Artwork is **converted to low quality** for thumbnails to prevent users from downloading the full-resolution artwork without purchase.

### Art Ownership

- Once purchased, users can **download the full resolution** of the artwork.
- Users can resell the artwork by creating a new card.

### Security

Features implemented to enhance security:

- **SQLAlchemy** to prevent SQL injections.
- **Werkzeug utilities** to protect against cross-site scripting, injections, etc.
- **Password hashing** for the database.
- **Email authentication link** using email hashing.
- **Webhooks** to validate purchases and update the database.

## Tools

**Frontend**

- HTML/CSS/JavaScript
- Bootstrap
- jQuery, Popper.js
- Sass

**Backend**

- Python backend framework: **Flask**
- Database: **SQLite**
- WTForms, SQLAlchemy, Werkzeug utilities
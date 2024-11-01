# Vinfei



>   This repo doesn't house the assets used to build the vinfei website

Available on heroku at https://vinfeii.herokuapp.com/

**Ecommerce website for people passionate about digital artworks and supporting artists**



## Key features



### User Management

Login/signup with **email link authentication** 

Website supports **Persistent cookies** and **session cookies** 



### Buy digital art

Buy digital art by visiting artpage, *email authentication required*

Payments require card and use **stripe api** to handle transactions

Uses a **Webhook** to update/add purchase information to database and handle the artwork transaction 



### Sell digital art

Make digital art cards and **upload your own art** on the profile page utilizing **responsive cards** that respond to changes in forms to accurately see what your art will look like on the front page, *email authentication required*

Artwork gets **converted to low quality** for thumbnails to prevent users from downloading the full resolution artwork without purchasing the artwork



### Art ownership

Once bought, a user can **download** **the full resolution** of the artwork 

Users can put the artwork on sale again if they wish by making a new card



### Security

Features implemented to improve security :

-   SQLAlchemy to prevent SQL injections
-   Werkzeug utilities to prevent Cross-site scripting, Injections etc
-   Password hashing for database
-   Email authentication link using email hashing
-   Webhooks to validate purchases and adding information to database



## Tools



**Frontend** 

-   HTML/CSS/Javascript

-   Bootstrap

-   JQuery, Popper.js

-   Sass

    

**Backend**

-   Python backend framework : **Flask**
-   Database : **SQLite**
-   Wtforms, sqlalchemy, werkzeug utilities




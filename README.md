# Portfolio Website - Jacob Folsom

## Overview

This project is a personal portfolio website for Jacob Folsom, a full-stack developer and cybersecurity professional. It serves as a central hub to showcase my projects, skills, and experiences. The website features an admin dashboard for managing projects, including adding, editing, and deleting projects, along with displaying those on the public-facing portfolio. It also includes sections for an "About Me" and "Contact" page.

## Features

- **Responsive Design**: The website is fully responsive and adapts to various screen sizes, from desktop to mobile.
- **Admin Dashboard**: The dashboard is protected by JWT-based authentication and allows the admin to manage projects dynamically.
- **Project Showcase**: Projects are dynamically loaded from the backend, with links to live demos and GitHub repositories.
- **File Uploads**: Admin can upload images for projects through the dashboard interface.
- **Authentication**: Secure login with JWT tokens, stored in cookies, ensuring both flexibility and security for managing sessions.

## Technologies Used

### Frontend

- **HTML5/CSS3**: The website’s structure and design are built using modern HTML5 and CSS3. A custom responsive design ensures it looks great across different devices.
- **JavaScript**: Vanilla JavaScript is used to manage dynamic content loading (e.g., fetching projects from the backend API).
- **Font Awesome**: Icons are implemented using Font Awesome for a professional and consistent look.
- **Responsive Grid Layout**: Projects are displayed in a responsive grid layout to provide a clean, easy-to-navigate experience.

### Backend

- **Flask**: The backend of the application is built using Flask, a lightweight Python web framework.
- **Flask-SQLAlchemy**: SQLAlchemy is used as the ORM to handle database operations.
- **Flask-JWT-Extended**: JWT (JSON Web Tokens) are used for user authentication. Tokens are stored in both cookies and HTTP headers for secure communication.
- **SQLite**: Data is stored using an SQLite database for lightweight storage needs.
- **Flask Uploads**: Handles file uploads for images associated with the projects.
- **Flask Static Files**: CSS and JavaScript files are served as static files using Flask.

### Deployment

This website is intended to be deployed on a standard Flask-compatible environment. It is set up for easy integration with services like DigitalOcean or Heroku for hosting.

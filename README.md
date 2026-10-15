# Esraa's Developer Portfolio

A personal portfolio website built with Django to showcase my backend development projects, technical skills, and experience.

## About the Project

This portfolio provides an overview of my work as an aspiring Django Backend Developer. It presents my projects, the technologies I use, and links to my GitHub repositories.

## Features

- Display projects dynamically from the database.
- View detailed information about each project.
- Filter projects by category.
- Manage projects and categories through the Django Admin panel.
- Include GitHub repository links and optional live demos.
- Responsive layout for different screen sizes.

## Technologies Used

- Python
- Django
- Django Templates
- HTML5
- CSS3
- SQLite

## Project Structure

```text
esraa-portfolio/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/
│   ├── migrations/
│   ├── static/
│   │   └── portfolio/
│   │       └── style.css
│   ├── templates/
│   │   └── portfolio/
│   │       ├── home.html
│   │       └── project_detail.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── manage.py
└── README.md
```

## Getting Started

### Prerequisites

- Python 3
- pip

### Installation

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate to the project directory:

   ```bash
   cd esraa-portfolio
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment.

   **Windows PowerShell:**

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

5. Install Django:

   ```bash
   pip install django
   ```

6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

8. Open the following address in your browser:

   ```text
   http://127.0.0.1:8000/
   ```

## Future Improvements

- Deploy the portfolio online.
- Add more backend projects.
- Improve accessibility and responsive design.

## Author

**Esraa Al-abd Al-Majeed**

Aspiring Django Backend Developer

- GitHub: [EsRaaAlmajeed](https://github.com/EsRaaAlmajeed)
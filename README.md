# NRPU Backend

The **NRPU** (National Research Program for Universities) backend handles core operations and provides the foundation for managing research programs. This lightweight backend currently uses **Excel sheets** as the primary database for now, making it simple and accessible while maintaining essential functionality.

---

## Project Overview

The backend facilitates the seamless management of research projects and user data through role-based authentication and authorization. It includes tools to track, update, and manage research projects while relying on **Excel sheets** for data storage.

---

## Features

- **Project Management**:
    - CRUD operations for research project data.
    - Excel-based storage for ease of use and portability.
- **Data Handling**:
    - Import and export data to and from Excel files for reporting and analysis.

---

## Technologies Used

- **Framework**: Django, Django RestFramework
- **Libraries:** Numpy, Pandas,
- **Data Storage**: Excel sheets (managed with Python libraries like `pandas` or `openpyxl`)
- **Language**: Python

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.9 or later

### Installation Steps

1. Clone the repository:
    
    ```bash
    git clone https://github.com/{your-username}/nrpu.git
    cd nrpu
    ```
    
2. Create a virtual environment and activate it:
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3. Install dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. Set up necessary configurations (if any):
    - Ensure the Excel files for data storage are located in the appropriate directory (e.g., `Data/` folder).
    - Update file paths in the code if needed.
5. Run the development server:
    
    ```bash
    python manage.py runserver
    ```
    

---

## Folder Structure

```
Extraction/
├── Extraction/            # Project settings
├── apps/
│------  App according to need
├── Data/                  # Excel sheets for data storage
├── static/                # Static files
├── templates/             # HTML templates
└── README.md              # Project documentation

```

---

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature description"`.
4. Push the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.

---

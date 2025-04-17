# 🎤 Entertainment Management Platform

This is a full-stack web application designed for an entertainment company to manage artists, their investments, platform operations, and personalized roles. The system includes both backend APIs and frontend Streamlit views, supporting different personas in the entertainment ecosystem.

## 👥 Personas

The platform supports the following four roles, each with dedicated API routes and user views:

- 🎨 **Artist**: View schedules and personal performance details.
- 👔 **Artist Manager**: Manage artist data and contracts.
- 💼 **Investment Counsellor**: Analyze and modify investment records.
- 🧠 **Platform Manager**: Oversee system-wide data and platform decisions.

Each persona has access to specific backend routes implemented using RESTful APIs (GET, POST, DELETE, PUT) and is supported by corresponding frontend pages.

---

## 🧱 Project Structure

```
📁 api/
  ├── backend/
  │     ├── artist/
  │     ├── artist_manager/
  │     ├── investment/
  │     ├── ml_models/
  │     ├── platform_manager/
  │     ├── db_connection/
  │     └── rest_entry.py
  ├── backend_app.py
  ├── Dockerfile
  ├── requirements.txt
  └── .env / .env.template

📁 app/
  └── [Streamlit frontend for each persona]

📁 database-files/
  └── [SQL schemas + mock data]

README.md
docker-compose-testing.yaml
```

---

## 🚀 Features

- RESTful API for 4 different roles
- Frontend built with **Streamlit** for real-time interaction
- Database with pre-inserted **mock data** for testing
- Support for containerized deployment with **Docker**
- Modular folder structure for scalability

---

## ⚙️ Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/JolinW0613/25S-Project.git
cd 25S-Project

### 2. Set up the environment

Create a `.env` file or modify `.env.template` as needed.
OR
in VSCODE:
Use the instruction in the following sequence:

docker compose up -d
docker compose down db
docker compose up db -d
docker compose up --build

```bash
cp api/.env.template api/.env

### 3. Run backend API

```bash
cd api
pip install -r requirements.txt
python backend_app.py
```

### 4. Launch Streamlit frontend

```bash
cd app
streamlit run main.py
```

---

## 🧪 API Examples

Here are some example endpoints:

- `GET /artist/<id>/schedule` – View upcoming performances
- `POST /artist_manager/artist` – Add a new artist
- `DELETE /platform_manager/contract/<id>` – Remove a contract

More endpoints are available in each role’s subfolder under `api/backend/`.

---

## 🗃️ Database

The system uses a SQL-based database defined in `/database-files`, and includes:

- Artists & Contracts
- Investment Records
- Role-Specific Tables

Mock data is provided for testing API and frontend behavior.

---

## 🐳 Docker Support (Optional)

To run the entire stack in containers:

```bash
docker compose -f docker-compose-testing.yaml up
```

---

## 📌 Future Directions

- Add authentication & role-based access
- Integrate ML-based investment suggestions
- Improve UI/UX design in Streamlit
- Expand database coverage with real-world datasets

---

## 📄 License

MIT License. See `LICENSE` file for more info.

---

## ✨ Acknowledgements

- Built for NEU CS3200 (Summer 2024 Template)
- Inspired by real-world entertainment data systems

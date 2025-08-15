# UPA Pool League Backend

This is the backend service for the UPA Pool League Mobile App. It is built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

---

## 🔧 Tech Stack

- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **PostgreSQL** – Database
- **Alembic** – Migrations
- **Uvicorn** – ASGI Server
- **Pydantic** – Request/response schema validation
- **Bcrypt** – Password hashing
- **JWT** – Authentication

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py               # Entry point for FastAPI app
│   ├── models/               # SQLAlchemy models (User, Match, etc.)
│   ├── schemas/              # Pydantic models for request/response
│   ├── api/                  # API route handlers
│   ├── core/                 # Config, JWT utils, password hashing
│   └── databse/                # Database connection and initialization
├── alembic/                  # Migrations
├── .env                      # Environment variables
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/upa-pool-league-backend.git
cd upa-pool-league-backend
```

### 2. Set up Environment

Create a `.env` file in root:

```ini
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/upa_pool
JWT_SECRET_KEY=your-secret-key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
uvicorn app.main:app --reload
```

---

## 📦 API Modules

- `/auth/register` – Register new user
- `/auth/login` – Login user & return JWT
- `/matches/` – Get match schedules
- `/scores/` – Submit and view scores

---

## 🔒 Security

- Passwords hashed using `bcrypt`
- Endpoints protected with JWT Bearer Auth

---

## 🧪 Testing

Coming soon with `pytest` integration.

---

## 📄 License

### 👨‍💻 Maintained by Rajesh Dumpeti

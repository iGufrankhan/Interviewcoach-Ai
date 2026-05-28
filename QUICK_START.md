<div align="center">
  <h1>⚡ Quick Start Guide</h1>
  <p><i>Get Interview Coach AI up and running on your local machine in minutes.</i></p>
</div>

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed and ready:

- 🟢 **Node.js 18+** and **npm**
- 🐍 **Python 3.8+**
- 🍃 **MongoDB 5.0+** (Local installation or MongoDB Atlas Cloud)
- 🔑 **Groq API Key** (Free tier available)
- 🤗 **Hugging Face Token** (Free tier available)

---

## 🛠️ Step-by-Step Setup

### Step 1: Database Setup (MongoDB)

**Option A: Local MongoDB**
```bash
# Windows
mongod
# macOS
brew services start mongodb-community
# Linux
sudo systemctl start mongod
```

**Option B: MongoDB Atlas (Cloud)**
1. Create a free M0 cluster at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Get your connection string: `mongodb+srv://user:password@cluster.mongodb.net/interviewcoach`.

---

### Step 2: Backend Setup

Open a terminal in the project root:

**1. Create and Activate Python Virtual Environment**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Create a `.env` file from the template (or create a new one):
```bash
cp .env.example .env
```
Edit the `.env` file with your credentials:
```env
DATABASE_URL=mongodb://localhost:27017/interviewcoach
GROQ_API_KEY=your_api_key_here
HF_TOKEN=your_huggingface_token_here
JWT_SECRET=your_jwt_secret_key
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

**4. Start the Server**
```bash
uvicorn app:app --reload --port 8000
```
> 🎉 *Backend is now running on `http://localhost:8000`*

---

### Step 3: Frontend Setup

Open a **new** terminal and navigate to the `Frontend` folder:

```bash
cd Frontend
```

**1. Install Dependencies**
```bash
npm install
```

**2. Create Local Environment File**
```bash
# Windows (PowerShell)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Mac/Linux
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**3. Start Next.js Server**
```bash
npm run dev
```
> 🎉 *Frontend is now running on `http://localhost:3000`*

---

## 🎮 Access the Application

1. Open your browser and go to [http://localhost:3000](http://localhost:3000).
2. Click **Login** or **Get Started** to create a free account.
3. Upload your Resume (`PDF` or `DOCX`).
4. Head to the **Interview Service**, paste a job description, and start practicing!

---

## 🛑 Troubleshooting

> **Stuck? Check out these common solutions:**

- **Backend won't start (Port 8000 in use):**
  - Change the port: `uvicorn app:app --reload --port 8001`
  - *Note: Don't forget to update `NEXT_PUBLIC_API_URL` in the frontend if you change the port!*

- **Resume upload fails:** 
  - Ensure your `GROQ_API_KEY` is set correctly in `.env` and the file is under 5MB.

- **CORS Errors:** 
  - Verify the frontend URL exactly matches the allowed origins in `app.py`.

---

<div align="center">
  <b>Happy Building! 🚀</b>
</div>

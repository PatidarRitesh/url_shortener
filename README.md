# url_shortener

## 🚀 Objective

This project implements a **URL Shortener Service**, similar to Bitly, using **FastAPI (Python)**.  
The service allows users to:

- Convert long URLs into short, unique URLs.
- Redirect shortened URLs back to the original URLs.
- Track access statistics (click count).
- Handle expiration for shortened URLs.

---

## 📚 Problem Statement

### ✅ Functional Requirements
✔ **Shorten URLs** → A user submits a long URL and gets a short one.  
✔ **Redirection** → A short URL redirects to the original long URL.  
✔ **Unique URLs** → Each long URL generates a unique short URL.  
✔ **Validation** → The service ensures the input is a valid URL.  

### ✅ Non-Functional Requirements
✔ **Clean, modular, and well-documented code**.  
✔ **Scalable design** (supports future enhancements).  
✔ **Handles edge cases** like invalid URLs and duplicates.  
✔ **Extensible for additional features** (e.g., analytics, TTL).  

### ⭐ Optional Bonus Features (Implemented)
✔ **Click Tracking** → Track how many times a short URL was accessed.  
✔ **Expiration** → URLs expire after a set duration (default: **7 days**).  
✔ **Frontend UI** → Simple **HTML, CSS, JS** interface for easy usage.  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python) 🚀
- **Frontend:** HTML, CSS, JavaScript 🎨
- **Storage:** CSV File (In-memory alternative) 📄
- **Server:** Uvicorn (for running FastAPI) ⚡


---

## 📂 Project Structure
```
url_shortener/
│── backend/              # Backend (FastAPI)
│   ├── main.py           # Entry point for FastAPI
│   ├── routes.py         # API routes (shorten, redirect, stats)
│   ├── database.py       # CSV-based URL storage
│   ├── utils.py          # URL hashing & validation
│   ├── models.py         # Pydantic models for request validation
│── frontend/             # Frontend (HTML, CSS, JS)
│   ├── index.html        # UI for URL shortening & stats
│   ├── styles.css        # CSS for UI styling
│   ├── script.js         # JavaScript for API calls
│── README.md             # Project documentation
│── requirements.txt      # Python dependencies
```

---

## 🔮 Logic Explanation

### **1️⃣ `main.py`** (Backend Entry Point)
- Initializes the **FastAPI app**.
- Enables **CORS** to allow frontend requests.
- **Mounts API routes** from `routes.py`.
- Runs the FastAPI server using **Uvicorn**.

### **2️⃣ `routes.py`** (API Endpoints)
- Defines API endpoints:
  - **`POST /shorten`** → Shortens a long URL.
  - **`GET /{short_url}`** → Redirects to the original URL.
  - **`GET /stats/{short_url}`** → Fetches URL statistics.
- Calls helper functions from `database.py` and `utils.py`.

### **3️⃣ `database.py`** (CSV Storage)
- Uses a **CSV file** (`url_mapping.csv`) to store URL mappings.
- Functions:
  - **`read_url_mapping()`** → Reads URL mappings from CSV.
  - **`write_url_mapping()`** → Saves new URL mappings.
  - **`update_click_count()`** → Increments click count.


### **4️⃣ `utils.py`** (Helper Functions)
- **Generates a short URL** using `MD5` hashing.
- **Validates URL input** before storing.
- Can be expanded to include additional features like QR codes.

### **5️⃣ `models.py`** (Pydantic Models)
- Defines **request validation** using Pydantic.
- Ensures **only valid URLs** are accepted when shortening.

### **6️⃣ `index.html`** (Frontend UI)
- Provides a simple **UI to shorten URLs**.
- Includes an input box, buttons, and result display.

### **7️⃣ `script.js`** (Frontend Logic)
- Calls FastAPI backend via **`fetch()`**.
- Handles:
  - Sending a **POST request** to shorten URLs.
  - Sending a **GET request** to retrieve stats.
  - Extracting **short URL ID** from short URLs.
  - Updating the UI dynamically.

### **8️⃣ `styles.css`** (Frontend Styling)
- Styles the frontend for a **clean and user-friendly** experience.
- Includes UI elements like buttons, input fields, and result sections.

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/PatidarRitesh/url_shortener.git
cd url-shortener
```

### 2️⃣ Install Backend Dependencies
```sh
cd backend
pip install -r requirements.txt
```

### 3️⃣ Run Backend Server
```sh
uvicorn app:app --reload 
```
✅ FastAPI will run at: **`http://127.0.0.1:8000`**

### 4️⃣ Run Frontend Server
```sh
cd frontend
python -m http.server 8001
```
✅ Open: **`http://127.0.0.1:8001/`** in your browser.

---

## 🔗 How It Works
### **1️⃣ Shorten a URL**
- Enter a **long URL** in the frontend.
- Click **"Shorten URL"** → Generates a short URL.
- Example:
  ```
  Input: Input any long URL
  Output: Output short URL (e.g., http://127.0.0.1:8000/abcd12)
  ```

### **2️⃣ Redirect to Long URL**
- Click the **short URL**, and it redirects to the original.

### **3️⃣ Track Statistics**
- Enter a **short URL** and click **"Get Stats"**.
- See **click count** and **expiration time**.

---

## 🎯 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/shorten` | Shorten a long URL |
| **GET** | `/{short_url}` | Redirect to the original URL |
| **GET** | `/stats/{short_url}` | Get stats (click count, expiry) |

---

## 🚀 Design Decisions
### ✅ Why FastAPI?
- High performance & async capabilities.
- Built-in validation with **Pydantic**.

### ✅ Why CSV for Storage?
- Lightweight for this task.
- Easily replaceable with **SQL or Redis** in the future.

### ✅ How Short URLs are Generated?
- Uses **MD5 hashing** on the long URL.
- Returns a **6-character unique identifier**.

---

## ⚠️ Challenges & Edge Cases Handled
✔ **Invalid URL Handling** → Rejects incorrect formats.  
✔ **Duplicate URL Handling** → Returns the same short URL if already shortened.  
✔ **Non-Existent Short URLs** → Returns `404 Not Found`.  
✔ **Expired URLs** → Shows `410 Gone` if the URL expired.  
✔ **Concurrency Support** → Uses thread-safe CSV handling.

---





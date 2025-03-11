# 🚀 Event-Driven Order Processing System

This project demonstrates an **event-driven architecture** using **Event Sourcing** and **Change Data Capture (CDC)** in Django, Redis Streams, and SQLite.

## 📌 Features

✅ **Event Sourcing** → Stores order state changes in an **event store** (SQLite).  
✅ **Change Data Capture (CDC)** → Listens for database changes and **pushes them to external services** using Redis Streams.  
✅ **Real-Time Notifications & Analytics** → CDC forwards events to services that handle **notifications** and **business insights**.  
✅ **Django Management Commands** → Runs background listeners **independently** inside the Django app.

---

## 🛠️ **Tech Stack**

- **Backend:** Django, Django REST Framework
- **Event Store:** SQLite (Relational DB)
- **Streaming:** Redis Streams
- **Microservices:** Notification & Analytics Services

---

## ⚙️ **Installation & Setup**

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/yourusername/event-driven-orders.git
cd event-driven-orders
```

**2️⃣ Set Up a Virtual Environment**

```bash
python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows
```

**3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

**4️⃣ Start Redis (if not running)**

**5️⃣ Apply Migrations**

```bash
python manage.py migrate
```

**6️⃣ Start the Django Server**

```bash
python manage.py runserver
```

**🚀 Running the Event-Driven Components**
**Run the CDC Listener (to capture DB changes and forward events)**

```bash
python manage.py cdc_listener
```

**Run the Notification Service (to send alerts)**

```bash
python manage.py notification_service
```

**Run the Analytics Service (to process event data)**

```bash
python manage.py analytics_service
```

📌 Endpoints
Method Endpoint Description
POST /orders/ Create a new order
GET /orders/<order_id>/ Get the reconstructed state of an order

```

```

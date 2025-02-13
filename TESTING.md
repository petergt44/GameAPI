## **Testing the API**

This section explains how to test the API endpoints using tools like **cURL** or **Postman**.

### **1. Start the Flask Application**

Before testing, ensure the Flask application is running. Start it with:

```bash
python run.py
```

The API will be available at:
```
http://192.168.100.9:8080
```

---

### **2. Test Endpoints**

#### **Admin Login**
- **Endpoint**: `POST /admin/api/login`
- **Request**:
  ```bash
  curl -X POST http://192.168.100.9:8080/admin/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
  ```
- **Response**:
  ```json
  {
      "message": "Login successful"
  }
  ```

#### **Create a New Account**
- **Endpoint**: `POST /admin/api/accounts`
- **Request**:
  ```bash
  curl -X POST http://192.168.100.9:8080/admin/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "store1", "email": "store1@example.com", "password": "store123"}'
  ```
- **Response**:
  ```json
  {
      "id": 2,
      "username": "store1",
      "email": "store1@example.com",
      "type": "PLAYER",
      "created_at": "2023-10-10T12:05:00"
  }
  ```

#### **Fetch All Accounts**
- **Endpoint**: `GET /admin/api/accounts`
- **Request**:
  ```bash
  curl -X GET http://192.168.100.9:8080/admin/api/accounts
  ```
- **Response**:
  ```json
  [
      {
          "id": 1,
          "username": "admin",
          "email": "admin@example.com",
          "type": "ADMIN",
          "created_at": "2023-10-10T12:00:00"
      }
  ]
  ```

---

### **3. Test Game Provider Endpoints**

#### **VBLink Login**
- **Endpoint**: `POST /api/vblink/login`
- **Request**:
  ```bash
  curl -X POST http://192.168.100.9:8080/api/vblink/login \
  -H "Content-Type: application/json" \
  -d '{"username": "vblink_user", "password": "vblink_pass"}'
  ```
- **Response**:
  ```json
  {
      "message": "Login successful",
      "token": "abc123"
  }
  ```

#### **Add User to Category 1**
- **Endpoint**: `POST /api/category1/add_user`
- **Request**:
  ```bash
  curl -X POST http://192.168.100.9:8080/api/category1/add_user \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "player123"}'
  ```
- **Response**:
  ```json
  {
      "message": "User added successfully"
  }
  ```

---

## **Using Swagger for API Documentation**

Swagger provides an interactive UI to explore and test the API endpoints.

### **1. Access Swagger UI**

Start the Flask application and navigate to:
```
http://192.168.100.9:8080/swagger/
```

You’ll see the Swagger UI with a list of all available endpoints.

---

### **2. Explore Endpoints**

- **Admin API**:
  - `/admin/api/login` (POST)
  - `/admin/api/accounts` (GET, POST)
  - `/admin/api/tokens` (GET, POST)
  - `/admin/api/logs` (GET)

- **Game Provider API**:
  - `/api/vblink/login` (POST)
  - `/api/category1/add_user` (POST)

---

### **3. Test Endpoints in Swagger**

1. Click on an endpoint (e.g., `POST /admin/api/login`).
2. Click the **Try it out** button.
3. Enter the required parameters (e.g., `username` and `password`).
4. Click **Execute** to send the request.
5. View the response in the **Responses** section.

---

### **4. Example: Testing `/admin/api/login` in Swagger**

1. Open the `POST /admin/api/login` endpoint in Swagger.
2. Enter the following request body:
   ```json
   {
       "username": "admin",
       "password": "admin123"
   }
   ```
3. Click **Execute**.
4. View the response:
   ```json
   {
       "message": "Login successful"
   }
   ```

---

## **Additional Notes**

- **Authentication**: Some endpoints may require authentication. Use the token returned from the `/admin/api/login` or `/api/vblink/login` endpoints.
- **Error Handling**: If an error occurs, the API will return a descriptive error message and status code.

---

## **Example API Workflow**

1. **Login as Admin**:
   - Use `POST /admin/api/login` to authenticate.
   - Save the returned token for future requests.

2. **Create a New Account**:
   - Use `POST /admin/api/accounts` to create a new account.

3. **Fetch All Accounts**:
   - Use `GET /admin/api/accounts` to list all accounts.

4. **Login to VBLink**:
   - Use `POST /api/vblink/login` to authenticate with the VBLink provider.

5. **Add a User to Category 1**:
   - Use `POST /api/category1/add_user` to add a new user.

---

Let me know if you need further assistance! 🚀
# 📝 Django Multi-Author Blog with RBAC & AI-Powered Moderation

A **multi-author blogging platform** built with Django.  
Implements **Role-Based Access Control (RBAC)**, **email-verification-based authentication**, and an **AI-powered comment moderation pipeline**.

⚠️ **Note:** This project is under active development.  
Currently the **core functionality is implemented**, while the **REST API layer (Django REST Framework)** will be added in the next phase.

---

## 🚀 Features

### 🔐 Authentication & User Management
- User registration with **email verification** (inactive until verified).  
- Email-based authentication (secure login/logout).  
- User roles with **RBAC**:
  - **Admin** → approve/reject posts, manage users & categories.  
  - **Author** → create & manage their own posts (requires admin approval before publishing).  
  - **Reader** → browse, search, and comment on posts.  
- User profiles with:
  - Editable personal details (bio, profile pic, etc.).  
  - Change password & account settings.  

---

### 📰 Blogging System
- Multi-author posts with **approval workflow**:
  - Authors create drafts.  
  - Admin reviews & approves posts before publishing.  
- Posts organized by **categories** (filterable via category buttons).  
- **Search functionality** across posts (title/content).  
- **Pagination** for scalable post browsing.  

---

### 💬 Comments & AI Moderation
- Registered users can comment on posts.  
- Each comment is automatically checked by the **Gemini AI model**:  
  - Blocks hateful, abusive, or dangerous content.  
  - Only safe comments are published.  

---

### ⚙️ Admin Features
- Review & approve/reject posts.  
- Manage users and assign roles.  
- Moderate flagged comments.  
- Manage categories.  

---

## 🛠 Tech Stack
- **Backend**: Django  
- **Database**: PostgreSQL (preferred for production)  
- **Auth**: Email verification + role-based access control  
- **AI Integration**: Gemini API (for comment moderation)  
- **Frontend (basic)**: Django templates (can be extended to React/Flutter later)  

---


---

## 📖 API Development Roadmap

The next phase of the project will introduce a **REST API layer** with **Django REST Framework (DRF)**:

- `POST /auth/register/` → User registration with email verification  
- `POST /auth/login/` → JWT login  
- `POST /posts/` → Create new post (Author only, requires Admin approval)  
- `PUT /posts/{id}/approve/` → Approve/reject post (Admin only)  
- `GET /posts/` → List posts (with search, filter, pagination)  
- `POST /posts/{id}/comments/` → Add comment (AI moderated)  
- `GET /users/{id}/profile/` → View author profile  

📌 *API endpoints are not yet implemented. They will be added in the upcoming iteration.*  

---

## 🧪 Testing
- Planned: unit & integration tests for authentication, RBAC, posts, and comments.  
- CI/CD pipeline will be integrated with GitHub Actions.  

---

## 🏗 Roadmap
- [x] User registration with email verification  
- [x] Role-based access (Admin, Author, Reader)  
- [x] Post approval workflow  
- [x] AI moderation for comments (Gemini integration)  
- [x] Search, categories, pagination  
- [ ] API endpoints with Django REST Framework  
- [ ] Swagger/OpenAPI documentation  
- [ ] Dockerization & deployment  

---

## 👨‍💻 Author
**Naeem Ahmed**  
Full Stack Developer | Passionate About **Backend Systems, Deep Learning & RAG**  

---


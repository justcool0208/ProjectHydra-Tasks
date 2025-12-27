# Task 0 – Environment Setup & GitHub Push
Tools Installed

I installed and verified all required tools for Kubernetes workflow:

| Tool       | Purpose                      | Command used          |
|------------|------------------------------|------------------------|
| Docker     | Container runtime            | `docker --version`     |
| kubectl    | Kubernetes CLI               | `kubectl version`      |
| Minikube/Kind | Local K8s cluster        | `minikube version`     |
| Helm       | K8s package manager          | `helm version`         |
| Git        | Version control              | `git --version`        |

Screenshot showing all tools installed: 
`setup_screenshot.png`

---

## 2. Sample Node.js App

Created a simple **Node.js + Express** application with a single health endpoint.

### **Endpoint**
```
GET /health → "OK"
```

### **Run Locally with Docker**

Build the image:

```bash
docker build -t task0-node .
```

Run the container:

```bash
docker run -p 8080:8080 task0-node
```

test endpoint:

```
http://localhost:8080/health
```

---
project structure

```
Task0/
 ├── app/
 │   ├── server.js
 │   └── package.json
 ├── Dockerfile
 ├── README.md
 ├── .gitignore
 └── setup_screenshot.png
```

---

## step 4

- Forked the original **ProjectHydra-Tasks** repository.
- Added all required files to `Task0/`.
- Committed with message:

# output screenshot

<img width="1920" height="1080" alt="health_check" src="https://github.com/user-attachments/assets/65b6b9b7-e7af-484c-9ca3-19edc1bef227" />

# setup screenshot

<img width="1920" height="1080" alt="setup_screenshot" src="https://github.com/user-attachments/assets/1a2091b5-0c5b-4b74-8d1d-038ea40aa118" />






```
Initial commit - Task 0 setup complete
```




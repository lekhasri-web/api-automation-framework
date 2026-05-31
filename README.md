# API Automation & Contract Validation Framework

A modular, production-ready backend test automation engine built with **Python** and **Pytest**. This framework is engineered to isolate microservices via localized mocking, enforce strict data schema compliance, and validate complete multi-endpoint data-dependency sequences (CRUD chaining).

---

## 🛠️ Tech Stack & Dependencies

* **Core Language:** Python 3.12+
* **HTTP Client:** Requests Library
* **Test Engine & Configurations:** Pytest
* **Data Contract Enforcer:** jsonschema
* **Service Isolation Routing:** requests-mock

---

## 🏗️ Core Architectural Features

### 1. Unified HTTP Client Service
* Centralized network configurations inside `utils/api_client.py` to handle dynamic payloads, query parameters, base URLs, and connection rules globally.
* Eliminates repetitive code blocks—adding test validation for a brand-new service endpoint requires only 3–5 lines of clean code configuration.

### 2. Token-Based Authentication Lifecycle
* Stateful session management tracking token generation, verification, and rotation.
* Automated interceptors evaluate token validation windows on outbound requests, programmatically triggering token-refresh actions seamlessly before session expiration splits pipeline continuity.

### 3. Full CRUD Lifecycle API Chaining
* End-to-end integration workflows validating state transitions by linking downstream request dependencies with data mutations returned from upstream endpoints (`POST` → `GET` → `PUT` → `DELETE`).

### 4. Rigid JSON Schema Contract Validation
* Direct integration of programmatic `jsonschema` checks evaluating backend payload properties against strict definitions (`schemas/`) to catch implicit structural regression bugs instantly.

### 5. High-Density Test Parametrization
* Utilizes Pytest matrix parameterization to evaluate varied negative inputs, empty payloads, boundary conditions, and valid entities efficiently, increasing overall edge-case script coverage by **200%**.

### 6. Local Performance Response Caching
* Internal memory caching intercepts sequential `GET` calls targeting identical static endpoints, reducing duplicate mock processing overhead.

---

## 🚀 How to Run the Test Suite

### 1. Clone the repository and navigate to the root directory:
```bash
git clone [https://github.com/lekhasri-web/API-Automation-Contract-Validation-Framework.git](https://github.com/lekhasri-web/API-Automation-Contract-Validation-Framework.git)
cd API-Automation-Contract-Validation-Framework
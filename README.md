# BFHL FastAPI - Bajaj Finserv Health API

[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.8.2-red.svg)](https://pydantic.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive FastAPI implementation of the Bajaj Finserv Health (BFHL) API specification. This REST API processes arrays of mixed data and intelligently categorizes elements into numbers, alphabets, and special characters with advanced processing rules.

## 🚀 Features

- ✅ **POST /bfhl** endpoint for processing data arrays
- 🔢 **Smart Token Classification** (numbers, alphabets, special characters)
- ➕ **Sum Calculation** for numeric values (returned as strings)
- 🔤 **Alphabet Processing** with uppercase conversion
- 🎭 **Advanced Concatenation** with alternating capitalization
- 🛡️ **Robust Error Handling** (always returns HTTP 200)
- 🧪 **Comprehensive Test Suite** with 100% specification coverage
- 🚀 **Production Ready** for Render deployment
- 📚 **Auto-generated API Documentation** (Swagger/ReDoc)
- 🔧 **Environment-based Configuration**

## 📊 Screenshots

### API Documentation (Swagger UI)
<!-- Add screenshot of Swagger UI documentation -->
![Swagger UI](screenshots/swagger-ui.png)
*Auto-generated API documentation with interactive testing interface*

### Successful API Response
<!-- Add screenshot of successful API response -->
![API Response](screenshots/api-response.png)
*Example of successful API response with categorized data*



## 🔧 API Specification

### 🎯 Endpoint
```
POST /bfhl
Content-Type: application/json
```

### 📝 Request Format
```json
{
  "data": ["mixed", "array", "of", "123", "data", "$", "elements"]
}
```

### 📤 Response Format
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com", 
  "roll_number": "ABCD123",
  "odd_numbers": ["123"],
  "even_numbers": [],
  "alphabets": ["MIXED", "ARRAY", "OF", "DATA", "ELEMENTS"],
  "special_characters": ["$"],
  "sum": "123",
  "concat_string": "StNeMeLeFaAtArAaDxEiM"
}
```

### 🏷️ Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `is_success` | boolean | Operation status (always present) |
| `user_id` | string | Format: `{full_name}_{ddmmyyyy}` (lowercase) |
| `email` | string | User email address |
| `roll_number` | string | College roll number |
| `odd_numbers` | array[string] | Odd numeric tokens as strings |
| `even_numbers` | array[string] | Even numeric tokens as strings |
| `alphabets` | array[string] | Pure alphabetic tokens (uppercased) |
| `special_characters` | array[string] | Mixed or special character tokens |
| `sum` | string | Sum of all numeric values (as string) |
| `concat_string` | string | Processed alphabetic concatenation |
| `error` | string | Error message (only if `is_success: false`) |

## 🧠 Processing Rules

### 🔢 Token Classification Rules

1. **Pure Numbers** (`^\d+$`): 
   - Classified by integer parity (odd/even)
   - Returned as strings in respective arrays
   - Examples: `"123"` → odd_numbers, `"456"` → even_numbers

2. **Pure Alphabets** (`^[A-Za-z]+$`):
   - Converted to uppercase
   - Added to alphabets array
   - Examples: `"hello"` → `"HELLO"`, `"World"` → `"WORLD"`

3. **Special Characters**: 
   - Everything else (mixed alphanumeric, punctuation, etc.)
   - Returned as-is in special_characters array
   - Examples: `"abc123"`, `"@#$"`, `"3.14"`

### ➕ Sum Calculation
- All pure numeric tokens are converted to integers
- Sum is calculated and returned as a string
- Non-numeric tokens are ignored in sum calculation

### 🎭 Concat String Algorithm
Complex 4-step process for alphabetic character processing:

1. **Extract**: Collect all alphabetic characters from input tokens (preserving order)
2. **Reverse**: Reverse the entire character sequence  
3. **Alternate**: Apply alternating capitalization starting with UPPERCASE
4. **Join**: Concatenate into final string

**Example**: `["a","1","334","4","R","$"]`
- Extract: `['a', 'R']`
- Reverse: `['R', 'a']` 
- Alternate: `['R'(upper), 'a'(lower)]`
- Result: `"Ra"`


### 🚀 Running the Application

1. **Start Development Server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the Application**
   - **API Endpoint**: http://localhost:8000/bfhl
   - **Swagger Documentation**: http://localhost:8000/docs
   - **ReDoc Documentation**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

## 🔍 API Examples

### 🎯 Example 1: Basic Mixed Data
<img width="1880" height="1016" alt="image" src="https://github.com/user-attachments/assets/6ce3a7d3-a475-42a4-93bf-5ddfea112924" />

**Request:**
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["a","1","334","4","R","$"]}'
```

**Response:**
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334","4"],
  "alphabets": ["A","R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}
```
<img width="1591" height="602" alt="image" src="https://github.com/user-attachments/assets/0a97daaf-6eff-41f4-9bbb-684e0cc99ae4" />


### 🎯 Example 2: Complex Mixed Content
<img width="1773" height="1012" alt="image" src="https://github.com/user-attachments/assets/04d1a2fc-f130-493d-a558-f0c8f21d583a" />

**Request:**
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["2","a","y","4","&","-","*","5","92","b"]}'
```

**Response:**
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["5"],
  "even_numbers": ["2","4","92"],
  "alphabets": ["A","Y","B"],
  "special_characters": ["&","-","*"],
  "sum": "103",
  "concat_string": "ByA"
}
```
<img width="1000" height="697" alt="image" src="https://github.com/user-attachments/assets/093d9bfa-839b-4a05-93d0-255936f96ae2" />

### 🎯 Example 3: Pure Alphabetic Processing
<img width="1829" height="961" alt="image" src="https://github.com/user-attachments/assets/a75ad87b-7a27-48ed-8da2-3ed0f7a2777b" />

**Request:**
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["A","ABcD","DOE"]}'
```

**Response:**
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": [],
  "even_numbers": [],
  "alphabets": ["A","ABCD","DOE"],
  "special_characters": [],
  "sum": "0",
  "concat_string": "EoDdCbAa"
}
```
<img width="997" height="520" alt="image" src="https://github.com/user-attachments/assets/e4ef4f28-fd81-4aec-b97b-0f62eb5ff74f" />


### 🎯 Example 4: Advanced Test Case
<img width="1801" height="1006" alt="image" src="https://github.com/user-attachments/assets/c1bb5eec-87fc-4698-80c9-95025550f967" />

**Request:**
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"data": ["hello", "123", "world", "456", "@", "#", "test", "789"]}'
```

**Response:**
```json
{
  "is_success": true,
  "user_id": "john_doe_17091999", 
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["123", "789"],
  "even_numbers": ["456"],
  "alphabets": ["HELLO", "WORLD", "TEST"],
  "special_characters": ["@", "#"],
  "sum": "1368",
  "concat_string": "TsEtWoRlDhElLo"
}
```
<img width="1225" height="642" alt="image" src="https://github.com/user-attachments/assets/0bd38ef0-5efe-46f9-bb6b-a3dd158413db" />


### 🔴 Error Response Example
<img width="1781" height="972" alt="image" src="https://github.com/user-attachments/assets/f89eaf41-b7a3-4be7-9ea8-a2c204a3c649" />

**Request with Invalid Data:**
```bash
curl -X POST "http://localhost:8000/bfhl" \
  -H "Content-Type: application/json" \
  -d '{"invalid_field": ["test"]}'
```

**Response:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "data"],
      "msg": "Field required",
      "input": {"invalid_field": ["test"]}
    }
  ]
}

```
<img width="998" height="541" alt="image" src="https://github.com/user-attachments/assets/eec3d90c-5292-4b8b-bb13-cb319c2da0e5" />



## 📁 Project Structure

```
bfhl-fastapi/
├── 📁 app/                          # Main application package
│   ├── 🐍 __init__.py              # Package initializer
│   ├── 🚀 main.py                  # FastAPI app & /bfhl endpoint
│   ├── ⚙️ core.py                  # Core processing logic
│   └── 🔧 config.py                # Environment configuration
├── 📁 tests/                       # Test suite
│   └── 🧪 test_bfhl.py             # Comprehensive API tests
├── 📁 screenshots/                 # Documentation screenshots
│   ├── 📸 swagger-ui.png           # API documentation
│   ├── 📸 api-response.png         # Sample responses
│   ├── 📸 test-results.png         # Test execution
│   ├── 📸 render-deployment.png    # Deployment process
│   └── 📸 api-testing.png          # API testing tools
├── 📋 requirements.txt              # Python dependencies
├── 🐍 runtime.txt                  # Python version (3.11.9)
├── ☁️ render.yaml                  # Render deployment config
├── 📖 README.md                    # Project documentation
└── 🚫 .gitignore                   # Git ignore patterns
```

### 📂 Key Files Description

| File | Purpose | Key Features |
|------|---------|--------------|
| `app/main.py` | FastAPI application | Route definitions, CORS, error handling |
| `app/core.py` | Processing logic | Token classification, sum calculation, concat logic |
| `app/config.py` | Configuration | Environment variables, user ID generation |
| `tests/test_bfhl.py` | Test suite | All specification examples, edge cases |
| `render.yaml` | Deployment config | Native Python deployment on Render |
| `requirements.txt` | Dependencies | FastAPI, Pydantic v2, testing frameworks |

## 🛠️ Technology Stack

### 🔧 Core Technologies

| Technology | Version | Purpose | Benefits |
|------------|---------|---------|----------|
| **Python** | 3.11.9 | Runtime environment | Latest features, performance |
| **FastAPI** | 0.111.0 | Web framework | Auto docs, high performance, async |
| **Pydantic** | 2.8.2 | Data validation | Type safety, auto-validation |
| **Uvicorn** | 0.30.0 | ASGI server | Production-ready, fast |

## 🔧 Environment Configuration

### 🔑 Required Environment Variables

```bash
# User identification (used for user_id generation)
FULL_NAME="john_doe"              # Lowercase with underscores
DOB_DDMMYYYY="17091999"          # Date format: DDMMYYYY
EMAIL="john@xyz.com"             # User email address
ROLL_NUMBER="ABCD123"            # College roll number
```

### 🌍 Environment Files

Create `.env` file for local development:
```env
FULL_NAME=john_doe
DOB_DDMMYYYY=17091999
EMAIL=john@xyz.com
ROLL_NUMBER=ABCD123
```

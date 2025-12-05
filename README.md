# 💬 ChatWave - Modern Messaging Reimagined

A revolutionary open-source messaging platform combining the best of WhatsApp, Telegram, and AI-powered features

## 🚀 Overview

ChatWave is a cutting-edge messaging platform that bridges the gap between simplicity and powerful functionality. We've taken the best aspects of popular messaging apps and enhanced them with modern AI capabilities, unlimited storage, and a privacy-first approach.

## ✨ Features

### 💬 Core Messaging
- Real-time one-on-one & group chats (500+ members)
- Media sharing (images available for 24 hours)
- Voice messages with transcription
- Message reactions, replies, editing & pinning
- Read receipts & typing indicators

### 🎨 Modern Experience
- 24-hour Stories with reactions & archives
- Voice & video calls with screen sharing
- Custom themes & chat backgrounds
- Dark/Light/System theme modes
- Cross-platform sync (Web, Mobile, Desktop)

### 🔒 Security & Privacy
- Optional end-to-end encryption
- Self-destructing messages
- Incognito mode (hide online status)
- App lock (PIN/Fingerprint)
- Two-factor authentication

### 🤖 AI Powered
- AI-powered quick replies
- Auto-translation in 100+ languages
- Smart search across conversations
- Message summarization
- Calendar integration

### 💰 Freemium Model
- **Free Tier**: 500 messages/day, 25 member groups
- **Premium** (₹200/month): Unlimited messages, 500 member groups, voice/video calls

## 🛠️ Tech Stack

### Frontend
- **Framework**: React.js + TypeScript + Tailwind CSS + PWA
- **Mobile**: React Native (iOS & Android)
- **State Management**: Zustand
- **Real-time**: Socket.io-client
- **Deployment**: Vercel

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Real-time**: WebSockets + Socket.io
- **AI Services**: OpenAI API, Hugging Face Transformers
- **File Storage**: Cloudinary
- **Caching**: Redis
- **Deployment**: Render

## 📋 Prerequisites

- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL
- Redis
- Cloudinary account (for file storage)
- OpenAI API key (for AI features)

## 🚀 Quick Start

### Frontend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/chatwave.git
cd chatwave

# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Add your environment variables
# REACT_APP_API_URL=http://localhost:8000
# REACT_APP_SOCKET_URL=http://localhost:8000

# Start development server
npm start
```

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Add your environment variables
# DATABASE_URL=postgresql://username:password@localhost/chatwave
# REDIS_URL=redis://localhost:6379
# OPENAI_API_KEY=your_openai_key
# CLOUDINARY_URL=cloudinary://your_cloudinary_url

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

```
chatwave/
├── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── utils/
│   │   ├── services/
│   │   └── types/
│   ├── package.json
│   ├── tailwind.config.js
│   └── vercel.json
└── backend/
    ├── app/
    │   ├── main.py
    │   ├── models/
    │   ├── schemas/
    │   ├── database/
    │   ├── routes/
    │   ├── middleware/
    │   ├── utils/
    │   └── ai_services/
    ├── requirements.txt
    ├── Dockerfile
    └── render.yaml
```

## 📝 Environment Variables

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_SOCKET_URL=http://localhost:8000
REACT_APP_CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
REACT_APP_CLOUDINARY_UPLOAD_PRESET=your_upload_preset
```

### Backend (.env)
```
DATABASE_URL=postgresql://username:password@localhost/chatwave
REDIS_URL=redis://localhost:6379
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
OPENAI_API_KEY=your_openai_api_key
CLOUDINARY_URL=cloudinary://your_cloudinary_url
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_email_password
```

## 🔧 Available Scripts

### Frontend
- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Lint code

### Backend
- `uvicorn app.main:app --reload` - Start development server
- `pytest` - Run tests
- `black .` - Format code
- `mypy .` - Type checking

## 🌐 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info

### Messages
- `GET /messages/{room_id}` - Get messages for a room
- `POST /messages` - Send a message
- `PUT /messages/{message_id}` - Edit a message
- `DELETE /messages/{message_id}` - Delete a message

### Rooms
- `GET /rooms` - Get user's rooms
- `POST /rooms` - Create a new room
- `GET /rooms/{room_id}` - Get room details
- `PUT /rooms/{room_id}` - Update room
- `DELETE /rooms/{room_id}` - Delete room

## 🤖 AI Features

### Translation
- Real-time translation in 100+ languages
- Auto-detect source language
- Preserve message context

### Quick Replies
- AI-powered smart suggestions
- Context-aware responses
- Customizable reply templates

### Message Summarization
- Automatic conversation summaries
- Key points extraction
- Time-based summaries

## 📱 Deployment

### Frontend (Vercel)
1. Push code to GitHub
2. Connect Vercel to your repository
3. Set environment variables in Vercel dashboard
4. Deploy automatically

### Backend (Render)
1. Create new Web Service on Render
2. Connect to your GitHub repository
3. Set environment variables in Render dashboard
4. Configure build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🛡️ Security

- JWT-based authentication with refresh tokens
- Rate limiting to prevent abuse
- Input validation and sanitization
- Secure password hashing (bcrypt)
- HTTPS enforced in production
- CORS configured for security

## 🧪 Testing

### Frontend Testing
```bash
npm test
npm run test:coverage
```

### Backend Testing
```bash
pytest
pytest --cov=app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- GitHub Issues: [Create Issue](https://github.com/yourusername/chatwave/issues)
- Discord: [Join Community](https://discord.gg/chatwave)
- Email: support@chatwave.com

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Socket.io for real-time communication
- OpenAI for AI capabilities
- Cloudinary for media storage
- All the open-source contributors who made this possible

---

<p align="center">
  Made with ❤️ by the ChatWave Team
</p>

<p align="center">
  <sub>Star this repo if you found it helpful! ⭐</sub>
</p>


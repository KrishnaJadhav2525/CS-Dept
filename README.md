# Computer Science Department Portal

This is the official web application for the Computer Science Department. **This portal is currently operational and actively used in production at Rajarshi Shahu Mahavidyalaya, Latur (Autonomous).**

The platform serve as a central hub for students, faculty, and administrative activities, bridging the gap between department management and user engagement.

## Key Features

### 🔐 Authentication & Profiles
- **Role-Based Access**: Specialized views and permissions for Students and Faculty members.
- **Secure Authentication**: Includes standard login/signup and secure Email OTP support for students.
- **Personalized Profiles**: Users can manage their details, track activity, and view their contributions.

### 📝 Content Management
- **Blog System**: Advanced submission workflow where users can write posts. Features include:
  - Administrative approval process.
  - Social interactions: Likes and comments on approved posts.
  - Support for image and PDF attachments.
- **Department Notices**: Real-time sorted notifications for important updates and announcements.

### 🏛️ Departmental Sections
- **CSA (Computer Science Association)**: Dedicated section for current and past association members, events, and reports.
- **Research & Publications**: Showcase for departmental research papers with download capabilities.
- **Events & Gallery**: Dynamic event listings (upcoming/past) and specialized galleries for Infrastructure, Industrial Tours, and Department Activities.
- **Curriculum**: Access to degree-specific syllabus and academic structures.

### 🛠️ Administrative Control
- **Full CRUD Dashboard**: Admins can manage all aspects of the site, from faculty listings and gallery images to research papers and student activities.
- **Inquiry Management**: Direct handling of contact form submissions.

## Technical Stack

- **Backend**: Flask (Python) with highly modular service layers.
- **Database**: 
  - **Remote**: MongoDB support with GridFS for efficient file storage.
  - **Fallback**: Robust local JSON-based storage for lightweight deployment.
- **Security**: Environment variable configuration via `.env` for secrets and API keys.
- **Deployment**: Configured for local servers or Vercel production environments.

## Local Installation

1. **Clone and Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env to set SECRET_KEY, MONGO_URI, and Mail settings
   ```

3. **Run Application**:
   ```bash
   python run.py
   ```

## Production Details
- **Location**: Rajarshi Shahu Mahavidyalaya, Latur (Autonomous).
- **Current Status**: Live Operations.
- **Department**: Computer Science.

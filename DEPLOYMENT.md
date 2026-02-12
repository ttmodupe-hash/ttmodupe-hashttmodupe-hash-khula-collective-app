# Deployment Guide 🚀

## Overview
This guide covers deploying the FNB Savings Tracker to various platforms.

## Current Deployment
Your application is currently running at: **https://00303.app.super.myninja.ai**

## Deployment Options

### 1. Streamlit Cloud (Recommended)

#### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)

#### Steps
1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets**:
   - In Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
     ```toml
     STITCH_CLIENT_ID = "your_client_id"
     STITCH_CLIENT_SECRET = "your_client_secret"
     STITCH_API_URL = "https://api.stitch.money/graphql"
     ```

### 2. Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run
```bash
# Build image
docker build -t fnb-savings-tracker .

# Run container
docker run -p 8501:8501 \
  -e STITCH_CLIENT_ID=your_id \
  -e STITCH_CLIENT_SECRET=your_secret \
  fnb-savings-tracker
```

### 3. Heroku Deployment

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Setup Files

**Procfile**:
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh**:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = &quot;your-email@domain.com&quot;\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

#### Deploy
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set STITCH_CLIENT_ID=your_id
heroku config:set STITCH_CLIENT_SECRET=your_secret

# Deploy
git push heroku main
```

### 4. AWS EC2 Deployment

#### Launch EC2 Instance
1. Choose Ubuntu 22.04 LTS
2. Select t2.micro (free tier eligible)
3. Configure security group to allow port 8501

#### Setup on EC2
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip -y

# Clone repository
git clone your-repo-url
cd fnb-savings-tracker

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
nano .env
# Add your credentials

# Run with nohup
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

### 5. Local Development Server

#### Using Python
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

#### Using Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

## Environment Variables

### Required Variables
- `STITCH_CLIENT_ID`: Your Stitch API client ID
- `STITCH_CLIENT_SECRET`: Your Stitch API client secret
- `STITCH_API_URL`: Stitch API endpoint (default: https://api.stitch.money/graphql)

### Configuration Methods

#### 1. .env File (Local Development)
```bash
STITCH_CLIENT_ID=your_client_id
STITCH_CLIENT_SECRET=your_client_secret
STITCH_API_URL=https://api.stitch.money/graphql
```

#### 2. Streamlit Secrets (Cloud Deployment)
Create `.streamlit/secrets.toml`:
```toml
STITCH_CLIENT_ID = "your_client_id"
STITCH_CLIENT_SECRET = "your_client_secret"
STITCH_API_URL = "https://api.stitch.money/graphql"
```

#### 3. System Environment Variables
```bash
export STITCH_CLIENT_ID=your_client_id
export STITCH_CLIENT_SECRET=your_client_secret
export STITCH_API_URL=https://api.stitch.money/graphql
```

## Security Best Practices

### 1. Credential Management
- ✅ Never commit `.env` files to version control
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Use environment variables or secrets management
- ✅ Rotate API credentials regularly

### 2. API Security
- ✅ Use HTTPS for all API communications
- ✅ Implement rate limiting
- ✅ Monitor API usage
- ✅ Set appropriate token expiration

### 3. Application Security
- ✅ Keep dependencies updated
- ✅ Use secure connections only
- ✅ Implement proper error handling
- ✅ Log security events

## Monitoring and Maintenance

### Health Checks
```python
# Add to app.py for health endpoint
import streamlit as st

def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Performance Monitoring
- Monitor response times
- Track API call frequency
- Monitor memory usage
- Set up alerts for errors

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>
```

#### Dependencies Not Installing
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt
```

#### Streamlit Not Starting
```bash
# Clear cache
streamlit cache clear

# Run with debug mode
streamlit run app.py --logger.level=debug
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (e.g., AWS ELB, Nginx)
- Deploy multiple instances
- Implement session affinity

### Vertical Scaling
- Increase instance size
- Optimize memory usage
- Use caching strategies

### Database Considerations
- Consider adding PostgreSQL for data persistence
- Implement caching layer (Redis)
- Use connection pooling

## Backup and Recovery

### Data Backup
```bash
# Backup configuration
cp .env .env.backup

# Backup application
tar -czf backup.tar.gz app.py stitch_api.py data_processor.py
```

### Disaster Recovery
1. Keep configuration in version control
2. Document deployment process
3. Test recovery procedures
4. Maintain backup credentials

## Updates and Maintenance

### Updating Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade streamlit
```

### Application Updates
```bash
# Pull latest changes
git pull origin main

# Restart application
# (method depends on deployment platform)
```

## Support and Resources

- **Streamlit Documentation**: https://docs.streamlit.io
- **Stitch API Documentation**: https://stitch.money/docs
- **Docker Documentation**: https://docs.docker.com
- **Heroku Documentation**: https://devcenter.heroku.com

## Checklist Before Deployment

- [ ] All dependencies listed in requirements.txt
- [ ] Environment variables configured
- [ ] Security credentials secured
- [ ] .gitignore properly configured
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Health checks added
- [ ] Documentation updated
- [ ] Testing completed
- [ ] Backup strategy in place

---

**Ready to deploy? Choose your platform and follow the guide above!** 🚀
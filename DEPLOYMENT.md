# AWS Deployment Guide

## Overview

This guide covers deploying the Clio Awards Chatbot to AWS using various deployment options.

## Deployment Options

### Option 1: AWS EC2 (Recommended for Beginners)
- **Pros**: Simple, full control, easy debugging
- **Cons**: Manual scaling, requires server management
- **Cost**: ~$5-10/month (t2.micro)

### Option 2: AWS Elastic Beanstalk
- **Pros**: Automatic scaling, managed infrastructure
- **Cons**: Higher cost, less control
- **Cost**: ~$20-30/month

### Option 3: AWS ECS (Fargate)
- **Pros**: Containerized, serverless, scalable
- **Cons**: More complex setup
- **Cost**: ~$15-25/month

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Docker installed (for containerized deployments)
- Domain name (optional)

## Option 1: EC2 Deployment (Step-by-Step)

### 1. Launch EC2 Instance

```bash
# Create security group
aws ec2 create-security-group \
  --group-name clios-chatbot-sg \
  --description "Security group for Clio chatbot"

# Allow HTTP (80) and SSH (22)
aws ec2 authorize-security-group-ingress \
  --group-name clios-chatbot-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-name clios-chatbot-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0

# Launch instance
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t2.micro \
  --key-name your-key-pair \
  --security-groups clios-chatbot-sg
```

### 2. Connect to Instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### 3. Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3.9
sudo yum install python39 -y

# Install git
sudo yum install git -y

# Clone repository
git clone <your-repo-url>
cd clios-chatbot

# Create virtual environment
python3.9 -m venv virtualenv
source virtualenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add:
```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=clios-index
GOOGLE_API_KEY=your_google_key
```

### 5. Run with Systemd (Production)

Create service file:
```bash
sudo nano /etc/systemd/system/clios-chatbot.service
```

Add:
```ini
[Unit]
Description=Clio Awards Chatbot
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/clios-chatbot
Environment="PATH=/home/ec2-user/clios-chatbot/virtualenv/bin"
ExecStart=/home/ec2-user/clios-chatbot/virtualenv/bin/streamlit run ui/app.py --server.port=80 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl start clios-chatbot
sudo systemctl enable clios-chatbot
```

### 6. Access Application

Visit `http://your-instance-ip` in your browser.

## Option 2: Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build and Run

```bash
# Build image
docker build -t clios-chatbot .

# Run container
docker run -d \
  -p 80:8501 \
  -e PINECONE_API_KEY=your_key \
  -e PINECONE_INDEX_NAME=clios-index \
  -e GOOGLE_API_KEY=your_key \
  --name clios-chatbot \
  clios-chatbot
```

### 3. Deploy to AWS ECS

```bash
# Push to ECR
aws ecr create-repository --repository-name clios-chatbot
docker tag clios-chatbot:latest <your-ecr-url>/clios-chatbot:latest
docker push <your-ecr-url>/clios-chatbot:latest

# Create ECS task definition and service (use AWS Console)
```

## Environment Configuration

### Production Environment Variables

```env
# Required
PINECONE_API_KEY=<your-key>
PINECONE_INDEX_NAME=clios-index
GOOGLE_API_KEY=<your-key>

# Optional
STREAMLIT_SERVER_PORT=80
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

## Security Best Practices

1. **Never commit `.env` file** - Use AWS Secrets Manager or Parameter Store
2. **Use HTTPS** - Set up SSL certificate with AWS Certificate Manager
3. **Restrict security groups** - Only allow necessary ports
4. **Use IAM roles** - Don't hardcode AWS credentials
5. **Enable CloudWatch logging** - Monitor application logs

## Monitoring

### CloudWatch Logs

```bash
# Install CloudWatch agent
sudo yum install amazon-cloudwatch-agent -y

# Configure logging
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json
```

### Health Checks

Add to Streamlit app:
```python
# ui/app.py
@st.cache_resource
def health_check():
    return {"status": "healthy"}
```

## Scaling

### Horizontal Scaling (Multiple Instances)

1. Create Application Load Balancer
2. Create Auto Scaling Group
3. Configure target tracking

### Vertical Scaling

- Upgrade instance type (t2.small → t2.medium)
- Increase memory/CPU

## Cost Optimization

1. **Use Reserved Instances** - Save up to 70%
2. **Auto-scaling** - Scale down during low traffic
3. **Spot Instances** - For non-critical workloads
4. **CloudFront CDN** - Cache static assets

## Troubleshooting

### Application Won't Start

```bash
# Check logs
sudo journalctl -u clios-chatbot -f

# Check Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log
```

### Port 80 Permission Denied

```bash
# Use port 8501 or configure iptables
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8501
```

### Out of Memory

```bash
# Increase swap space
sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Backup & Recovery

### Backup Strategy

1. **Code**: Git repository
2. **Data**: S3 bucket for `data/` folder
3. **Environment**: Document all environment variables

### Disaster Recovery

```bash
# Backup data to S3
aws s3 sync data/ s3://your-bucket/clios-chatbot-backup/data/

# Restore from S3
aws s3 sync s3://your-bucket/clios-chatbot-backup/data/ data/
```

## Domain Setup (Optional)

### 1. Register Domain

Use Route 53 or external registrar

### 2. Configure DNS

```bash
# Create A record pointing to EC2 instance
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch file://dns-change.json
```

### 3. SSL Certificate

```bash
# Request certificate
aws acm request-certificate \
  --domain-name chatbot.yourdomain.com \
  --validation-method DNS
```

## Next Steps

1. Set up CI/CD pipeline (GitHub Actions)
2. Implement caching layer (Redis)
3. Add rate limiting
4. Set up monitoring alerts
5. Create staging environment

## Support

For deployment issues, check:
- AWS Documentation
- Streamlit Deployment Guide
- Project GitHub Issues

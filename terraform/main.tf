provider "aws" {
  region = "us-east-1"
}

# -------------------------
# SECURITY GROUP
# -------------------------
resource "aws_security_group" "app_sg" {

  name        = "compiler-sg"
  description = "Security Group for Compiler App"

  vpc_id = "vpc-02c32b04e7fbba84b"

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "compiler-sg"
  }
}

# -------------------------
# IAM ROLE FOR SSM (IMPORTANT)
# -------------------------
resource "aws_iam_role" "ec2_role" {
  name = "ec2_ssm_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = aws_iam_role.ec2_role.name
}

# -------------------------
# EC2 INSTANCE
# -------------------------
resource "aws_instance" "app" {

  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"

  subnet_id = "subnet-01bdc876e58b5e1eb"

  vpc_security_group_ids = [
    aws_security_group.app_sg.id
  ]

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
#!/bin/bash
yum update -y

# Install Docker
yum install -y docker
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# Install & start SSM agent (CRITICAL FIX)
yum install -y amazon-ssm-agent
systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent
EOF

  tags = {
    Name = "Compiler-App"
  }
}
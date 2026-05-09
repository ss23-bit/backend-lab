provider "aws" {
  region = "ap-southeast-1"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "devops_server" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  key_name      = var.key_name

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  security_groups = [aws_security_group.devops_sg.name]

  user_data = <<-EOF
                #!/bin/bash
                # Exit immediately if any command fails
                set -e
                
                apt update -y
                
                apt install -y docker.io
                
                systemctl start docker
                systemctl enable docker
                
                # Install AWS CLI v2
                apt install -y unzip curl
                
                # Keeps home directory clean, safe for temporary installs
                cd /tmp
                
                curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
                unzip awscliv2.zip
                ./aws/install
                
                # cut from the / part onwards
                REGISTRY=$(echo "$(var.ecr.uri)" | cut -d'/' -f1)


                # "--password-stdin" avoids exposing password
                aws ecr get-login-password --region ap-southeast-1 \
                | docker login --username AWS --password-stdin $REGISTRY

                docker pull $REGISTRY:latest

                # Normally with "latest" Docker does NOT always auto-refresh tags. Might needs "pull, stop, rm, run" to guarantee newest image
                docker run -d -p 8000:8000 \
                --restart always \
                $REGISTRY:latest
                
                rm -rf /tmp/aws /tmp/awscliv2.zip

                EOF

  tags = {
    Name = "ephemeral-devops-server"
  }
}

resource "aws_security_group" "devops_sg" {
  name = "devops-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # App
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Prometheus
  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
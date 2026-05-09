provider "aws" {
  region = "ap-southeast-1"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023*-kernel-*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_instance" "devops_server" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  key_name      = var.key_name

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  vpc_security_group_ids = [aws_security_group.devops_sg.id]

  user_data = <<-EOF
                #!/bin/bash
                exec > /var/log/user-data.log 2>&1
                # Exit immediately if any command fails
                set -e
                
                dnf update -y
                
                dnf install -y docker
                
                systemctl start docker
                systemctl enable docker
                
                REGISTRY=${var.ecr_registry}
                IMAGE=${var.ecr_uri}:latest

                # "--password-stdin" avoids exposing password
                aws ecr get-login-password --region ap-southeast-1 \
                | docker login --username AWS --password-stdin $REGISTRY
                
                docker pull $IMAGE

                # Normally with "latest" Docker does NOT always auto-refresh tags. Might needs "pull, stop, rm, run" to guarantee newest image
                docker run -d -p 8000:8000 --restart always $IMAGE               

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
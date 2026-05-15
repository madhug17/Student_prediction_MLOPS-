provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "mlops_server" {
  ami           = "ami-0c55b159cbfafe1f0" # Ubuntu Image
  instance_type = "t2.micro"

  tags = {
    Name = "Student-AI-Monitor-Server"
  }
}
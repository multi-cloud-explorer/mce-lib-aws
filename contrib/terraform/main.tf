
# TODO: voir https://github.com/terraform-providers/terraform-provider-aws/blob/master/examples/two-tier/main.tf

//resource "aws_s3_bucket" "b" {
//  bucket = "my-tf-test-bucket"
//  acl    = "public-read"
//}

resource "aws_key_pair" "admin" {
   key_name   = "admin"
   #public_key = "${file(var.public_key_path)}"
   public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCkyw+5+m6wTGef4ix/3b602w8hjt8YXB/CkkKGadmOOrFY8RoEWuW6LJFxZfDqLlX1ql94rIGUe6/Yh2Y5ESlCnfBJiBJkQ8tEmDDS4B51f4sRyo96wWxL85iarUa1KBfOn0hiW2d9ILB5TiARSImSFakoCh1t33V9N4X17toCp+GSpdtMWejKjWGQMOgFhjXX0oJTVdNxuWIPfAyxzefJoRh6hl4AYs33f0qpPIuzZxTo2iHbGxPK0PtCUbyQp1MbPKa8uR6rfAuDVqeoJeiH0v1jlyEyW0eu7wx4XRmcGPF4F/6ZKfxNywAQOF6GRDZIMeMJXrAEoChd2uKubuIL/45UhbQFJz/Tl8VZB+Z0oMHcq7uXtsJpvfunUr6GGzommrVklkPyRPBYxdjVKOsw9kbhIQYlkXpt6F2UBNHqkEvSsQEJtROmZa2XAn2hknh2jZGR7sVlVAwYAMh1fL/8iNlJqTeuVUgwr/Q0aUYcGplLEeelLSQFnxtaDAN0xas= srault@loan-sraul2"
}


# reseau virtuel privé par défaut
resource "aws_default_vpc" "default" {
   tags = {
     Name = "Default VPC"
   }
}

resource "aws_default_security_group" "default" {
   vpc_id      = aws_default_vpc.default.id
   ingress {
     from_port   = 22
     to_port     = 22
     protocol    = "tcp"
     cidr_blocks     = ["0.0.0.0/0"]
   }
   egress {
     from_port       = 0
     to_port         = 0
     protocol        = "-1"
     cidr_blocks     = ["0.0.0.0/0"]
   }
}   

resource "aws_instance" "server1" {
   ami           = "ami-045fa58af83eb0ff4"
   #ami           = "ami-123"
   instance_type = "t2.micro"
   key_name      = "admin"

  ebs_block_device {
    device_name = "sda2"
    volume_size = 16
  }

  #timeouts {
  #  create = "2m"
  #  delete = "5m"
  #}

  #provisioner "remote-exec" {
  #  inline = [
  #    "sudo apt-get -y update",
  #    "sudo apt-get -y install nginx",
  #    "sudo service nginx start",
  #  ]
  #}
}


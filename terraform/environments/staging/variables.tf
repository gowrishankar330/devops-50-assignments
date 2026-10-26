variable "environment" {
  default = "staging"
}

variable "aws_region" {
  default = "eu-west-2"
}

variable "vpc_cidr" {
  default = "10.1.0.0/16"
}

variable "public_subnet_cidrs" {
  default = ["10.1.1.0/24", "10.1.2.0/24"]
}

variable "private_subnet_cidrs" {
  default = ["10.1.10.0/24", "10.1.11.0/24"]
}

variable "availability_zones" {
  default = ["eu-west-2a", "eu-west-2b"]
}

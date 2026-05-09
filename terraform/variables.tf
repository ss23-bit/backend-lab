variable "key_name" {
  description = "EC2 key pair name"
  type        = string
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the server"
  type        = list(string)

  default = ["58.8.249.145/32"]
}

variable "ecr_uri" {
  description = "ECR image URI"
  type        = string

}

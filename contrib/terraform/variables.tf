variable "localstack_global_url" {
  description = "Edge URL for all localstack services"
  default     = "https://localhost:4566"
}

variable "credentials_profile" {
  description = "credential profile inside the profile file"
  default     = "default"
}

variable "credentials_file" {
  description = "credential file inside the user profile"
  default     = "~/.aws/credentials"
}

variable "credentials_access_key" {
  description = "AWS Access Key"
  default     = "anaccesskey"
}

variable "credentials_secret_key" {
  description = "AWS Secret Key"
  default     = "asecretkey"
}

variable "region" {
  description = "region use for the project"
  default     = "us-east-1"
}

variable "ssh_key_name" {
  description = "Name of the SSH keypair to use in AWS."
  default     = "deployer-key"
}

variable "ssh_key_path" {
  description = "Path to the private portion of the SSH key specified."
  default     = "~/pem.pem"
}

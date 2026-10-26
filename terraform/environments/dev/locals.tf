locals {
  common_tags = {
    Environment = var.environment
    Project     = "devops-50-assignments"
    ManagedBy   = "terraform"
    Owner       = "gowri"
  }
}

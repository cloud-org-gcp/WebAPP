packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = ">= 1.0.0"
    }
  }
}

variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "zone" {
  type        = string
  description = "The GCP zone where resources will be created"
}

variable "image_family" {
  type        = string
  description = "Image family to use as a base"
  default     = "centos-stream-9"
}

variable "machine_type" {
  type        = string
  default     = "n1-standard-1"
  description = "Machine type to use for the build instance"
}

variable "db_user" {
  type = string
}

variable "db_password" {
  type = string
}

variable "db_name" {
  type = string
}

source "googlecompute" "centos" {
  project_id          = var.project_id
  zone                = var.zone
  source_image_family = var.image_family
  ssh_username        = "packer"
  machine_type        = var.machine_type
  image_name          = "webapp-image-${formatdate("YYYYMMDDHHmmss", timestamp())}"
  image_family        = "webapp-image-family"
}

build {
  sources = [
    "source.googlecompute.centos"
  ]

  # Provisioner to copy the application zip file
  provisioner "file" {
    source      = "../app.zip"
    destination = "/tmp/app.zip"
  }

  # Provisioner to create user and set directory ownership
  provisioner "shell" {
    script = "./scripts/create_user.sh"
  }

  # Provisioner to install dependencies and deploy application
  provisioner "shell" {
    environment_vars = [
      "DB_USER=${var.db_user}",
      "DB_PASSWORD=${var.db_password}",
      "DB_NAME=${var.db_name}"
    ]
    script = "./scripts/install_dependencies.sh"
  }

  # Provisioner to set up systemd service for the application
  provisioner "shell" {
    script = "./scripts/systemd-service.sh"
  }
}

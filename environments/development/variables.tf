variable "subscription_id" { type = string }

variable "location" {
  type    = string
  default = "eastasia"
}

variable "project" {
  type    = string
  default = "cloud-ml"
}

variable "project_short" {
  type    = string
  default = "cloudml"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "image_tag" {
  type    = string
  default = "v2"
}
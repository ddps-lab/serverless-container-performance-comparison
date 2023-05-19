variable "project" {
  type    = string
  default = "cloudrun-inference"
}

variable "region" {
  type    = string
  default = "asia-northeast3"
}

variable "prefix" {
  type    = string
  default = "mhsong"
}

variable "docker_registry" {
  type    = string
  default = "asia-northeast3-docker.pkg.dev/cloudrun-inference/serverless-container-performance-comparison"
}

variable "enabled_models" {
  type    = list(string)
  # default = ["yolo_v5"]
  default = [ "mobilenet_v1", "mobilenet_v2", "inception_v3", "yolo_v5", "bert_imdb"]
}

variable "model_resources" {
  type = object({
    mobilenet_v1 = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
    mobilenet_v2 = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
    inception_v3 = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
    yolo_v5 = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
    bert_imdb = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
    distilbert_sst2 = object({
      cpu_number    = number
      ram_mib       = number
      min_instances = number
      max_instances = number
    })
  })
  default = {
    mobilenet_v1 = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
    mobilenet_v2 = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
    inception_v3 = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
    yolo_v5 = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
    bert_imdb = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
    distilbert_sst2 = {
      cpu_number    = 1
      ram_mib       = 4096
      min_instances = 0
      max_instances = 1
    }
  }
}
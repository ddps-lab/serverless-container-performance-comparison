variable "APIS" {
  type = list(string)
  default = ["gRPC", "REST"]
}

resource "google_cloud_run_service" "cloudrun_mobilenet_v1" {
  count = 2
  name = "mobilenet_v1_${var.APIS[count.index]}"
  location = var.region

  template {
    spec {
      containers {
        image ="${var.docker_registry}/mobilenet_v1-${var.APIS[count.index]}"
        ports {
          name = var.APIS[count.index] == "gRPC" ? "h2c" : "http1"
          container_port = 8500
          protocol = "tcp"
        }

        startup_probe {
          initial_delay_seconds = 10
          timeout_seconds = 1
          period_seconds = 5
          failure_threshold = 1
          tcp_socket {
            port = 8500
          }
        }
      }
    }
  }

  traffic {
    percent = 100
    latest_revision = true
  }
}
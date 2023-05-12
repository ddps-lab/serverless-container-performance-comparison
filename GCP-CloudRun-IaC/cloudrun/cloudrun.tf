variable "APIS" {
  type    = list(string)
  default = ["grpc", "rest"]
}

resource "google_cloud_run_service" "cloudrun_service" {
  count    = 2
  name     = "${replace(var.model_name,"_","-")}-${var.APIS[count.index]}"
  location = var.region
  template {
    spec {
      containers {
        image = "${var.docker_registry}/${var.model_name}-${var.APIS[count.index]}"
        ports {
          name           = var.APIS[count.index] == "grpc" ? "h2c" : "http1"
          container_port = 8500
          protocol       = "TCP"
        }
        resources {
          limits = {
            cpu    = "${var.cpu_number * 1000}m"
            memory = "${var.ram_mib}Mi"
          }
        }

        startup_probe {
          initial_delay_seconds = 10
          timeout_seconds       = 1
          period_seconds        = 5
          failure_threshold     = 1
          tcp_socket {
            port = 8500
          }
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale"  = var.min_instances
        "autoscaling.knative.dev/maxScale" = var.max_instances
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_policy" "cloudrun_noauth" {
  count    = 2
  location = google_cloud_run_service.cloudrun_service[count.index].location
  project  = google_cloud_run_service.cloudrun_service[count.index].project
  service  = google_cloud_run_service.cloudrun_service[count.index].name

  policy_data = var.noauth_policy
}

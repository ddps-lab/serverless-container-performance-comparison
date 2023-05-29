resource "google_cloud_run_service" "cloudrun_service" {
  count    = length(var.APIS)
  name     = "${replace(var.model_name,"_","-")}-${var.APIS[count.index]}"
  location = var.region
  template {
    spec {
      container_concurrency = var.concurrency
      containers {
        image = "${var.docker_registry}/gcp-run-${var.model_name}-${var.APIS[count.index]}"
        ports {
          name           = var.APIS[count.index] == "grpc" ? "h2c" : "http1"
          container_port = var.APIS[count.index] == "grpc" ? 8500 : 8501
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
          failure_threshold     = 3
          tcp_socket {
            port = var.APIS[count.index] == "grpc" ? 8500 : 8501
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
  count    = length(var.APIS)
  location = google_cloud_run_service.cloudrun_service[count.index].location
  project  = google_cloud_run_service.cloudrun_service[count.index].project
  service  = google_cloud_run_service.cloudrun_service[count.index].name

  policy_data = var.noauth_policy
}

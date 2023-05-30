resource "google_cloud_run_service" "cloudrun_service" {
  name     = "${var.prefix}_scpc_rest_bench"
  location = var.region
  template {
    spec {
      container_concurrency = var.concurrency
      containers {
        image = "${var.docker_registry}/scpc_rest_bench:latest"
        ports {
          name           = "http1"
          container_port = 8501
          protocol       = "TCP"
        }
        resources {
          limits = {
            cpu    = "2000m"
            memory = "4096Mi"
          }
        }

        startup_probe {
          initial_delay_seconds = 10
          timeout_seconds       = 1
          period_seconds        = 5
          failure_threshold     = 3
          tcp_socket {
            port = 8501
          }
        }

        env {
          name = "AWS_ACCESS_KEY_ID"
          value = var.aws_access_key
        }

        env {
          name = "AWS_SECRET_ACCESS_KEY"
          value = var.aws_secret_access_key
        }

        env {
          name = "AWS_REGION"
          value = var.aws_region
        }
      }
    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = var.min_instances
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
  location = google_cloud_run_service.cloudrun_service.location
  project  = google_cloud_run_service.cloudrun_service.project
  service  = google_cloud_run_service.cloudrun_service.name

  policy_data = var.noauth_policy
}

resource "google_compute_network" "bench_network" {
  name                    = "${var.prefix}-serverless-bench-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "bench_subnet" {
  name             = "${var.prefix}-serverless-bench-subnet"
  ip_cidr_range    = "192.168.0.0/16"
  network          = google_compute_network.bench_network.id
  ipv6_access_type = "EXTERNAL"
  stack_type       = "IPV4_IPV6"
}

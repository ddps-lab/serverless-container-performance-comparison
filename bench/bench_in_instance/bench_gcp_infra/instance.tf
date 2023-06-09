resource "google_compute_firewall" "bench_instance_firewall_rule" {
  name          = "allow-ssh"
  network       = google_compute_network.bench_network.name
  target_tags   = ["allow-ssh"]
  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_compute_instance" "bench_instance" {
  name         = "${var.prefix}-bench-instance"
  machine_type = "e2-standard-2"
  zone         = "${var.region}-a"

  tags = ["allow-ssh"]
  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 64
    }
  }

  network_interface {
    network    = google_compute_network.bench_network.id
    subnetwork = google_compute_subnetwork.bench_subnet.id
    stack_type = "IPV4_IPV6"
    ipv6_access_config {
      network_tier = "PREMIUM"
    }
    access_config {

    }
  }
  metadata_startup_script = <<-EOF
  apt update
  apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev liblzma-dev unzip curl docker.io awscli

  echo 'export PYENV_ROOT="/pyenv"' >> /etc/bash.bashrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /etc/bash.bashrc
  echo 'eval "$(pyenv init -)"' >> /etc/bash.bashrc

  git clone https://github.com/pyenv/pyenv.git /pyenv
  source /etc/bash.bashrc

  pyenv install 3.10.11
  chmod 777 -R /pyenv
  EOF
}

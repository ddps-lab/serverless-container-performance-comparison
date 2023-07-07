resource "aws_security_group" "bench_instance_sg" {
  ingress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = ""
    from_port        = 22
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "tcp"
    security_groups  = []
    self             = false
    to_port          = 22
  }]
  egress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = ""
    from_port        = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
    }, {
    cidr_blocks      = []
    description      = ""
    from_port        = 0
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids  = []
    protocol         = "-1"
    security_groups  = []
    self             = false
    to_port          = 0
  }]
  vpc_id = aws_vpc.bench_vpc.id

  tags = {
    "Name" = "${var.prefix}-bench-instance-sg"
  }
}


resource "aws_instance" "bench_instance" {
  ami                    = data.aws_ami.ubuntu_ami.id
  instance_type          = "t3.large"
  iam_instance_profile   = aws_iam_instance_profile.bench-instance-role-instance-profile.name
  key_name               = var.keypair
  subnet_id              = aws_subnet.bench_subnet.id
  vpc_security_group_ids = [aws_security_group.bench_instance_sg.id]
  source_dest_check      = false
  tags = {
    "Name" : "${var.prefix}-bench-instance"
  }
  user_data = <<-EOF
  #!/bin/bash
  apt update
  apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev liblzma-dev unzip curl docker.io awscli
  echo 'export PYENV_ROOT="/pyenv"' >> /etc/bash.bashrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /etc/bash.bashrc
  echo 'eval "$(pyenv init -)"' >> /etc/bash.bashrc

  git clone https://github.com/pyenv/pyenv.git /pyenv
  source /etc/bash.bashrc

  /pyenv/bin/pyenv install 3.10.11
  chmod 777 -R /pyenv
  EOF
  root_block_device {
    volume_size           = 64    # 볼륨 크기를 지정합니다.
    volume_type           = "gp2" # 볼륨 유형을 지정합니다.
    delete_on_termination = true  # 인스턴스가 종료될 때 볼륨도 함께 삭제되도록 설정합니다.
  }
}

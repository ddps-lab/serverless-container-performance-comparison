resource "aws_vpc" "bench_vpc" {
  cidr_block                       = "192.168.0.0/16"
  enable_dns_hostnames             = true
  enable_dns_support               = true
  assign_generated_ipv6_cidr_block = true

  tags = {
    Name = "${var.prefix}-bench-vpc"
  }
}

resource "aws_internet_gateway" "bench_igw" {
  vpc_id = aws_vpc.bench_vpc.id
  tags = {
    Name = "${var.prefix}-bench-vpc-igw"
  }
}

resource "aws_subnet" "bench_subnet" {
  vpc_id                                         = aws_vpc.bench_vpc.id
  cidr_block                                     = "192.168.0.0/24"
  ipv6_cidr_block                                = cidrsubnet(aws_vpc.bench_vpc.ipv6_cidr_block, 8, 1)
  availability_zone                              = "${var.region}a"
  enable_resource_name_dns_a_record_on_launch    = true
  enable_resource_name_dns_aaaa_record_on_launch = true
  map_public_ip_on_launch                        = true
  assign_ipv6_address_on_creation                = true
}

resource "aws_route_table" "bench_route_table" {
  vpc_id = aws_vpc.bench_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.bench_igw.id
  }
  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.bench_igw.id
  }
  tags = {
    "Name" : "${var.prefix}-bench-vpc-public-route-table"
  }
}

resource "aws_route_table_association" "bench_route_table_association" {
  subnet_id      = aws_subnet.bench_subnet.id
  route_table_id = aws_route_table.bench_route_table.id
}

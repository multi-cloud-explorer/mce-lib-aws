//output "address" {
//  value = aws_s3_bucket.b.bucket
//}

output "vpc_id" {
  value = aws_default_vpc.default.id
}

output "instance_ip_addr" {
  value = aws_instance.server1.private_ip
  #value = "Instances: ${element(aws_instance.server.*.id, 0)}"
  description = "The private IP address of the main server instance."
}

# Kafka E-Commerce Simulation Project Specification

## Overview

A self-hosted, event-driven Kafka simulation project designed to showcase knowledge in:

- Kafka & Zookeeper cluster deployment and configuration
- Infrastructure automation with Terraform and Ansible
- AWS services integration (Lambda, S3, EC2, VPC, IAM)
- Secure messaging (SASL/SCRAM, ACLs)
- Observability (Confluent Control Center, structured logging)
- Modular, testable Python microservices

The project will simulate an e-commerce order processing workflow using AWS Lambda functions as microservices communicating through Kafka topics.

## Goals

- Deploy a Kafka + Zookeeper cluster across 3 AZs using EC2 instances.
- Configure Kafka security (SASL/SCRAM auth, ACLs).
- Deploy Python-based Lambda functions simulating service events.
- Automate infrastructure and service configuration.
- Implement structured logging and unit testing.
- Run the system for a few hours and fully tear it down afterward to minimize costs.

## Architecture

### Core Components

- **Kafka Cluster:** 3 brokers on EC2 instances
- **Zookeeper Cluster:** 3 nodes on EC2 instances
- **AWS Lambda Services:**
  - `order_generator` (EventBridge trigger)
  - `payment_processor`
  - `inventory_manager`
  - `shipping_handler`
  - `notification_handler`
- **S3 Bucket:** Stores packaged Lambda ZIPs for deployment
- **IAM Roles:** For Lambda execution and deployment permissions
- **Control Center:** Runs on a dedicated EC2 instance for Kafka observability

### Networking

- All Kafka and Zookeeper nodes use **private DNS/IP** for communication.
- EC2 instances are in **public subnets** for SSH/demo access (with notes indicating bastion hosts should be used in production).
- Lambdas are deployed in **VPC-connected subnets** to reach private Kafka endpoints.

## Security

- **Kafka Authentication:** SASL/SCRAM-SHA-512
- **Authorization:** Topic-level ACLs per service user
- **Password Management:** Static credentials defined in Ansible vars (not rotated in v1)
- **Control Center:** Publicly accessible with password protection and IP restriction

## Kafka Topics & Service Responsibilities

| Topic              | Publisher               | Consumers                                |
| ------------------ | ----------------------- | ---------------------------------------- |
| `order_placed`     | `order_generator`       | `inventory_manager`, `payment_processor` |
| `payment_result`   | `payment_processor`     | `shipping_handler`                       |
| `inventory_result` | `inventory_manager`     | `notification_handler`                   |
| `order_shipped`    | `shipping_handler`      | `notification_handler`                   |
| `notifications`    | All services (optional) | `notification_handler`                   |

## Lambda Logic Summary

Each Lambda will:

- Consume/produce Kafka events with a correlation ID (`order_id`)
- Simulate business logic outcomes (e.g., payment success/failure)
- Emit structured JSON logs
- Be packaged as ZIPs for S3-based deployment

### Correlation ID

- `order_id` is generated once by `order_generator`
- Propagated through all service events for traceability

## Event Simulation & Error Handling

- Services use randomization to simulate real-world outcomes:
  - Payment success rate: \~90%
  - Inventory availability: \~80%
  - Shipping triggers only on payment success
- All services are stateless in v1
- Logs include structured JSON entries with `timestamp`, `order_id`, `event_type`, `service`, and `status`

## Logging

- All Lambdas use Python's `logging` module with a custom JSON formatter
- Logs are written to stdout and captured in CloudWatch

## Infrastructure Deployment Flow

Scripts:

- `deploy_all.sh`: Wraps full deployment process
- `deploy_terraform.sh`: Provisions VPC, EC2, Lambda, S3, IAM
- `configure_kafka.sh`: Uses Ansible to set up Zookeeper, Kafka, ACLs
- `deploy_lambdas.sh`: Uploads ZIPs to S3 and applies Lambda configs
- `destroy_all.sh`: Tears down all infra (with `-y` for automation)
- `build_all_zips.sh`: Builds ZIPs from each Lambda folder
- `run_tests.sh`: Runs unit tests across all Lambdas

## Terraform Modules

- VPC, subnets, and security groups
- EC2 instances for Kafka and Zookeeper
- S3 bucket (`kafka-demo-lambda-code`)
- Lambda functions (deployed from S3)
- IAM roles (Lambda execution, deployer access)

## Ansible Responsibilities

- Kafka/Zookeeper installation and configuration
- Broker config (e.g., listeners, advertised.host.name)
- SASL/SCRAM user creation per Lambda service
- Kafka ACLs per topic/service
- Topic creation (no auto-create)

## Unit Testing Plan

- Each Lambda contains:
  - Testable core logic (e.g., `generate_order_event()`)
  - `test_*.py` files using `pytest`
- Project includes `requirements-dev.txt` and `run_tests.sh`

## Deployment Best Practices

- Use S3-based ZIP deployments for Lambdas (not `filename`)
- All infra defined in Terraform for idempotent runs
- Clear logs and exit codes for each deployment stage
- Manual cleanup via `destroy_all.sh -y` if anything fails

## Stretch Goals / Future Enhancements

- Secrets Manager integration for Kafka credentials
- Prometheus + Grafana for richer monitoring
- Kafka Connect (e.g., to S3 or RDS)
- Schema Registry
- CI/CD pipelines (GitHub Actions)
- Multi-cluster Kafka setup with MirrorMaker 2
- Manual test event injector script


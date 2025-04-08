# TODO Checklist

A step-by-step task list for the Kafka E-Commerce Simulation Project. Mark tasks `[x]` as completed.

## Phase A: Project Initialization

- [ ] **A1: Create Repo Structure**
  - [ ] Create top-level folders:
    - `infra/terraform/`
    - `infra/ansible/`
    - `services/`
    - `scripts/`
    - `tests/`
  - [ ] Add a `.gitignore` file (for Python, Terraform, etc.)
  - [ ] Commit the initial structure to version control.

- [ ] **A2: Python Environment & Testing**
  - [ ] Create a `requirements.txt` or `poetry/pyproject.toml` including `pytest`.
  - [ ] Install dependencies (e.g., `pip install -r requirements.txt`).

- [ ] **A3: Hello World Lambda**
  - [ ] In `services/hello_world`, create `hello_world.py` with a minimal function returning `"Hello World"`.
  - [ ] In `tests/`, create `test_hello_world.py` to test the above function using `pytest`.

- [ ] **A4: Validate Tests**
  - [ ] Run `pytest` locally.
  - [ ] Confirm all tests pass.

---

## Phase B: Terraform for AWS Foundations

- [ ] **B1: Minimal Terraform Setup**
  - [ ] In `infra/terraform/main.tf`, configure the AWS provider.
  - [ ] Create a placeholder or local S3 bucket resource.
  - [ ] Run `terraform init`, `terraform plan`, `terraform apply`.
  - [ ] Confirm the bucket is created in AWS.

- [ ] **B2: VPC & Subnets**
  - [ ] Update `main.tf` to add:
    - [ ] VPC
    - [ ] Public subnets
    - [ ] Internet Gateway
  - [ ] `terraform plan`, then `terraform apply`.
  - [ ] Confirm VPC and subnets in AWS.

- [ ] **B3: Security Groups & IAM**
  - [ ] Create an SG for SSH (port 22).
  - [ ] Create an SG for Kafka (ports 9092, 9093, etc.).
  - [ ] Create a minimal IAM role for a Lambda with `AWSLambdaBasicExecutionRole`.
  - [ ] `terraform apply`, confirm resources in AWS.

---

## Phase C: Kafka & Zookeeper Cluster (Infrastructure-Level)

- [ ] **C1: EC2 Instances for Zookeeper & Kafka**
  - [ ] In `main.tf`, add resources for:
    - [ ] 3 Zookeeper EC2 instances (t2.micro).
    - [ ] 3 Kafka EC2 instances (t2.micro).
  - [ ] Use public subnets for the demo (or private if you have a bastion).
  - [ ] Associate them with the SSH SG.
  - [ ] `terraform apply`, confirm EC2 instances in AWS.
  - [ ] Output their private IPs for Ansible inventory.

---

## Phase D: Ansible Configuration for Kafka & Zookeeper

- [ ] **D1: Ansible Inventory & Zookeeper Install**
  - [ ] Generate an inventory file (e.g., `inventory.ini`) from Terraform outputs (IPs, hostnames).
  - [ ] Create an Ansible role or playbook to:
    - [ ] Install Zookeeper (plus Java).
    - [ ] Start/enable Zookeeper via `systemd`.
  - [ ] Run `ansible-playbook` to confirm Zookeeper installation succeeds.

- [ ] **D2: Kafka Installation & SASL Setup**
  - [ ] Create an Ansible role or tasks to:
    - [ ] Install Kafka on the Kafka EC2 instances.
    - [ ] Configure SASL/SCRAM (SCRAM-SHA-512).
    - [ ] Set up listeners, advertised.listeners, etc.
  - [ ] Verify brokers are running and can be reached.

- [ ] **D3: Kafka Users & Topics**
  - [ ] Create SCRAM users for each microservice:
    - `order_generator`
    - `payment_processor`
    - `inventory_manager`
    - `shipping_handler`
    - `notification_handler`
  - [ ] Set ACLs for each user on their respective topics.
  - [ ] Create topics:
    - [ ] `order_placed`
    - [ ] `payment_result`
    - [ ] `inventory_result`
    - [ ] `order_shipped`
    - [ ] `notifications`
  - [ ] Run a check (`kafka-topics.sh`) to verify topics exist.

---

## Phase E: Lambda Microservices

- [ ] **E1: order_generator (TDD)**
  - [ ] Create `services/order_generator/order_generator.py` with a `handler(event, context)`.
  - [ ] Write core logic function `generate_order_event()`.
  - [ ] Create `tests/test_order_generator.py` using pytest to confirm event structure.
  - [ ] For now, log events instead of sending to Kafka.
  - [ ] Build and package the Lambda (e.g., `zip` or `build_all_zips.sh`).

- [ ] **E2: payment_processor (TDD)**
  - [ ] Create `services/payment_processor/payment_processor.py` with `handler(event, context)`.
  - [ ] Write `process_payment(order_event)` logic (simulate ~90% success).
  - [ ] Create `tests/test_payment_processor.py` (mock random or check distribution).
  - [ ] Log results, no Kafka integration yet.

- [ ] **E3: inventory_manager, shipping_handler, notification_handler (TDD)**
  - [ ] **inventory_manager**:
    - [ ] `handler(event, context)`
    - [ ] `check_inventory(order_event)` (~80% success)
    - [ ] `tests/test_inventory_manager.py`
  - [ ] **shipping_handler**:
    - [ ] `handler(event, context)`
    - [ ] `ship_order(payment_result)`
    - [ ] `tests/test_shipping_handler.py`
  - [ ] **notification_handler**:
    - [ ] `handler(event, context)`
    - [ ] `notify(...)`
    - [ ] `tests/test_notification_handler.py`
  - [ ] Log all events.

- [ ] **E4: Integrate with Kafka**
  - [ ] Configure each Lambda to:
    - [ ] Connect to the Kafka cluster (SASL/SCRAM credentials).
    - [ ] `order_generator` → publish to `order_placed`.
    - [ ] `payment_processor` → consume `order_placed`, publish `payment_result`.
    - [ ] `inventory_manager` → consume `order_placed`, publish `inventory_result`.
    - [ ] `shipping_handler` → consume `payment_result`, publish `order_shipped`.
    - [ ] `notification_handler` → consume `inventory_result` or `order_shipped` to log notifications.
  - [ ] Update unit tests to mock Kafka producer/consumer calls.
  - [ ] Update Terraform to supply environment variables (broker endpoints, credentials) to each Lambda.
  - [ ] Re-deploy Lambdas; confirm they can reach Kafka in the VPC.

---

## Phase F: Observability & Control Center

- [ ] **F1: Control Center Installation**
  - [ ] Extend Terraform to add one more EC2 instance for Control Center.
  - [ ] Ansible role or tasks to install Confluent Control Center.
  - [ ] Verify broker metrics and topic details appear in Control Center.

---

## Phase G: Integration & End-to-End Testing

- [ ] **G1: Full Deployment & Integration Tests**
  - [ ] Run `terraform apply` for all resources.
  - [ ] Run Ansible playbooks to configure Zookeeper/Kafka, create users/topics.
  - [ ] Deploy Lambdas with environment variables for broker connection.
  - [ ] **Trigger order_generator**:
    - [ ] Option A: Manual invocation from AWS Console.
    - [ ] Option B: EventBridge schedule for automatic invocation.
  - [ ] Check:
    - [ ] Kafka topics flow in Control Center.
    - [ ] CloudWatch logs for each Lambda.
    - [ ] Validate success/failure logic for payment and inventory.

---

## Phase H: Teardown & Validation

- [ ] **H1: `destroy_all.sh` & Cleanup**
  - [ ] Script calls `terraform destroy -auto-approve`.
  - [ ] Removes leftover S3 objects (Lambda code zips, etc.).
  - [ ] Verify all AWS resources are deleted.
  - [ ] Confirm no EC2, VPC, or IAM roles remain.

---

## Additional Notes / Stretch Goals

- [ ] **Secrets & Security**:
  - [ ] Consider storing Kafka passwords in AWS Secrets Manager or Parameter Store.
  - [ ] Restrict SG access further (bastion host or private subnets).
  - [ ] Use TLS for Kafka communication.
- [ ] **Monitoring**:
  - [ ] Add Prometheus + Grafana for deeper metrics.
  - [ ] Integrate structured logs with JSON format in CloudWatch.
- [ ] **CI/CD**:
  - [ ] GitHub Actions or similar for automated tests & Terraform validation.
- [ ] **Cleanup**:
  - [ ] Confirm documentation is up-to-date in `README.md`.
  - [ ] Summarize cost and usage estimates for ephemeral runs.

---


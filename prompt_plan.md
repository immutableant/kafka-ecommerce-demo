## 1. High-Level Blueprint

1. **Infrastructure**  
   - **Terraform** to provision AWS resources:  
     - VPC, subnets, and security groups  
     - EC2 instances (Kafka, Zookeeper, Control Center)  
     - S3 bucket for Lambda deployment packages  
     - IAM roles and policies  
     - Lambda functions (pointing to code in S3)  
   - **Ansible** to configure the Kafka + Zookeeper cluster:  
     - Install Kafka and Zookeeper  
     - Create SASL/SCRAM users and ACLs  
     - Create Kafka topics  

2. **Python Lambda Services**  
   - **Order Generator**  
   - **Payment Processor**  
   - **Inventory Manager**  
   - **Shipping Handler**  
   - **Notification Handler**  
   Each Lambda simulates business logic, uses structured logging, and is tested with `pytest`.

3. **Scripts**  
   - `deploy_all.sh`  
   - `deploy_terraform.sh`  
   - `configure_kafka.sh`  
   - `deploy_lambdas.sh`  
   - `destroy_all.sh`  
   - `build_all_zips.sh`  
   - `run_tests.sh`  

4. **Observability**  
   - **Kafka Control Center** on a dedicated EC2 instance.  
   - **Structured logging** (JSON) for all Lambdas.  

5. **Testing**  
   - **Unit tests** for each Lambda.  
   - Potential system tests after partial deployment.  

---

## 2. Break the Blueprint into Iterative Chunks

Here we split the entire effort into sequential “chunks,” each building on the last:

1. **Chunk A: Project Initialization**  
   - Repository structure, basic scaffolding, initial testing framework.
   - Basic “hello world” Lambda to prove local invocation and test pipeline.

2. **Chunk B: Terraform for AWS Foundations**  
   - Create VPC, subnets, security groups, S3 bucket, basic IAM roles.
   - Verify resources with minimal cost.

3. **Chunk C: Kafka & Zookeeper Cluster Setup (Infrastructure)**  
   - Add EC2 for Zookeeper + Kafka in Terraform.
   - Validate connectivity with placeholders (no real config yet).

4. **Chunk D: Ansible Configuration for Kafka & Zookeeper**  
   - Install Kafka, Zookeeper, set up SASL/SCRAM, define initial topics.
   - Validate cluster health with minimal testing.

5. **Chunk E: Lambda Microservices**  
   - Add Terraform definitions for each Lambda function (pointing to code in S3).
   - Python code for each microservice, plus tests.

6. **Chunk F: Observability & Control Center**  
   - Deploy Confluent Control Center on a dedicated EC2 instance.
   - Validate basic metrics and logging.

7. **Chunk G: Integration & End-to-End Testing**  
   - Wire topics to Lambdas properly.
   - Conduct a small, timed run to see end-to-end flow.
   - Observe logs and metrics, validate success.

8. **Chunk H: Teardown & Validation**  
   - Ensure `destroy_all.sh` cleans everything.
   - Document final instructions and results.

---

## 3. Deeper Breakdown of Each Chunk

We refine each chunk into smaller steps. Notice how each step is small but functional.

### Chunk A: Project Initialization

1. **Create Repository & Base Folders**  
   - `infra/terraform`  
   - `infra/ansible`  
   - `services/order_generator` (and so on)  
   - `scripts/`  
2. **Set up Basic `pyproject.toml` or `requirements.txt`**  
   - For shared dev tools (e.g., `pytest`).  
3. **Hello World Lambda**  
   - Minimal Python Lambda function.  
4. **Test Suite Setup**  
   - `pytest` scaffolding for the Hello World Lambda.  
5. **Sanity Check**  
   - Local invocation with `pytest` passing.  

### Chunk B: Terraform for AWS Foundations

1. **Initialize Terraform**  
   - `terraform init` and create a minimal main file with `provider "aws"`.  
2. **Create VPC & Subnets**  
   - Public subnets (for demonstration).  
3. **Create Security Groups**  
   - For SSH access, for Kafka cluster, and for Lambdas.  
4. **S3 Bucket**  
   - `kafka-demo-lambda-code`.  
5. **Basic IAM Roles**  
   - Minimal policy for a test Lambda execution role.  
6. **Validate**  
   - `terraform plan` / `terraform apply`.  

### Chunk C: Kafka & Zookeeper Cluster (Infra-Level)

1. **EC2 Instances**  
   - 3 Zookeeper + 3 Kafka (some might be shared, but better to isolate for demonstration).  
2. **User Data / Minimal Setup**  
   - Placeholder to ensure they can SSH and are healthy.  
3. **Output Tests**  
   - Terraform outputs listing EC2 IP addresses.  
4. **Skeleton for Ansible Inventory**  
   - Automatic generation from Terraform outputs.  

### Chunk D: Ansible Configuration for Kafka & Zookeeper

1. **Install Zookeeper & Kafka**  
   - Use roles or tasks that install from official packages.  
2. **Create Kafka Users / SASL Credentials**  
   - Each service (e.g., `order_generator`) has a username/password.  
3. **ACLs & Topics**  
   - `order_placed`, `payment_result`, `inventory_result`, `order_shipped`, `notifications`.  
4. **Validation**  
   - Command-line check that Kafka topics exist, and cluster is stable.  

### Chunk E: Lambda Microservices

1. **order_generator**  
   - **Test**: `test_order_generator.py` with random outcomes.  
   - **Implementation**: Produces events to `order_placed`.  
2. **payment_processor**  
   - **Test**: Mocks Kafka consumption, checks logic.  
   - **Implementation**: Reads from `order_placed`, writes to `payment_result`.  
3. **inventory_manager**  
   - **Test**: Similar pattern, uses `order_placed` → emits `inventory_result`.  
4. **shipping_handler**  
   - **Test**: Consumes from `payment_result`, emits to `order_shipped`.  
5. **notification_handler**  
   - **Test**: Consumes `inventory_result` or `order_shipped` → logs a notification event.  
6. **Integration**  
   - Terraform definitions to wire each Lambda’s code from S3 and assign correct Kafka credentials.  

### Chunk F: Observability & Control Center

1. **Control Center Installation**  
   - On a dedicated EC2 instance (via Ansible).  
2. **Validate Dashboards**  
   - Check broker metrics, topics, consumer groups.  

### Chunk G: Integration & End-to-End Testing

1. **Deploy**  
   - Run `deploy_all.sh` end-to-end.  
2. **Trigger**  
   - `order_generator` automatically triggers via an EventBridge schedule, or manual invocation.  
3. **Observe**  
   - Check logs in CloudWatch, check Kafka dashboards.  
4. **Verify**  
   - Payment success/fail distribution, inventory checks, shipping triggered.  

### Chunk H: Teardown & Validation

1. **Destroy**  
   - `destroy_all.sh` with a yes flag.  
2. **Check**  
   - All AWS resources removed (S3, EC2, etc.).  
3. **Document**  
   - Summarize the ephemeral run costs and next steps.  

---

## 4. Final Iteration of Step-by-Step, with Right-Sized Tasks

To ensure each phase is implementable with strong testing but without huge leaps, here is an even more granular breakdown. We keep them small, so each can be tested (like “write a minimal Ansible role to install Zookeeper” then test, etc.) while still moving forward.

1. **Initialize & Basic Tests**  
   - (A1) Create the repo folder structure, add `.gitignore`, and commit.  
   - (A2) Set up `requirements.txt` (or `poetry/pyproject.toml`) for dev dependencies.  
   - (A3) Write a single minimal Python function (`hello_world.py`) with a unit test.  
   - (A4) Validate tests pass locally.

2. **Minimal Terraform Foundation**  
   - (B1) Create a single Terraform file (`main.tf`) with `provider "aws"` config.  
   - (B2) Add a minimal resource (e.g., an S3 bucket).  
   - (B3) `terraform init`, `terraform plan` & `terraform apply`.  
   - (B4) Confirm the S3 bucket is created in AWS.  

3. **VPC & Subnets**  
   - (B5) Add VPC, public subnets, and an Internet gateway resource.  
   - (B6) Output VPC/subnet IDs.  
   - (B7) `terraform apply`, confirm VPC exists.  

4. **Security Groups & IAM**  
   - (B8) Create a basic SG for SSH and for Kafka.  
   - (B9) Create a minimal IAM role for Lambda.  
   - (B10) `terraform apply`, confirm roles and SG exist.  

5. **EC2 for Zookeeper & Kafka**  
   - (C1) Add 3 Zookeeper instances in different subnets.  
   - (C2) Add 3 Kafka broker instances in different subnets.  
   - (C3) `terraform apply`, confirm EC2 is up.  
   - (C4) Output their private IPs for Ansible inventory.  

6. **Ansible Inventory & Basic Zookeeper Install**  
   - (D1) Generate an Ansible inventory file from Terraform outputs.  
   - (D2) Create a minimal role or task file to install Zookeeper on the Zookeeper EC2s.  
   - (D3) Validate (e.g., SSH in, run `systemctl status zookeeper`).  

7. **Kafka Installation & SASL Setup**  
   - (D4) Create a minimal role or tasks to install Kafka.  
   - (D5) Configure SASL/SCRAM on each broker.  
   - (D6) Validate brokers are running.  

8. **Create Kafka Users & Topics**  
   - (D7) For each microservice, create a user with a password.  
   - (D8) Create topics (`order_placed`, etc.).  
   - (D9) Confirm topics exist via `kafka-topics.sh`.  

9. **Lambda Services (One by One)**  
   - (E1) `order_generator`:  
     - **Test**: `test_order_generator.py` with a mock.  
     - **Implementation**: minimal logic.  
   - (E2) `payment_processor`:  
     - **Test**: `test_payment_processor.py`.  
     - **Implementation**.  
   - (E3) `inventory_manager` … etc.  

   Each time:
   - Write the test.  
   - Implement the function.  
   - Build the ZIP (`build_all_zips.sh`).  
   - Upload to S3 and reference in Terraform.  
   - Deploy, run a manual test with CloudWatch logs.  

10. **Control Center**  
   - (F1) Add a new EC2 for Control Center in Terraform.  
   - (F2) Use Ansible to install and configure Confluent Control Center.  
   - (F3) Confirm broker metrics visible.  

11. **End-to-End Integration**  
   - (G1) Add triggers or a script to invoke `order_generator`.  
   - (G2) Watch events flow in CloudWatch and Control Center.  
   - (G3) Verify logs and success/failure rates.  

12. **Teardown**  
   - (H1) Ensure `destroy_all.sh` calls `terraform destroy`, removes S3 objects, etc.  
   - (H2) Validate nothing is left behind.  

---

## 5. Series of Prompts for a Code-Generation LLM

Below are example prompts for each step. You would copy each prompt into your code-generation LLM (such as ChatGPT, GPT-4, etc.) in sequence. Each prompt includes context about what has been done so far and what we want next. This ensures continuity and that no code is “orphaned.”

> **Note:** Each prompt is enclosed in triple backticks for clarity. You can adjust the text or references as necessary for your environment.

---

### Prompt A1: Repository Structure & Basic Test Setup

```
You are building a Kafka E-Commerce Simulation project in Python, with Terraform and Ansible for infrastructure. 
Your goal in this step is to:
1. Create a basic repo structure:
   - infra/
     - terraform/
     - ansible/
   - services/
   - scripts/
   - tests/
2. Initialize a Python environment with a requirements.txt that includes pytest.
3. Provide a minimal "hello_world.py" function in services/hello_world that returns the string "Hello World".
4. Provide a test_hello_world.py in tests/ that uses pytest to verify that "hello_world.py" returns "Hello World".

Write the code or file structure for all of this in a well-organized manner.
Explain how to run the test locally using pytest.
```

---

### Prompt A2: Terraform Initialization (Minimal)

```
We have our repo structure with a Python environment for testing. Now we want to start setting up Terraform for AWS. 

Tasks:
1. In infra/terraform, create a main.tf that:
   - Configures the AWS provider (assume region us-east-1).
   - Has a placeholder for a backend (we'll add remote state later).
2. Include a simple resource, e.g., an S3 bucket called "kafka-demo-lambda-code-[random suffix]".
3. Show how to run 'terraform init', 'terraform plan', and 'terraform apply'.
4. Explain any relevant variables or outputs to add, if needed.

Write the Terraform code and any needed instructions.
```

---

### Prompt B1: VPC & Subnets

```
We now have a minimal Terraform setup with an S3 bucket. Next:
1. Add a VPC, public subnets, and an Internet Gateway to main.tf.
2. Output the VPC ID and subnet IDs.
3. Show how to confirm these resources in AWS after applying.

Write the Terraform code changes and any necessary details.
```

---

### Prompt C1: Security Groups & IAM Roles

```
Continuing the Terraform build:
1. Create a Security Group that allows SSH (port 22) from anywhere (we'll refine later).
2. Create a second Security Group for Kafka listeners (ports 9092, 9093, etc.) restricting to internal traffic only.
3. Create a minimal IAM role for a Lambda with 'AWSLambdaBasicExecutionRole' attached.
4. Provide updated Terraform code and how to reference these in outputs.

Ensure no orphan resources, all included in main.tf or sub-files. 
```

---

### Prompt C2: EC2 for Zookeeper & Kafka

```
Now we want to provision EC2 instances for Zookeeper and Kafka:
1. Create three EC2 instances for Zookeeper (t2.micro is fine for the demo).
2. Create three EC2 instances for Kafka (t2.micro again, for the demo).
3. Associate the SSH Security Group with them.
4. Provide Terraform code that references the public subnets you made earlier.
5. Output the instance IDs and private IPs.

Write the updated Terraform code, ensuring no big leaps. 
```

---

### Prompt D1: Ansible Inventory & Zookeeper Installation

```
We have Terraform creating EC2 instances for Zookeeper and Kafka. Now let's start configuring them with Ansible:
1. Show how to export Terraform outputs (EC2 IP addresses) to an Ansible inventory file (inventory.ini).
2. Write an Ansible playbook or role to install Zookeeper on the three Zookeeper EC2 instances.
3. Provide tasks for installing Java and Zookeeper from a known repository.
4. Ensure a systemd service is started for Zookeeper. 
5. Provide instructions on how to run this Ansible playbook.

No orphan code – integrate with the existing infra/ansible directory.
```

---

### Prompt D2: Kafka Installation & SASL/SCRAM Setup

```
We now have Zookeeper installed. Next:
1. Create an Ansible role or tasks for installing Kafka on the three Kafka EC2 instances.
2. Configure the brokers to use SASL/SCRAM:
   - Accept a username/password for each microservice (e.g., 'order_generator', 'payment_processor').
   - Use SCRAM-SHA-512.
3. Provide instructions on setting the relevant broker config in server.properties (like listeners, advertised.listeners).
4. Show how to verify the cluster is up and broker is running with SASL enabled.

Include code references for the tasks and highlight any potential pitfalls.
```

---

### Prompt D3: Create Kafka Users & Topics

```
We have Kafka installed with SASL/SCRAM. Now:
1. In Ansible, add tasks to create Kafka users (SCRAM credentials) for 'order_generator', 'payment_processor', 'inventory_manager', 'shipping_handler', 'notification_handler'.
2. Create the five Kafka topics:
   - 'order_placed'
   - 'payment_result'
   - 'inventory_result'
   - 'order_shipped'
   - 'notifications'
3. Apply ACLs to limit each user to its relevant topics. 
4. Demonstrate a check (kafka-topics.sh) to confirm the topics are created.

Ensure the code is integrated with the existing roles or tasks, no orphan files.
```

---

### Prompt E1: Lambda: order_generator (TDD)

```
We are ready to start coding the Lambda services. We'll do test-driven development for each. Focus on 'order_generator' first:
1. In services/order_generator, create a file 'order_generator.py' that has a function 'handler(event, context)' for AWS Lambda entry.
2. Write a separate Python module for the core logic, e.g., 'generate_order_event()' – so we can unit test it easily.
3. Create 'test_order_generator.py' in tests/ that uses pytest to:
   - Verify that 'generate_order_event()' produces an event dict with a random order_id, event_type='order_placed', etc.
4. Provide minimal logic in 'order_generator.py' that, once running on AWS Lambda, would produce a Kafka message to 'order_placed'.
   - For now, just log the event instead of actually sending to Kafka. We'll integrate Kafka in a later step or partial step.

We want all relevant code, plus instructions on how to run the tests and package the Lambda into a ZIP.
```

---

### Prompt E2: Lambda: payment_processor (TDD)

```
Next microservice: 'payment_processor':
1. In services/payment_processor, create 'payment_processor.py' with a 'handler(event, context)'.
2. Create a core logic function 'process_payment(order_event)' that randomly returns success/failure with about a 90% success rate.
3. Create 'test_payment_processor.py' verifying the random outcome distribution is correct (you can mock random or check boundary cases).
4. For now, just log the result. We'll integrate Kafka in subsequent steps.
5. Provide instructions for testing (pytest) and building the zip.

Ensure code references the same project structure.
```

---

### Prompt E3: Lambda: inventory_manager, shipping_handler, notification_handler (TDD)

```
We will do the remaining three Lambdas in the same TDD style. 
1. inventory_manager
2. shipping_handler
3. notification_handler

For each:
- Provide a 'handler(event, context)' entrypoint.
- Provide a core logic function tested by pytest.
- The logic should randomly simulate outcomes (e.g., 80% item in stock, shipping triggers only on successful payment).
- For now, only log events, do not yet integrate with Kafka.

Write the code, test files, and packaging instructions. Keep it incremental.
```

---

### Prompt E4: Integrating Lambdas with Kafka

```
Now we integrate Kafka in each Lambda so they actually read from and write to topics:
1. Explain how to set up a Python Kafka client in each service, using the SASL/SCRAM credentials created by Ansible.
2. For 'order_generator', have it publish messages to 'order_placed' upon invocation.
3. For 'payment_processor', subscribe to 'order_placed' and publish to 'payment_result'.
4. For 'inventory_manager', subscribe to 'order_placed' and publish to 'inventory_result'.
5. For 'shipping_handler', subscribe to 'payment_result' and publish to 'order_shipped'.
6. For 'notification_handler', subscribe to 'inventory_result' or 'order_shipped' and log notifications. 
   - Alternatively, publish to 'notifications' if we want one consolidated place.

Each step should be TDD style: write or update tests to mock Kafka connections, then implement.
Also, provide updated Terraform code that sets environment variables (broker endpoints, username/password) so the Lambdas can connect inside the VPC.
```

---

### Prompt F1: Control Center Installation

```
We want to add Confluent Control Center on a separate EC2 instance:
1. Extend Terraform to create one more EC2 with the same SSH SG or a separate SG.
2. Write an Ansible role to install Confluent Control Center, referencing the existing Kafka cluster.
3. Verify that the cluster metrics appear in Control Center's UI.

Provide the code or steps, ensuring it doesn’t conflict with existing roles.
```

---

### Prompt G1: End-to-End Integration Test & Observability

```
Now let's run an end-to-end test:
1. After deploying all infra (terraform apply) and configuring with Ansible, deploy Lambdas with environment variables set for broker endpoints.
2. Manually trigger 'order_generator' or set up an EventBridge schedule to invoke it every minute.
3. Watch Kafka topics in Control Center and CloudWatch logs for each Lambda.
4. Provide test instructions to see if the full workflow completes:
   - order_generator -> order_placed
   - payment_processor -> payment_result
   - inventory_manager -> inventory_result
   - shipping_handler -> order_shipped
   - notification_handler -> final notification

Document any debugging tips or known issues.
```

---

### Prompt H1: Teardown & Cleanup

```
Finally, we want a clean teardown:
1. Write a script 'destroy_all.sh' that:
   - Calls 'terraform destroy -auto-approve'
   - Removes any leftover S3 objects if needed
   - Optionally cleans up local build artifacts
2. Provide instructions on verifying that no AWS resources remain.

Ensure no orphan resources remain, and that this script is safe to run.
```

---

# Vertex AI Evaluation Service - Setup Guide

Complete setup guide for integrating Vertex AI Evaluation Service with the Architecture Domain ANS Agent.

## 🎯 Overview

This directory contains a **production-ready implementation** of Google Cloud's Vertex AI Evaluation Service for comprehensive agent evaluation with:

- ✅ Visual dashboards in Vertex AI Console
- ✅ Automated metrics (safety, groundedness, tool use quality)
- ✅ Custom ANS-specific metrics
- ✅ BigQuery integration for historical analysis
- ✅ Version comparison capabilities
- ✅ CI/CD integration ready

## 📁 Files Added

```
eval/
├── vertex_ai_evaluation.py         # Core Vertex AI Evaluation Service
├── run_vertex_ai_evaluation.py     # Production evaluation runner
├── custom_metrics.py                # ANS-specific custom metrics
├── vertex_ai_setup.md              # This file - setup instructions
└── requirements_vertex_ai.txt      # Additional dependencies
```

## 🔧 Prerequisites

### 1. GCP Project Configuration

Enable required APIs:

```bash
# Set your project
export PROJECT_ID="gft-bu-gcp"
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable generativelanguage.googleapis.com
```

### 2. Service Account Setup

Create service account with required permissions:

```bash
# Create service account
gcloud iam service-accounts create vertex-ai-evaluator \
  --display-name="Vertex AI Evaluator" \
  --description="Service account for running Vertex AI evaluations"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"

# Download key (for local development)
gcloud iam service-accounts keys create vertex-ai-evaluator-key.json \
  --iam-account=vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com
```

### 3. Create GCS Bucket

```bash
# Create staging bucket
gsutil mb -p $PROJECT_ID -l us-central1 gs://$PROJECT_ID-eval-staging

# Set lifecycle policy (optional - auto-delete old datasets after 30 days)
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [{
      "action": {"type": "Delete"},
      "condition": {"age": 30}
    }]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://$PROJECT_ID-eval-staging
```

### 4. Create BigQuery Dataset

```bash
# Create dataset
bq mk --dataset \
  --location=us-central1 \
  --description="Architecture Domain ANS Agent Evaluation Results" \
  $PROJECT_ID:architecture_domain_ans_eval

# Create results table
bq mk --table \
  $PROJECT_ID:architecture_domain_ans_eval.evaluation_results \
  evaluation_id:STRING,display_name:STRING,agent_id:STRING,timestamp:TIMESTAMP,metrics_summary:JSON,pass_rate:FLOAT
```

## 📦 Installation

### Install Additional Dependencies

```bash
cd architecture-domain-ans

# Install Vertex AI SDK and additional dependencies
pip install -r eval/requirements_vertex_ai.txt

# Or install individually
pip install google-cloud-aiplatform>=1.38.0
pip install google-cloud-storage>=2.10.0
pip install google-cloud-bigquery>=3.13.0
```

## 🚀 Usage

### 1. Basic Evaluation

Run a full evaluation with all test cases:

```bash
# Set credentials (if using service account key)
export GOOGLE_APPLICATION_CREDENTIALS="vertex-ai-evaluator-key.json"
export GOOGLE_CLOUD_PROJECT="gft-bu-gcp"

# Run evaluation
cd architecture-domain-ans
python -m eval.run_vertex_ai_evaluation --agent-version v1.0
```

**Output**:
```
================================================================================
🚀 VERTEX AI EVALUATION SERVICE - Architecture Domain ANS Agent
================================================================================

📊 Initializing Vertex AI Evaluation Service
────────────────────────────────────────────────────────────────────────────────

Configuration:
  Project: gft-bu-gcp
  Location: us-central1
  Staging Bucket: gs://gft-bu-gcp-eval-staging
  BigQuery Dataset: architecture_domain_ans_eval

✅ Initialization complete

📊 Evaluation Dataset
────────────────────────────────────────────────────────────────────────────────

Total test cases: 8
Categories: {
  "renovacao_favoravel": 1,
  "nova_contratacao_ressalvas": 1,
  ...
}

📊 Preparing Evaluation Dataset
────────────────────────────────────────────────────────────────────────────────

✅ Dataset prepared: eval_dataset_20251129_230000.jsonl (15234 bytes)
Uploading to GCS: gs://gft-bu-gcp-eval-staging/datasets/eval_dataset_20251129_230000.jsonl
✅ Upload complete: gs://gft-bu-gcp-eval-staging/datasets/eval_dataset_20251129_230000.jsonl

📊 Running Evaluation - Agent: architecture-domain-ans-v1.0
────────────────────────────────────────────────────────────────────────────────

Standard Metrics: tool_use_quality, response_quality, safety, groundedness, instruction_following
Custom Metrics: 5 ANS-specific metrics

⏳ Evaluation in progress... This may take several minutes.

✅ Evaluation completed successfully!
📊 Dashboard: https://console.cloud.google.com/vertex-ai/generative/evaluation/12345?project=gft-bu-gcp
💾 Results: gft-bu-gcp.architecture_domain_ans_eval.evaluation_results

📊 Evaluation Results
────────────────────────────────────────────────────────────────────────────────

✅ Status: COMPLETED
📊 Dashboard: https://console.cloud.google.com/vertex-ai/generative/evaluation/12345?project=gft-bu-gcp
💾 BigQuery Table: gft-bu-gcp.architecture_domain_ans_eval.evaluation_results

📈 Metrics Summary:
   tool_use_quality: 0.9200
   response_quality: 0.8800
   safety: 0.9500
   groundedness: 0.9100
   onetrust_integration: 0.8750
   cmdb_integration: 0.8750
   ...

📊 Next Steps
────────────────────────────────────────────────────────────────────────────────

1. Open Vertex AI Console to view detailed dashboard:
   https://console.cloud.google.com/vertex-ai/generative/evaluation/12345?project=gft-bu-gcp

2. Query results from BigQuery:
   bq query 'SELECT * FROM `gft-bu-gcp.architecture_domain_ans_eval.evaluation_results` LIMIT 10'

3. Compare with previous versions:
   python -m eval.run_vertex_ai_evaluation --compare v1.0 v1.1

================================================================================
🎉 Evaluation complete!
================================================================================
```

### 2. Compare Versions

Compare evaluation results between two agent versions:

```bash
python -m eval.run_vertex_ai_evaluation --compare v1.0 v1.1
```

**Output**:
```
📊 Comparing Versions: v1.0 vs v1.1
────────────────────────────────────────────────────────────────────────────────

📊 Comparison Results:
   Version A: v1.0
   Version B: v1.1

📈 Metrics Delta:
   📈 tool_use_quality: 0.9200 → 0.9450 (+0.0250, +2.72%)
   📈 response_quality: 0.8800 → 0.9100 (+0.0300, +3.41%)
   ➡️ safety: 0.9500 → 0.9500 (+0.0000, +0.00%)
   📈 groundedness: 0.9100 → 0.9300 (+0.0200, +2.20%)
   📈 onetrust_integration: 0.8750 → 0.9000 (+0.0250, +2.86%)

✅ Comparison saved: eval/results/comparison_20251129_230500.json
```

### 3. Query Historical Results

View past evaluation runs:

```bash
python -m eval.run_vertex_ai_evaluation --history --limit 10
```

**Output**:
```
📊 Historical Evaluation Results (Last 10)
────────────────────────────────────────────────────────────────────────────────

Found 5 evaluation runs:

1. architecture-domain-ans-eval-20251129-230000
   Agent: architecture-domain-ans-v1.1
   Timestamp: 2025-11-29 23:00:00
   Pass Rate: 92.5%
   Evaluation ID: projects/gft-bu-gcp/locations/us-central1/evaluations/12345

2. architecture-domain-ans-eval-20251128-150000
   Agent: architecture-domain-ans-v1.0
   Timestamp: 2025-11-28 15:00:00
   Pass Rate: 87.5%
   Evaluation ID: projects/gft-bu-gcp/locations/us-central1/evaluations/12344
   ...
```

### 4. Dry Run (Test Without Running Evaluation)

Prepare dataset and validate configuration without running evaluation:

```bash
python -m eval.run_vertex_ai_evaluation --dry-run --save-dataset
```

### 5. Custom Metrics Only

Run evaluation with only ANS-specific custom metrics:

```bash
python -m eval.run_vertex_ai_evaluation \
  --metrics tool_use_quality response_quality \
  --agent-version v1.0
```

### 6. Skip Custom Metrics (Standard Only)

```bash
python -m eval.run_vertex_ai_evaluation --skip-custom-metrics
```

## 📊 Viewing Results

### 1. Vertex AI Console (Visual Dashboard)

Open the dashboard URL from the evaluation output:

```
https://console.cloud.google.com/vertex-ai/generative/evaluation/{eval_id}?project=gft-bu-gcp
```

**Dashboard Features**:
- 📊 Overall performance metrics
- 📈 Metrics trend over time
- 🔍 Detailed test case results
- 🔄 Version comparison
- 📤 Export to CSV/JSON
- 🔗 Share with team

### 2. BigQuery (SQL Analysis)

Query results directly from BigQuery:

```sql
-- Latest evaluation
SELECT 
  display_name,
  agent_id,
  timestamp,
  JSON_EXTRACT_SCALAR(metrics_summary, '$.tool_use_quality') as tool_use,
  JSON_EXTRACT_SCALAR(metrics_summary, '$.response_quality') as response,
  pass_rate
FROM `gft-bu-gcp.architecture_domain_ans_eval.evaluation_results`
ORDER BY timestamp DESC
LIMIT 1;

-- Trend analysis (last 30 days)
SELECT 
  DATE(timestamp) as date,
  agent_id,
  AVG(CAST(JSON_EXTRACT_SCALAR(metrics_summary, '$.tool_use_quality') AS FLOAT64)) as avg_tool_use,
  AVG(pass_rate) as avg_pass_rate
FROM `gft-bu-gcp.architecture_domain_ans_eval.evaluation_results`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY date, agent_id
ORDER BY date DESC;

-- Compare versions
SELECT 
  agent_id,
  AVG(pass_rate) as avg_pass_rate,
  COUNT(*) as num_evaluations
FROM `gft-bu-gcp.architecture_domain_ans_eval.evaluation_results`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY agent_id
ORDER BY avg_pass_rate DESC;
```

### 3. Local JSON Files

Results are also saved locally in `eval/results/`:

```bash
# View latest result
cat eval/results/vertex_ai_evaluation_$(ls -t eval/results/ | grep vertex_ai | head -1)

# Pretty print with jq
jq '.' eval/results/vertex_ai_evaluation_20251129_230000.json
```

## 🔄 CI/CD Integration

### GitHub Actions

Create `.github/workflows/vertex-ai-evaluation.yml`:

```yaml
name: Vertex AI Evaluation (Weekly)

on:
  schedule:
    - cron: '0 2 * * 1'  # Every Monday at 2 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  evaluate:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd adk-samples/python/agents/architecture-domain-ans
          pip install -r requirements.txt
          pip install -r eval/requirements_vertex_ai.txt
      
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Run Vertex AI Evaluation
        run: |
          cd adk-samples/python/agents/architecture-domain-ans
          python -m eval.run_vertex_ai_evaluation \
            --agent-version ${GITHUB_REF##*/} \
            --project gft-bu-gcp
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: vertex-ai-evaluation-results
          path: adk-samples/python/agents/architecture-domain-ans/eval/results/
```

### Cloud Scheduler (Weekly Evaluation)

```bash
# Create Cloud Scheduler job
gcloud scheduler jobs create http vertex-ai-eval-weekly \
  --schedule="0 2 * * 1" \
  --uri="https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/vertex-ai-evaluation:run" \
  --http-method=POST \
  --oauth-service-account-email=vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com \
  --location=us-central1
```

## 📊 Cost Estimation

### Vertex AI Evaluation API

- **Per Evaluation**: ~$5-10 USD
  - API calls: ~$0.10 per 1K requests
  - Model invocations: ~$4-8 (depends on model and tokens)
  - BigQuery storage: ~$0.02 per GB

### Monthly Cost (Recommended Usage)

| Scenario | Frequency | Monthly Cost |
|----------|-----------|--------------|
| **CI/CD (ADK)** | Unlimited | **$0.00** ✅ |
| **Production (Vertex AI)** | Weekly (4x) | **~$20-40** 💰 |
| **Ad-hoc Evaluations** | As needed | Variable |

**Recommendation**: Use ADK for CI/CD (daily), Vertex AI for production releases (weekly)

## 🔒 Security Best Practices

### 1. Use Workload Identity (GKE/Cloud Run)

Instead of service account keys, use Workload Identity:

```bash
# Bind Kubernetes service account to GCP service account
gcloud iam service-accounts add-iam-policy-binding \
  vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:$PROJECT_ID.svc.id.goog[default/vertex-ai-eval]"
```

### 2. Least Privilege Permissions

Only grant minimum required permissions:

```bash
# Instead of roles/storage.admin, use:
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectCreator"  # Only create objects

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"  # Only read objects
```

### 3. Encrypt Sensitive Data

Enable customer-managed encryption keys (CMEK):

```bash
# Create encryption key
gcloud kms keyrings create vertex-ai-eval \
  --location=us-central1

gcloud kms keys create evaluation-data \
  --location=us-central1 \
  --keyring=vertex-ai-eval \
  --purpose=encryption

# Grant key access to service account
gcloud kms keys add-iam-policy-binding evaluation-data \
  --location=us-central1 \
  --keyring=vertex-ai-eval \
  --member="serviceAccount:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/cloudkms.cryptoKeyEncrypterDecrypter"
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Permission Denied

```
Error: Permission denied on resource project gft-bu-gcp
```

**Solution**: Verify service account permissions:

```bash
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:vertex-ai-evaluator@$PROJECT_ID.iam.gserviceaccount.com"
```

#### 2. API Not Enabled

```
Error: The Vertex AI API has not been used in project...
```

**Solution**: Enable required APIs:

```bash
gcloud services enable aiplatform.googleapis.com
```

#### 3. Dataset Upload Failed

```
Error: 403 Access denied to gs://bucket/path
```

**Solution**: Check bucket permissions and location:

```bash
gsutil iam get gs://$PROJECT_ID-eval-staging
gsutil ls -L -b gs://$PROJECT_ID-eval-staging | grep Location
```

#### 4. BigQuery Table Not Found

```
Error: Table not found: project.dataset.table
```

**Solution**: Create table manually:

```bash
bq mk --table \
  $PROJECT_ID:architecture_domain_ans_eval.evaluation_results \
  evaluation_id:STRING,display_name:STRING,agent_id:STRING,timestamp:TIMESTAMP,metrics_summary:JSON,pass_rate:FLOAT
```

### Debug Mode

Enable detailed logging:

```bash
export GOOGLE_CLOUD_LOGGING_ENABLED=true
export GOOGLE_CLOUD_PROJECT=gft-bu-gcp

python -m eval.run_vertex_ai_evaluation --agent-version v1.0 2>&1 | tee evaluation.log
```

## 📚 References

- [Vertex AI Agent Builder Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-builder/overview)
- [Vertex AI Evaluation Service](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-agents)
- [Custom Metrics Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-custom-metrics)
- [BigQuery Integration](https://cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-export-bigquery)

## 📧 Support

For issues or questions:
1. Check troubleshooting section above
2. Review Google Cloud documentation
3. Contact GFT DevOps team
4. Open GitHub issue

---

**Last Updated**: November 29, 2025  
**Version**: 1.0  
**Status**: ✅ Production Ready


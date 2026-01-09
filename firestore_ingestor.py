import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import os

# Initialize Firebase Admin SDK
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your service account key file.
# For deployment, consider using environment variables or Google Cloud's default credentials.
# Example: cred = credentials.ApplicationDefault()

# For local testing, you might use a service account key file:
# cred = credentials.Certificate("path/to/your/serviceAccountKey.json")

# For this example, we'll assume the environment is set up for Application Default Credentials
# or that a service account key file path is provided via an environment variable.

# Check if a service account key path is provided via environment variable
service_account_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if service_account_key_path and os.path.exists(service_account_key_path):
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred)
    print(f"Firebase Admin SDK initialized using service account key: {service_account_key_path}")
elif os.getenv('FIRESTORE_EMULATOR_HOST'):
    # If running against Firestore emulator, no explicit credentials needed if project ID is set
    firebase_admin.initialize_app()
    print("Firebase Admin SDK initialized for Firestore emulator.")
else:
    # Fallback to Application Default Credentials (e.g., when deployed on GCP)
    try:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized using Application Default Credentials.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK with Application Default Credentials: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or running on GCP.")
        exit(1)

db = firestore.client()

def ingest_evidence(evidence_data):
    """
    Ingests evidence into the Firestore 'evidence' collection.
    """
    try:
        # Add server-side timestamp
        evidence_data['timestamp'] = datetime.datetime.now(datetime.timezone.utc)

        doc_ref = db.collection('evidence').add(evidence_data)
        print(f"Evidence ingested successfully. Document ID: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        print(f"Error ingesting evidence: {e}")
        return None

if __name__ == '__main__':
    # Example evidence data
    example_evidence = {
        "type": "ci-run",
        "source": "github-actions",
        "data": {
            "run_id": "987654321",
            "status": "failed",
            "commit_sha": "fedcba9876543210"
        }
    }
    ingest_evidence(example_evidence)

    example_evidence_2 = {
        "type": "vulnerability-scan",
        "source": "snyk",
        "data": {
            "scan_id": "snyk-scan-001",
            "vulnerabilities_found": 5,
            "severity": "high"
        }
    }
    ingest_evidence(example_evidence_2)

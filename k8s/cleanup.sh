#!/bin/bash

echo "🧹 Cleaning up Puku App from Kubernetes..."

# Delete all resources in puku-app namespace
kubectl delete namespace puku-app

# Delete PersistentVolumes (if any)
kubectl delete pv postgres-pv 2>/dev/null || true

# Delete StorageClass (if created)
kubectl delete storageclass standard 2>/dev/null || true

# Wait for namespace deletion
echo "⏳ Waiting for namespace deletion..."
kubectl wait --for=delete namespace/puku-app --timeout=60s 2>/dev/null || true

echo "✅ Cleanup completed!"
echo "📋 Check remaining resources: kubectl get all --all-namespaces"

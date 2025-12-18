#!/bin/bash

# Ensure proper kubeconfig
if [ ! -f "$HOME/.kube/config" ]; then
    mkdir -p $HOME/.kube
    sudo cp /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
fi

echo "🚀 Deploying Puku App to Kubernetes..."

# Apply namespace first
kubectl apply -f namespace.yaml

# Apply ConfigMaps and Secrets
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f postgres-init-configmap.yaml

# Apply PV (StorageClass skip if exists)
kubectl get storageclass standard >/dev/null 2>&1 || kubectl apply -f storageclass.yaml
kubectl apply -f postgres-pv.yaml

# Apply PVC
kubectl apply -f postgres-pvc.yaml

# Deploy PostgreSQL
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment -n puku-app

# Deploy backend services
kubectl apply -f user-service-deployment.yaml
kubectl apply -f user-service-service.yaml

kubectl apply -f recipe-service-deployment.yaml
kubectl apply -f recipe-service-service.yaml

kubectl apply -f rating-service-deployment.yaml
kubectl apply -f rating-service-service.yaml

# Deploy frontend
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

# Apply Ingress
kubectl apply -f ingress.yaml

echo "✅ Deployment completed!"
echo "📋 Check status with: kubectl get all -n puku-app"
echo "🌐 Access app at: http://puku-app.local (add to /etc/hosts)"

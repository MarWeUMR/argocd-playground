# How to bootstrap ArgoCD?

## ArgoCD Installation in the cluster

We need the namespace first.
Then simple apply the installation manifest.

```bash
kubectl create namespace argocd
kubectl -n argocd apply -f bootstrap-argo/install-argo.yaml
```

## ArgoCD setup

Next we need to configure the repository in the ArgoCD UI.

## ArgoCD App of Apps Pattern

Next up, apply the app-of-apps manifest:

```bash
kubectl apply -f app-of-apps/app-of-apps.yaml
```

Now the apps should be rolling out.


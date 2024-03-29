# How to bootstrap ArgoCD?

## ArgoCD Installation in the cluster

We need the namespace first.
Then simple apply the installation manifest.

```bash
kubectl apply -k .
kubectl -n argocd apply -f applicationset.yaml
```

Now the apps should be rolling out.

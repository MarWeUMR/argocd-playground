# How to bootstrap ArgoCD?

## Prerequisites

- `$SOPS_AGE_KEY_FILE` should point to your `age-key.txt` somewhere on your machine.


## ArgoCD Installation in the cluster

We need to bootstrap ArgoCD first with `kustomize`.
Use `just bootstrap-argocd` for that.
Then simple apply the `applicationset.yaml` manifest.

```bash
kubectl apply -k ./bootstrap/overlays/
kubectl apply -f applicationset.yaml
```

While boostrapping, the `sealed-secrets` secrets get decrypted and deployed to the cluster.
That ensures, that the actual `SealedSecret` resources can be used by kubernetes.

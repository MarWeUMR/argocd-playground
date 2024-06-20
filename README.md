# How to bootstrap ArgoCD?

## Prerequisites

- `$SOPS_AGE_KEY_FILE` should point to your `age-key.txt` somewhere on your machine.


## ArgoCD Installation in the cluster

We need to bootstrap ArgoCD first with `kustomize`.
Use `just bootstrap-argocd` for that.
Then simply apply the `applicationset.yaml` manifest.

```bash
kubectl apply -k ./bootstrap/overlays/
kubectl apply -f applicationset.yaml
```

While bootstrapping, the `sealed-secrets` secrets (cert/key) get decrypted.
These are used to generate the actual secret that is used by `sealed-secrets-controller` in the cluster.
That ensures, that the actual `SealedSecret` resources can be used by kubernetes.

# How to bootstrap ArgoCD?

## Prerequisites

- `$SOPS_AGE_KEY_FILE` should point to your `age-key.txt` somewhere on your machine.

The `age-key.txt` should looks like this:
```txt
# created: 2024-04-05T06:54:42Z
# public key: age16v4...
AGE-SECRET-KEY-18M2h...
```

## ArgoCD Installation in the cluster

We need to bootstrap ArgoCD initially with `kustomize`.
Use `just bootstrap-argocd` for that.
Then simply apply the `applicationset.yaml` manifest.

```bash
kubectl apply -f applicationset.yaml
```

While bootstrapping, the `sealed-secrets` secrets (cert/key) get decrypted.
These are used to generate the actual secret that is used by `sealed-secrets-controller` in the cluster.
This ensures, that the actual `SealedSecret` resources can be used by kubernetes.

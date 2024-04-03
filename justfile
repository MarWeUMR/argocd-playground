_default:
  @just --choose

# Install k3s and configure kubectl
install-k3s:
    # Download and execute the k3s installation script
    curl -sfL https://get.k3s.io | sh -
    # Ensure the k3s kubeconfig is accessible for kubectl
    sudo mkdir -p ~/.kube
    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
    sudo chown $USER ~/.kube/config
    echo "k3s installed and kubeconfig configured."

# Reset k3s cluster
reset-k3s:
    # Gracefully stop k3s service
    sudo systemctl stop k3s || true
    # Stop all k3s-related processes
    /usr/local/bin/k3s-killall.sh || true
    # Uninstall k3s
    /usr/local/bin/k3s-uninstall.sh || true
    # Attempt to unmount kubelet mounts if present
    sudo umount /var/lib/kubelet/* || true
    sudo umount /var/lib/kubelet || true
    # Cleanup remaining k3s artifacts
    sudo rm -rf /var/lib/kubelet
    sudo rm -rf /etc/rancher/k3s
    sudo rm -rf /var/lib/rancher/k3s
    echo "k3s cluster has been reset."

# Check k3s service status
status-k3s:
    # Display the current status of the k3s service
    sudo systemctl status k3s


bootstrap-argocd:
    # Deploy argocd with kustomize
    kubectl apply -k ./bootstrap
    @echo ""

    # Now we wait until the initial admin secret is ready. It will be printed to stdout
    @while ! kubectl -n argocd get secret argocd-initial-admin-secret >/dev/null 2>&1; do echo "`date`: Waiting for argocd-initial-admin-secret to become available..."; sleep 2; done
    @echo ""

    # The secret is now available (already decoded):
    @kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
    @echo ""

    # This is your argocd server URL
    @echo https://$(hostname -i):`kubectl get -n argocd service/argocd-server -o jsonpath="{.spec.ports[?(@.name=='https')].nodePort}"`


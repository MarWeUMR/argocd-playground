# Justfile for managing a k3s cluster

# Install k3s
install-k3s:
    # Download and execute the k3s installation script
    curl -sfL https://get.k3s.io | sh -
    sudo cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config


# Reset cluster
reset-k3s:
    # Stop k3s service
    sudo systemctl stop k3s || true
    # Stop all k3s
    /usr/local/bin/k3s-killall.sh || true
    # Uninstall k3s
    /usr/local/bin/k3s-uninstall.sh || true
    # Optionally, clean up any remaining artifacts
    sudo umount /var/lib/kubelet/* || true
    sudo umount /var/lib/kubelet || true
    # Now try to remove /var/lib/kubelet again
    sudo rm -rf /var/lib/kubelet
    sudo rm -rf /etc/rancher/k3s
    sudo rm -rf /var/lib/rancher/k3s
    sudo rm -rf /var/lib/kubelet

# Check k3s status
status-k3s:
    # Check the status of the k3s service
    sudo systemctl status k3s

